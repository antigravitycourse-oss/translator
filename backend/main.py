import os
import io
import json
import uuid
import httpx
import logging
import asyncio
import shutil
import tempfile
import time
from typing import Dict, Generator, List, Tuple
from fastapi import FastAPI, UploadFile, File, Header, Query, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import fitz  # PyMuPDF
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError
from PIL import Image

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Constants and Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(BASE_DIR, "fonts")
TEMP_DIR = os.path.join(BASE_DIR, "temp_data")
FONT_PATH = os.path.join(FONTS_DIR, "Amiri-Regular.ttf")

os.makedirs(FONTS_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

app = FastAPI(title="Urdu to Arabic PDF Layout-Preserved Translator")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store for active processing sessions
# session_id -> { "input_path": str, "output_path": str, "progress": int, "status": str }
sessions: Dict[str, dict] = {}

# Download Arabic Font at startup if not present
async def download_font_if_needed():
    if not os.path.exists(FONT_PATH):
        logger.info("Amiri-Regular.ttf not found. Downloading from Google Fonts...")
        url = "https://github.com/google/fonts/raw/main/ofl/amiri/Amiri-Regular.ttf?raw=true"
        try:
            async with httpx.AsyncClient(follow_redirects=True) as client:
                response = await client.get(url, timeout=30.0)
                if response.status_code == 200:
                    with open(FONT_PATH, "wb") as f:
                        f.write(response.content)
                    logger.info("Amiri font downloaded successfully.")
                else:
                    logger.error(f"Failed to download Amiri font. HTTP Status: {response.status_code}")
        except Exception as e:
            logger.error(f"Failed to download Amiri font: {e}")

@app.on_event("startup")
async def startup_event():
    await download_font_if_needed()
    # Clean up old temporary files from previous runs
    cleanup_old_temp_files(max_age_seconds=3600)

def cleanup_old_temp_files(max_age_seconds: int = 3600):
    """Deletes temporary files older than the specified age."""
    now = time.time()
    count = 0
    for filename in os.listdir(TEMP_DIR):
        file_path = os.path.join(TEMP_DIR, filename)
        try:
            if os.path.isfile(file_path):
                if now - os.path.getmtime(file_path) > max_age_seconds:
                    os.remove(file_path)
                    count += 1
        except Exception as e:
            logger.error(f"Error deleting temp file {file_path}: {e}")
    if count > 0:
        logger.info(f"Cleaned up {count} expired temporary files.")

# Helper function to remove session files
def clean_session_files(session_id: str):
    session = sessions.get(session_id)
    if session:
        for key in ["input_path", "output_path"]:
            path = session.get(key)
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                    logger.info(f"Deleted temporary file: {path}")
                except Exception as e:
                    logger.error(f"Failed to delete {path}: {e}")
        sessions.pop(session_id, None)

# Helper functions for translation logic
def get_dominant_style(block: dict) -> Tuple[float, str]:
    """Extracts the font size and color of the longest span in a block."""
    max_len = -1
    dom_size = 12.0
    dom_color = 0x000000
    
    for line in block.get("lines", []):
        for span in line.get("spans", []):
            text_len = len(span.get("text", ""))
            if text_len > max_len:
                max_len = text_len
                dom_size = span.get("size", 12.0)
                dom_color = span.get("color", 0x000000)
                
    color_hex = f"#{dom_color & 0xFFFFFF:06x}"
    return dom_size, color_hex

def parse_gemini_json_response(response_text: str) -> dict:
    """Parses Gemini raw JSON responses, stripping any markdown code formatting."""
    text = response_text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()
    return json.loads(text)

async def translate_text_blocks(blocks_dict: dict, api_key: str, model_name: str) -> dict:
    """Translates text blocks using Gemini API, batching them into a single JSON request."""
    if not blocks_dict:
        return {}
    
    genai.configure(api_key=api_key)
    
    # Configure Gemini Model with System Instructions
    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=(
            "You are a professional Urdu-to-Arabic translator. "
            "Translate the values of the JSON object from Urdu to classical Arabic. "
            "Do NOT translate the keys, preserve them exactly. "
            "Maintain the exact paragraph structures and context. "
            "Do NOT add any conversational text or markdown code block formatting. "
            "Return only the translated JSON object."
        )
    )
    
    prompt = json.dumps(blocks_dict, ensure_ascii=False)
    
    max_retries = 5
    backoff = 2.0
    for attempt in range(max_retries):
        try:
            response = await model.generate_content_async(
                contents=[prompt],
                generation_config={"response_mime_type": "application/json"}
            )
            return parse_gemini_json_response(response.text)
        except (GoogleAPIError, Exception) as e:
            logger.warning(f"Gemini Translation API call attempt {attempt+1} failed: {e}")
            if attempt == max_retries - 1:
                raise e
            sleep_time = (backoff ** attempt) + 0.5
            await asyncio.sleep(sleep_time)
    return {}

async def ocr_and_translate_scanned_page(page_image_bytes: bytes, api_key: str, model_name: str) -> dict:
    """Performs visual OCR and translation on a scanned PDF page using Gemini Vision."""
    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=(
            "You are a professional Urdu-to-Arabic translator and visual OCR expert. "
            "Analyze the image of a scanned Urdu page. Locate all text blocks. "
            "Translate each text block into classical Arabic. "
            "You must return a JSON object with a single key 'blocks' mapping to a list of objects. "
            "Each object must contain:\n"
            "1. 'translated_text': The classical Arabic translation of the text block.\n"
            "2. 'box_2d': The normalized bounding box [ymin, xmin, ymax, xmax] of the original Urdu text "
            "where coordinates are integers normalized in the range [0, 1000] relative to the image size.\n"
            "Do NOT return any conversational comments or markdown block backticks. Return ONLY raw JSON."
        )
    )
    
    img = Image.open(io.BytesIO(page_image_bytes))
    
    max_retries = 5
    backoff = 2.0
    for attempt in range(max_retries):
        try:
            response = await model.generate_content_async(
                contents=[img, "Translate all text in this image and return their bounding boxes in JSON format."],
                generation_config={"response_mime_type": "application/json"}
            )
            return parse_gemini_json_response(response.text)
        except (GoogleAPIError, Exception) as e:
            logger.warning(f"Gemini OCR API call attempt {attempt+1} failed: {e}")
            if attempt == max_retries - 1:
                raise e
            sleep_time = (backoff ** attempt) + 0.5
            await asyncio.sleep(sleep_time)
    return {"blocks": []}

def is_page_scanned(blocks: list) -> bool:
    """Determines if a page is scanned by checking the amount of extracted text."""
    total_chars = 0
    for block in blocks:
        if block.get("type") == 0:  # Text block
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span.get("text", "")
                    # Clean out spaces and numbers
                    clean_text = "".join(c for c in text if not c.isspace() and not c.isdigit())
                    total_chars += len(clean_text)
    return total_chars < 15

# Endpoints
@app.post("/api/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Receives the PDF file, validates it, and generates a session ID."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    session_id = str(uuid.uuid4())
    input_path = os.path.join(TEMP_DIR, f"input_{session_id}.pdf")
    output_path = os.path.join(TEMP_DIR, f"translated_{session_id}.pdf")
    
    try:
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Verify the PDF is valid and not encrypted
        doc = fitz.open(input_path)
        if doc.is_encrypted:
            doc.close()
            os.remove(input_path)
            raise HTTPException(status_code=400, detail="Password-protected PDFs are not supported.")
        doc.close()
        
        sessions[session_id] = {
            "input_path": input_path,
            "output_path": output_path,
            "status": "pending",
            "progress": 0
        }
        return {"session_id": session_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload processing failed: {e}")
        if os.path.exists(input_path):
            os.remove(input_path)
        raise HTTPException(status_code=500, detail="Failed to upload and validate PDF.")

@app.get("/api/translate-stream/{session_id}")
async def translate_stream(
    session_id: str,
    api_key: str = Query(..., alias="apiKey"),
    model_name: str = Query("gemini-2.5-flash", alias="model")
):
    """SSE streaming endpoint for translating the PDF and tracking progress."""
    session = sessions.get(session_id)
    if not session:
        return StreamingResponse(
            (f"data: {json.dumps({'status': 'error', 'message': 'Invalid session ID.'})}\n\n" for _ in range(1)),
            media_type="text/event-stream"
        )
        
    async def process_generator() -> Generator[str, None, None]:
        input_path = session["input_path"]
        output_path = session["output_path"]
        
        try:
            # Step 1: Open & Parse PDF structure
            yield f"data: {json.dumps({'status': 'parsing', 'progress': 10, 'message': 'Parsing PDF structure...'})}\n\n"
            await asyncio.sleep(0.5)
            
            doc = fitz.open(input_path)
            total_pages = len(doc)
            
            # Rebuilt document
            out_doc = fitz.open()
            
            # Setup custom fonts archive for insert_htmlbox
            arch = pymupdf.Archive(FONTS_DIR)
            
            for page_idx in range(total_pages):
                page = doc[page_idx]
                page_width = page.rect.width
                page_height = page.rect.height
                
                # Check if it's a scanned page
                text_dict = page.get_text("dict")
                blocks = text_dict.get("blocks", [])
                
                # Create a blank/duplicate canvas matching original size
                new_page = out_doc.new_page(width=page_width, height=page_height)
                
                if is_page_scanned(blocks):
                    yield f"data: {json.dumps({'status': 'translating', 'progress': 10 + int((page_idx) / total_pages * 80), 'message': f'OCR & translating scanned page {page_idx + 1}/{total_pages}...'})}\n\n"
                    
                    # 1. Render page to image bytes
                    pix = page.get_pixmap(dpi=150)
                    img_bytes = pix.tobytes("png")
                    
                    # 2. Get OCR & Translation coordinates from Gemini Vision
                    ocr_res = await ocr_and_translate_scanned_page(img_bytes, api_key, model_name)
                    
                    # 3. Rebuild layout on the new page
                    # First, copy the original page visual appearance as an image background so all graphics are kept
                    # Wait, for scanned PDF, page itself is an image, so we draw it onto the new page first!
                    # Actually, we can draw the original page background pixmap on the new page
                    new_page.insert_image(new_page.rect, stream=img_bytes)
                    
                    # Draw OCR blocks
                    for item in ocr_res.get("blocks", []):
                        box = item.get("box_2d")
                        translated_text = item.get("translated_text", "").strip()
                        if not box or len(box) != 4 or not translated_text:
                            continue
                            
                        # Map normalized coordinates back to PDF points
                        # box format: [ymin, xmin, ymax, xmax] (0 to 1000 scale)
                        ymin, xmin, ymax, xmax = box
                        x0 = (xmin / 1000.0) * page_width
                        y0 = (ymin / 1000.0) * page_height
                        x1 = (xmax / 1000.0) * page_width
                        y1 = (ymax / 1000.0) * page_height
                        
                        rect = fitz.Rect(x0, y0, x1, y1)
                        
                        # Cover the original Urdu text with a white rectangle (or matching page background)
                        new_page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1), width=0)
                        
                        # Draw translated Arabic text in the same rect
                        css_str = f"""
                        @font-face {{
                            font-family: 'Amiri';
                            src: url('Amiri-Regular.ttf');
                        }}
                        body {{
                            font-family: 'Amiri', serif;
                            direction: rtl;
                            text-align: right;
                            font-size: 14pt;
                            color: #000000;
                            margin: 0;
                            padding: 0;
                            line-height: 1.2;
                        }}
                        """
                        html_content = f"<div>{translated_text}</div>"
                        new_page.insert_htmlbox(rect, html_content, css=css_str, archive=arch)
                        
                else:
                    # Non-scanned text-based page
                    yield f"data: {json.dumps({'status': 'translating', 'progress': 10 + int((page_idx) / total_pages * 80), 'message': f'Translating page {page_idx + 1}/{total_pages}...'})}\n\n"
                    
                    # 1. Extract text blocks and filter empty blocks
                    text_blocks = []
                    blocks_to_translate = {}
                    
                    # First, copy vector graphics and images of the original page to new page
                    new_page.show_pdf_page(new_page.rect, doc, page_idx)
                    
                    for b_idx, block in enumerate(blocks):
                        if block.get("type") == 0:  # Text block
                            # Concatenate lines to get the block text
                            block_text = ""
                            for line in block.get("lines", []):
                                for span in line.get("spans", []):
                                    block_text += span.get("text", "")
                            
                            # Clean text and determine if it requires translation
                            clean_text = block_text.strip()
                            # Check if it contains actual words (non-digits/symbols)
                            letters = [c for c in clean_text if not c.isdigit() and not c.isspace()]
                            if clean_text and len(letters) > 1:
                                key = f"b_{b_idx}"
                                blocks_to_translate[key] = clean_text
                                text_blocks.append((key, block))
                                
                    # 2. Query Gemini
                    translated_dict = {}
                    if blocks_to_translate:
                        try:
                            translated_dict = await translate_text_blocks(blocks_to_translate, api_key, model_name)
                        except Exception as e:
                            logger.error(f"Failed to translate blocks on page {page_idx + 1}: {e}")
                            # Fallback: keep original text blocks
                            translated_dict = blocks_to_translate
                    
                    # 3. Apply redactions on original page content in new page to wipe out Urdu text
                    # We add transparent redaction annotations on all spans of text blocks that were translated
                    for key, block in text_blocks:
                        for line in block.get("lines", []):
                            for span in line.get("spans", []):
                                r = fitz.Rect(span["bbox"])
                                new_page.add_redact_annot(r, fill=False)
                                
                    # Run apply_redactions. Set images=0 and graphics=0 to preserve photos and vector designs
                    new_page.apply_redactions(images=0, graphics=0)
                    
                    # 4. Rebuild translated Arabic text inside bounding boxes
                    for key, block in text_blocks:
                        translated_text = translated_dict.get(key)
                        if not translated_text:
                            # Fallback to original text if missing
                            translated_text = blocks_to_translate.get(key, "")
                            
                        # Get dominant styling
                        size, color_hex = get_dominant_style(block)
                        
                        rect = fitz.Rect(block["bbox"])
                        
                        # Generate HTML content
                        html_content = f"<div>{translated_text}</div>"
                        
                        # Align right for RTL Arabic
                        css_str = f"""
                        @font-face {{
                            font-family: 'Amiri';
                            src: url('Amiri-Regular.ttf');
                        }}
                        body {{
                            font-family: 'Amiri', serif;
                            direction: rtl;
                            text-align: right;
                            font-size: {size}pt;
                            color: {color_hex};
                            margin: 0;
                            padding: 0;
                            line-height: 1.25;
                        }}
                        """
                        
                        # Insert text box with automatic styling, shaping, and shrinking
                        new_page.insert_htmlbox(rect, html_content, css=css_str, archive=arch)
            
            # Step 3: Rebuilding Layout & Font Matching
            yield f"data: {json.dumps({'status': 'rebuilding', 'progress': 90, 'message': 'Rebuilding layout and saving PDF...'})}\n\n"
            await asyncio.sleep(0.5)
            
            # Subset fonts to keep size minimal, then save
            try:
                out_doc.subset_fonts()
            except Exception as font_err:
                logger.warning(f"Could not subset fonts: {font_err}")
                
            out_doc.save(output_path, garbage=3, deflate=True)
            out_doc.close()
            doc.close()
            
            # Step 4: Ready for Download!
            session["status"] = "completed"
            session["progress"] = 100
            yield f"data: {json.dumps({'status': 'completed', 'progress': 100, 'download_id': session_id, 'message': 'Translation complete! Ready to download.'})}\n\n"
            
        except Exception as e:
            logger.error(f"Processing session {session_id} failed: {e}", exc_info=True)
            session["status"] = "failed"
            yield f"data: {json.dumps({'status': 'error', 'message': f'Processing failed: {str(e)}'})}\n\n"
            
    return StreamingResponse(process_generator(), media_type="text/event-stream")

@app.get("/api/download/{session_id}")
async def download_file(session_id: str, background_tasks: BackgroundTasks):
    """Downloads the completed PDF and triggers background cleanup of session files."""
    session = sessions.get(session_id)
    if not session or not session.get("output_path") or not os.path.exists(session["output_path"]):
        raise HTTPException(status_code=404, detail="File not found or session expired.")
        
    output_path = session["output_path"]
    
    # Clean up file immediately after sending it
    background_tasks.add_task(clean_session_files, session_id)
    
    return FileResponse(
        path=output_path,
        media_type="application/pdf",
        filename="translated_arabic.pdf"
    )

# Serve Frontend static files
# We place this at the bottom so it doesn't intercept API routes
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")
if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
else:
    logger.warning("Frontend directory not found at root, static files serving disabled.")

if __name__ == "__main__":
    import uvicorn
    # Clean up expired files at startup
    cleanup_old_temp_files(max_age_seconds=3600)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
