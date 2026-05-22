// Bilingual Dictionary for English & Urdu
const TRANSLATIONS = {
    en: {
        title: "Urdu to Arabic PDF Translator",
        desc: "Translate your Urdu document to Arabic while preserving the exact layout, colors, tables, and images.",
        subLogo: "Urdu ➔ Arabic 1:1 Layout",
        apiKeyLbl: "Google Gemini API Key",
        apiKeyNote: "If left blank, the server's configured environment API Key will be used.",
        modelLbl: "AI Model Selection",
        modelNote: "All models support OCR fallback for scanned pages automatically.",
        dragDropTxt1: "Drag and drop your PDF file here",
        dragDropTxt2: "or click to browse from files (Max 25MB)",
        step1Title: "Step 1: Uploading & Parsing PDF Structure",
        step1Desc: "Extracting positions of text, fonts, colors, and images",
        step2Title: "Step 2: AI Translation (Urdu to Arabic)",
        step2Desc: "Batch translating blocks and OCR text using Google Gemini",
        step3Title: "Step 3: Rebuilding Layout & Font Matching",
        step3Desc: "Inserting Arabic text, auto-scaling fonts, and aligning blocks",
        step4Title: "Step 4: Ready for Download!",
        step4Desc: "Completing output file and packaging document",
        card1Title: "1:1 Visual Preservation",
        card1Desc: "Maintains PDF dimensions, absolute text locations, shapes, table cells, and graphic aesthetics.",
        card2Title: "Multimodal OCR Fallback",
        card2Desc: "Uses Gemini's Vision models to scan, OCR, translate, and overlay text on complex image-based PDFs automatically.",
        card3Title: "Privacy First Processing",
        card3Desc: "No files are kept permanently. Temporary PDF documents are deleted from the server immediately after download.",
        successTitle: "Translation Successful!",
        successDesc: "Your PDF has been successfully translated to Arabic. Visual formatting, images, and tables have been preserved.",
        downloadBtn: "Download PDF",
        resetBtn: "Translate Another",
        footerText: "Built using FastAPI, PyMuPDF, and Google Gemini API.",
        langBtn: "اردو",
        stages: {
            parsing: "Parsing PDF structure...",
            translating: "Translating document...",
            rebuilding: "Rebuilding layout and saving...",
            completed: "Translation complete! Ready to download."
        }
    },
    ur: {
        title: "اردو سے عربی پی ڈی ایف مترجم",
        desc: "اپنے اردو دستاویز کا عربی میں ترجمہ کریں جبکہ پی ڈی ایف کا اصل لے آؤٹ، رنگ، تصاویر اور ٹیبلز بالکل برقرار رہیں۔",
        subLogo: "اردو ➔ عربی 1:1 لے آؤٹ",
        apiKeyLbl: "گوگل جیمنی API کلید",
        apiKeyNote: "اگر خالی چھوڑ دیا جائے تو سرور پر موجود پہلے سے طے شدہ API کلید استعمال ہوگی۔",
        modelLbl: "مصنوعی ذہانت ماڈل کا انتخاب",
        modelNote: "تمام ماڈلز خودکار طور پر اسکین شدہ صفحات کے لیے OCR کو سپورٹ کرتے ہیں۔",
        dragDropTxt1: "اپنی پی ڈی ایف فائل یہاں لا کر چھوڑیں",
        dragDropTxt2: "یا اپنے کمپیوٹر سے منتخب کرنے کے لیے کلک کریں (زیادہ سے زیادہ 25MB)",
        step1Title: "مرحلہ 1: فائل اپ لوڈ اور پی ڈی ایف تجزیہ",
        step1Desc: "لکھائی کی پوزیشنز، فونٹس، رنگوں اور تصاویر کا اخراج",
        step2Title: "مرحلہ 2: اے آئی ترجمہ (اردو سے عربی)",
        step2Desc: "گوگل جیمنی کے ذریعے پیراگراف اور اسکین شدہ ٹیکسٹ کا ترجمہ",
        step3Title: "مرحلہ 3: لے آؤٹ کی دوبارہ تیاری اور فونٹ کی مطابقت",
        step3Desc: "عربی متن کا اندراج، فونٹس کو خودکار طور پر فٹ کرنا اور سیدھ کرنا",
        step4Title: "مرحلہ 4: ڈاؤن لوڈ کے لیے تیار ہے!",
        step4Desc: "آؤٹ پٹ فائل کی تکمیل اور دستاویز کی تیاری",
        card1Title: "1:1 لے آؤٹ کا تحفظ",
        card1Desc: "پی ڈی ایف کے سائز، تحریر کی درست پوزیشن، اشکال، اور ٹیبلز کے لے آؤٹ کو برقرار رکھتا ہے۔",
        card2Title: "ملٹی ماڈل OCR فال بیک",
        card2Desc: "تصویری اور اسکین شدہ پی ڈی ایف صفحات کا خودکار تجزیہ، ترجمہ اور اوورلے کرنے کے لیے جیمنی ویژن کا استعمال۔",
        card3Title: "پرائیویسی پہلی ترجیح",
        card3Desc: "فائلوں کو مستقل طور پر محفوظ نہیں کیا جاتا۔ ڈاؤن لوڈ کے فوراً بعد تمام فائلیں سرور سے حذف کر دی جاتی ہیں۔",
        successTitle: "ترجمہ کامیابی سے مکمل ہو گیا!",
        successDesc: "آپ کی پی ڈی ایف کا کامیابی سے عربی میں ترجمہ ہو گیا ہے۔ فارمیٹنگ، تصاویر اور ٹیبلز کو محفوظ رکھا گیا ہے۔",
        downloadBtn: "پی ڈی ایف ڈاؤن لوڈ کریں",
        resetBtn: "دوسری فائل کا ترجمہ کریں",
        footerText: "FastAPI، PyMuPDF، اور Google Gemini API کے اشتراک سے تیار کردہ۔",
        langBtn: "English",
        stages: {
            parsing: "پی ڈی ایف لے آؤٹ کا تجزیہ کیا جا رہا ہے...",
            translating: "دستاویز کا ترجمہ جاری ہے...",
            rebuilding: "لے آؤٹ دوبارہ ترتیب دیا جا رہا ہے...",
            completed: "ترجمہ مکمل! ڈاؤن لوڈ کے لیے تیار ہے۔"
        }
    }
};

let currentLang = 'en';
let currentDownloadId = null;
let eventSource = null;

// DOM Elements
const langToggleBtn = document.getElementById('lang-toggle');
const langBtnText = document.getElementById('lang-btn-text');
const subLogoTxt = document.getElementById('sub-logo-txt');
const mainTitle = document.getElementById('main-title');
const mainDesc = document.getElementById('main-desc');
const lblApiKey = document.getElementById('lbl-api-key');
const apiKeyInput = document.getElementById('api-key-input');
const apiKeyNote = document.getElementById('api-key-note');
const toggleKeyVisibilityBtn = document.getElementById('toggle-key-visibility');
const lblModelChoice = document.getElementById('lbl-model-choice');
const modelSelect = document.getElementById('model-select');
const modelNote = document.getElementById('model-note');

const uploadStage = document.getElementById('upload-stage');
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const uploadTxt1 = document.getElementById('upload-txt-1');
const uploadTxt2 = document.getElementById('upload-txt-2');
const errorMessage = document.getElementById('error-message');
const errorText = document.getElementById('error-text');

const progressStage = document.getElementById('progress-stage');
const progressBarFill = document.getElementById('progress-bar-fill');
const currentStageDesc = document.getElementById('current-stage-desc');
const progressPercentage = document.getElementById('progress-percentage');

const step1 = document.getElementById('step-1');
const step2 = document.getElementById('step-2');
const step3 = document.getElementById('step-3');
const step4 = document.getElementById('step-4');

const downloadStage = document.getElementById('download-stage');
const finishTitle = document.getElementById('finish-title');
const finishDesc = document.getElementById('finish-desc');
const downloadBtn = document.getElementById('download-btn');
const downloadBtnTxt = document.getElementById('download-btn-txt');
const resetBtn = document.getElementById('reset-btn');
const resetBtnTxt = document.getElementById('reset-btn-txt');

const card1Title = document.getElementById('card-1-title');
const card1Desc = document.getElementById('card-1-desc');
const card2Title = document.getElementById('card-2-title');
const card2Desc = document.getElementById('card-2-desc');
const card3Title = document.getElementById('card-3-title');
const card3Desc = document.getElementById('card-3-desc');
const footerText = document.getElementById('footer-text');

// Initialize API Key from LocalStorage
if (localStorage.getItem('gemini_api_key')) {
    apiKeyInput.value = localStorage.getItem('gemini_api_key');
}

// Save API Key on input change
apiKeyInput.addEventListener('input', () => {
    localStorage.setItem('gemini_api_key', apiKeyInput.value.trim());
});

// Toggle API Key Visibility
toggleKeyVisibilityBtn.addEventListener('click', () => {
    if (apiKeyInput.type === 'password') {
        apiKeyInput.type = 'text';
    } else {
        apiKeyInput.type = 'password';
    }
});

// Switch Language Function
function updateLanguage(lang) {
    currentLang = lang;
    const t = TRANSLATIONS[lang];
    
    // Header & Logo
    langBtnText.innerText = t.langBtn;
    subLogoTxt.innerText = t.subLogo;
    
    // Main Texts
    mainTitle.innerText = t.title;
    mainDesc.innerText = t.desc;
    
    // Inputs Panel
    lblApiKey.innerText = t.apiKeyLbl;
    apiKeyNote.innerText = t.apiKeyNote;
    lblModelChoice.innerText = t.modelLbl;
    modelNote.innerText = t.modelNote;
    
    // Upload Stage
    uploadTxt1.innerText = t.dragDropTxt1;
    uploadTxt2.innerText = t.dragDropTxt2;
    
    // Steps
    document.getElementById('step-1-title').innerText = t.step1Title;
    document.getElementById('step-1-desc').innerText = t.step1Desc;
    document.getElementById('step-2-title').innerText = t.step2Title;
    document.getElementById('step-2-desc').innerText = t.step2Desc;
    document.getElementById('step-3-title').innerText = t.step3Title;
    document.getElementById('step-3-desc').innerText = t.step3Desc;
    document.getElementById('step-4-title').innerText = t.step4Title;
    document.getElementById('step-4-desc').innerText = t.step4Desc;
    
    // Info Cards
    card1Title.innerText = t.card1Title;
    card1Desc.innerText = t.card1Desc;
    card2Title.innerText = t.card2Title;
    card2Desc.innerText = t.card2Desc;
    card3Title.innerText = t.card3Title;
    card3Desc.innerText = t.card3Desc;
    
    // Success Panel
    finishTitle.innerText = t.successTitle;
    finishDesc.innerText = t.successDesc;
    downloadBtnTxt.innerText = t.downloadBtn;
    resetBtnTxt.innerText = t.resetBtn;
    
    // Footer
    footerText.innerText = t.footerText;
    
    // Layout alignment adjust for RTL Urdu
    if (lang === 'ur') {
        document.body.style.direction = 'rtl';
    } else {
        document.body.style.direction = 'ltr';
    }
}

langToggleBtn.addEventListener('click', () => {
    updateLanguage(currentLang === 'en' ? 'ur' : 'en');
});

// Drag & Drop Functionality
dropZone.addEventListener('click', () => fileInput.click());

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('border-brand-500', 'bg-brand-500/[0.04]');
});

['dragleave', 'dragend'].forEach(type => {
    dropZone.addEventListener(type, () => {
        dropZone.classList.remove('border-brand-500', 'bg-brand-500/[0.04]');
    });
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('border-brand-500', 'bg-brand-500/[0.04]');
    
    if (e.dataTransfer.files.length) {
        handleFile(e.dataTransfer.files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (fileInput.files.length) {
        handleFile(fileInput.files[0]);
    }
});

function showError(text) {
    errorText.innerText = text;
    errorMessage.classList.remove('hidden');
}

function clearError() {
    errorMessage.classList.add('hidden');
}

// File Validation & Upload Trigger
function handleFile(file) {
    clearError();
    if (!file.name.toLowerCase().endsWith('.pdf')) {
        showError(currentLang === 'en' ? 'Please upload a valid PDF file.' : 'براہ کرم ایک درست پی ڈی ایف فائل اپ لوڈ کریں۔');
        return;
    }
    if (file.size > 25 * 1024 * 1024) {
        showError(currentLang === 'en' ? 'File is too large. Max allowed size is 25MB.' : 'فائل بہت بڑی ہے۔ زیادہ سے زیادہ سائز 25MB ہے۔');
        return;
    }
    
    startUpload(file);
}

// API Connection and Process Monitoring
async fn => {} // helper placeholder (unused)
async function startUpload(file) {
    uploadStage.classList.add('hidden');
    progressStage.classList.remove('hidden');
    updateProgress(0, TRANSLATIONS[currentLang].stages.parsing);
    setStepState(step1, 'active', '⏳');
    
    const formData = new FormData();
    formData.append('file', file);
    
    // Construct dynamic API base URL
    const apiBase = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? ''
        : ''; // Uses relative URLs when backend serves frontend
    
    try {
        const response = await fetch(`${apiBase}/api/upload`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.detail || 'Upload failed.');
        }
        
        const data = await response.json();
        const sessionId = data.session_id;
        
        // Start streaming the status via SSE
        monitorProgress(sessionId, apiBase);
        
    } catch (err) {
        handleProcessFailure(err.message);
    }
}

function monitorProgress(sessionId, apiBase) {
    const apiKey = apiKeyInput.value.trim();
    const model = modelSelect.value;
    
    // Connect to Server-Sent Events stream
    eventSource = new EventSource(`${apiBase}/api/translate-stream/${sessionId}?apiKey=${encodeURIComponent(apiKey)}&model=${encodeURIComponent(model)}`);
    
    eventSource.onmessage = function(event) {
        const data = JSON.parse(event.data);
        
        if (data.status === 'parsing') {
            updateProgress(data.progress, data.message || TRANSLATIONS[currentLang].stages.parsing);
            setStepState(step1, 'active', '⏳');
        } 
        else if (data.status === 'translating' || data.status === 'ocr_translating') {
            updateProgress(data.progress, data.message || TRANSLATIONS[currentLang].stages.translating);
            setStepState(step1, 'completed', '✓');
            setStepState(step2, 'active', '⏳');
        } 
        else if (data.status === 'rebuilding') {
            updateProgress(data.progress, data.message || TRANSLATIONS[currentLang].stages.rebuilding);
            setStepState(step1, 'completed', '✓');
            setStepState(step2, 'completed', '✓');
            setStepState(step3, 'active', '⏳');
        } 
        else if (data.status === 'completed') {
            updateProgress(100, data.message || TRANSLATIONS[currentLang].stages.completed);
            setStepState(step1, 'completed', '✓');
            setStepState(step2, 'completed', '✓');
            setStepState(step3, 'completed', '✓');
            setStepState(step4, 'completed', '✓');
            
            setTimeout(() => {
                showDownloadScreen(data.download_id);
            }, 800);
            
            eventSource.close();
        } 
        else if (data.status === 'error' || data.status === 'failed') {
            handleProcessFailure(data.message || 'An error occurred during translation.');
            eventSource.close();
        }
    };
    
    eventSource.onerror = function() {
        handleProcessFailure(currentLang === 'en' ? 'Connection to server lost.' : 'سرور سے رابطہ منقطع ہو گیا۔');
        eventSource.close();
    };
}

function updateProgress(percent, text) {
    progressBarFill.style.width = `${percent}%`;
    progressPercentage.innerText = `${percent}%`;
    currentStageDesc.innerText = text;
}

function setStepState(stepElement, state, iconText) {
    const iconContainer = stepElement.querySelector('.step-icon');
    const statusText = stepElement.querySelector('.step-status');
    
    if (state === 'active') {
        stepElement.classList.remove('opacity-50');
        stepElement.classList.add('border-brand-500/30', 'bg-brand-900/10');
        iconContainer.className = 'step-icon bg-brand-600 p-2 rounded-lg text-white animate-pulse';
        statusText.className = 'step-status text-brand-400 text-xs font-semibold';
        statusText.innerText = iconText;
    } 
    else if (state === 'completed') {
        stepElement.classList.remove('opacity-50', 'border-brand-500/30', 'bg-brand-900/10');
        stepElement.classList.add('border-emerald-500/10', 'bg-emerald-950/5');
        iconContainer.className = 'step-icon bg-emerald-500 p-2 rounded-lg text-white';
        statusText.className = 'step-status text-emerald-400 text-sm font-bold';
        statusText.innerText = iconText;
    }
}

function handleProcessFailure(message) {
    progressStage.classList.add('hidden');
    uploadStage.classList.remove('hidden');
    showError(message);
    resetProgressUI();
}

function resetProgressUI() {
    progressBarFill.style.width = '0%';
    progressPercentage.innerText = '0%';
    
    [step1, step2, step3, step4].forEach(step => {
        step.classList.add('opacity-50');
        step.classList.remove('border-brand-500/30', 'bg-brand-900/10', 'border-emerald-500/10', 'bg-emerald-950/5');
        const iconContainer = step.querySelector('.step-icon');
        iconContainer.className = 'step-icon bg-slate-800 p-2 rounded-lg text-slate-400 animate-none';
        const statusText = step.querySelector('.step-status');
        statusText.className = 'step-status text-slate-500 text-xs';
        statusText.innerText = '-';
    });
}

function showDownloadScreen(downloadId) {
    currentDownloadId = downloadId;
    progressStage.classList.add('hidden');
    downloadStage.classList.remove('hidden');
}

// Download Button Click Trigger
downloadBtn.addEventListener('click', () => {
    if (currentDownloadId) {
        const apiBase = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
            ? ''
            : '';
        window.location.href = `${apiBase}/api/download/${currentDownloadId}`;
    }
});

// Reset Form Functionality
resetBtn.addEventListener('click', () => {
    downloadStage.classList.add('hidden');
    uploadStage.classList.remove('hidden');
    fileInput.value = '';
    currentDownloadId = null;
    resetProgressUI();
    clearError();
});
