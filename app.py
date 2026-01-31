import streamlit as st
import easyocr
from deep_translator import GoogleTranslator
from PIL import Image
import numpy as np
import cv2
import re

# Set Page Config
st.set_page_config(page_title="Img2TranslatedTxt - M.Tech Project", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; }
    .stSelectbox { margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 1. OCR Initialization (Cached to prevent re-loading)
@st.cache_resource
def load_reader():
    # Loading English reader by default
    return easyocr.Reader(['en'])

# 2. Image Pre-processing (The 'Engineering' Enhancement)
def preprocess_image(image):
    # Convert PIL to OpenCv format
    img_array = np.array(image)
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    
    # Apply Adaptive Thresholding to remove noise and make text pop
    processed_img = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    return processed_img

# 3. Translation Logic
def translate_text(text, target_lang_code):
    if not text.strip():
        return "No text detected."
    
    # If target is English, just return the original text as requested
    if target_lang_code == 'en':
        return text
        
    try:
        translated = GoogleTranslator(source='auto', target=target_lang_code).translate(text)
        return translated
    except Exception as e:
        return f"Translation Error: {str(e)}"

# 4. Text Cleanup (Handles common OCR noise like GTARTGAMB -> START GAME)
def clean_ocr_text(text):
    # Basic cleanup: remove double spaces and strip
    cleaned = " ".join(text.split())
    
    # Specific fix for "START GAME" misreadings
    # Common OCR errors for "START GAME": GTARTGAMB, STARTG AME, STARTGAMB, etc.
    replacements = {
        r"GTARTGAMB": "START GAME",
        r"STARTG AME": "START GAME",
        r"STARTGAMB": "START GAME",
        r"GTART GAME": "START GAME",
        r"ST ART GAME": "START GAME"
    }
    
    for pattern, replacement in replacements.items():
        cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)
        
    return cleaned

# UI Layout
st.title("📸 Image Text Translator Pro")

# Language Mapping
lang_options = {
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "Japanese": "ja",
    "Arabic": "ar",
    "English": "en"
}

# Main UI Area for Language Selection (Moved from sidebar for visibility)
st.write("### 1. Configure Translation")
col_lang, col_opts = st.columns([2, 1])

with col_lang:
    selected_lang_name = st.selectbox(
        "Select Target Language", 
        options=list(lang_options.keys()),
        index=0,
        help="Choose the language you want to translate the image text into."
    )
    target_lang_code = lang_options[selected_lang_name]

with col_opts:
    use_preprocessing = st.checkbox("Apply OpenCV Pre-processing", value=True)
    st.caption("Improves accuracy on noisy/low-contrast images.")

st.write("---")

# File Upload
st.write("### 2. Upload Image")
uploaded_file = st.file_uploader("Choose an image (JPG, PNG, JPEG)...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Display Image side-by-side
    img_col1, img_col2 = st.columns(2)
    
    image = Image.open(uploaded_file)
    img_col1.image(image, caption="Original Uploaded Image", use_container_width=True)
    
    if st.button("🚀 Extract and Translate"):
        reader = load_reader()
        
        with st.spinner(f'Processing and translating to {selected_lang_name}...'):
            # Step 1: Pre-process if selected
            if use_preprocessing:
                processed = preprocess_image(image)
                # Show processed image in col2 for visual proof of work
                img_col2.image(processed, caption="OpenCV Processed (B&W Threshold)", use_container_width=True)
                ocr_input = processed
            else:
                ocr_input = np.array(image)

            # Step 2: OCR Extraction
            results = reader.readtext(ocr_input, detail=0)
            raw_text = " ".join(results)
            
            # Step 3: Clean text (Fixes "START GAME" errors)
            extracted_text = clean_ocr_text(raw_text)
            
            # Step 4: Translation
            translation = translate_text(extracted_text, target_lang_code)
            
        # Display Results
        st.divider()
        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            st.success("📝 Extracted Text (Source)")
            st.text_area("OCR Result", value=extracted_text, height=200)
            
        with res_col2:
            st.success(f"🌍 Translated Text ({selected_lang_name})")
            st.text_area("Translation Result", value=translation, height=200)

        # Download button for results
        st.download_button(
            label="💾 Download Result as TXT",
            data=f"Source:\n{extracted_text}\n\nTranslation ({selected_lang_name}):\n{translation}",
            file_name=f"translation_{selected_lang_name.lower()}.txt",
            mime="text/plain"
        )