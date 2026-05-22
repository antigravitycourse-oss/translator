# Urdu to Arabic PDF Translator with 1:1 Layout Preservation

This is a production-grade web application that translates PDFs from Urdu to Arabic while maintaining the exact visual layout (fonts, coordinates, sizes, colors, images, and tables) of the original document.

For scanned pages or pages without extractable text, the system automatically falls back to a **Multimodal OCR & Translation Layer** using Gemini Vision, which detects, translates, covers the original text, and overlays Arabic at the correct coordinates.

---

## Technical Architecture

*   **Frontend**: Responsive single-page application using HTML5, Tailwind CSS v3 (via CDN), and Vanilla JavaScript. Features a bilingual English/Urdu toggle and visual step-by-step progress tracking.
*   **Backend**: Async FastAPI (Python) server handling file upload, layout analysis, batch translation, layout reconstruction, and automatic temporary file cleanup.
*   **PDF Core**: PyMuPDF (`fitz`) handles coordinate-level text mapping, text redaction (`fill=False` to preserve backgrounds), and font-matched Right-to-Left (RTL) text insertion via `insert_htmlbox`.
*   **AI Engine**: Google Gemini API (`gemini-2.5-flash` or `gemini-2.5-pro`) performing batch text translations and vision-based coordinate layout mapping.

---

## Directory Structure

```
.
├── backend/
│   ├── main.py              # FastAPI main server and PDF processing pipeline
│   └── requirements.txt     # Python backend dependencies
├── frontend/
│   ├── index.html           # Bilingual UI Layout
│   └── app.js               # Frontend controller, drag-drop and SSE connection
└── README.md                # Documentation (this file)
```

---

## Local Development Setup

### 1. Prerequisites
*   Python 3.9 or higher installed on your system.
*   A Google Gemini API Key. You can get a free-tier key from [Google AI Studio](https://aistudio.google.com/).

### 2. Install Dependencies
Navigate to the project root and create a Python virtual environment:
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install the required packages
pip install -r backend/requirements.txt
```

### 3. Set Gemini API Key (Optional)
You can set your Gemini API Key as an environment variable, or enter it directly in the frontend UI.
```bash
# On Windows (PowerShell):
$env:GEMINI_API_KEY="your-api-key-here"

# On Windows (CMD):
set GEMINI_API_KEY=your-api-key-here

# On macOS/Linux:
export GEMINI_API_KEY="your-api-key-here"
```

### 4. Run the Server
Launch the FastAPI backend using `uvicorn`:
```bash
# Navigate to backend directory and run
cd backend
python main.py
```
Or run directly from the root directory:
```bash
uvicorn backend.main:app --reload --port 8000
```

### 5. Access the Web App
Open your browser and navigate to:
**[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

*The backend is configured to automatically download the beautiful Amiri Arabic font from Google Fonts on first start and serve the frontend files from the `frontend/` folder.*

---

## Cloud Deployment Guide

To deploy this project to production, you can split the frontend and backend or run them together on a single server.

### Backend Deployment (e.g., Render / HuggingFace Spaces)

#### Deploying on Render
1.  Sign in to [Render](https://render.com/).
2.  Create a new **Web Service** and link it to your GitHub Repository.
3.  Set the following configuration:
    *   **Runtime**: `Python`
    *   **Build Command**: `pip install -r backend/requirements.txt`
    *   **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
4.  Add Environment Variables:
    *   `GEMINI_API_KEY`: Your Google Gemini API Key (optional, users can also input their own on the UI).
5.  Render will deploy your backend and provide a public URL (e.g., `https://your-app.onrender.com`).

#### Deploying on Hugging Face Spaces
1.  Sign in to [Hugging Face](https://huggingface.co/) and click **New Space**.
2.  Name your Space, select **Docker** as the SDK, and choose **Blank** template.
3.  Set the Space visibility (Public/Private).
4.  Go to the Space **Settings** -> **Variables and secrets**, and add your secret:
    *   Key: `GEMINI_API_KEY`, Value: `your-api-key-here` (Optional, as clients can supply their own keys).
5.  Push your codebase (containing the root `Dockerfile`, `backend/`, and `frontend/` folders) to the Hugging Face Git remote repository:
    ```bash
    git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
    git push -u hf main --force
    ```
6.  Hugging Face will automatically build the container using the root `Dockerfile` and launch the application on port `7860`.
7.  Once the Space status changes to **Running**, your app will be active and hosted on Hugging Face.

---

### Frontend Deployment (e.g., Vercel)

If you want to host the frontend separately on Vercel for fast loading:
1.  Deploy the frontend directory to [Vercel](https://vercel.com).
2.  Edit `frontend/app.js` and set the `apiBase` variable to point to your Render backend URL:
    ```javascript
    // In frontend/app.js line 223:
    const apiBase = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? ''
        : 'https://your-app.onrender.com'; // Replace with your Render backend URL
    ```
3.  Vercel will build and serve your static frontend files globally.

---

## Key PDF Pipeline Details (1:1 Layout Magic)

1.  **Text Redaction without Background Artifacts**: We use `add_redact_annot` with `fill=False` (transparent) and call `apply_redactions(images=0, graphics=0)`. This completely wipes out the Urdu text from the rendering stream while leaving background images, vector shapes, and table border lines untouched.
2.  **HTML/CSS Layout Flow**: We insert the translated Arabic text using `insert_htmlbox` inside the original bounding boxes. PyMuPDF's Story engine compiles the HTML, formats the typography, renders it RTL, shapes the characters (using HarfBuzz), and automatically downscales the text font size if the translated Arabic text exceeds the bounding box boundaries.
3.  **Visual OCR Fallback**: If no digital text blocks are found on a page, it is treated as a scanned image. The backend renders the page to a PNG image, queries Gemini Vision to locate the Urdu blocks and translate them, generates a coordinate map, draws white background blocks on the scanned page to mask the original Urdu text, and overlays Arabic text at the exact same location.
