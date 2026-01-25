"""Main entry point for the application."""

import sys
from pathlib import Path
import easyocr
from deep_translator import GoogleTranslator


def extract_text_from_image(image_path, languages=['en'], confidence_threshold=0.5):
    """Extract text from an image using EasyOCR.
    
    Args:
        image_path: Path to the image file
        languages: List of language codes to recognize (default: ['en'])
        confidence_threshold: Minimum confidence score to include text (default: 0.5)
        
    Returns:
        List of tuples containing (bbox, text, confidence)
    """
    try:
        # Initialize the EasyOCR reader
        reader = easyocr.Reader(languages)
        
        # Read text from the image
        results = reader.readtext(image_path)
        
        # Filter results by confidence threshold to exclude ambiguous recognition
        # Each result is a tuple: (bbox, text, confidence)
        filtered_results = [
            (bbox, text, conf) for (bbox, text, conf) in results 
            if conf >= confidence_threshold
        ]
        
        return filtered_results
    except FileNotFoundError:
        print(f"Error: Image file not found: {image_path}")
        return []
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return []


def translate_text(text, target_language='es'):
    """Translate text to target language using Google Translate.
    
    Args:
        text: Text to translate
        target_language: Target language code (default: 'es' for Spanish)
        
    Returns:
        Translated text or original text if translation fails
    """
    try:
        if not text.strip():
            return text
        translator = GoogleTranslator(source='auto', target=target_language)
        translated = translator.translate(text)
        return translated
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return text


def format_results(results, translate_to=None):
    """Format extraction results with optional translation.
    
    Args:
        results: List of (bbox, text, confidence) tuples
        translate_to: Target language code for translation (optional)
        
    Returns:
        Formatted string with results
    """
    if not results:
        return "No text detected with sufficient confidence in the image."
    
    output_lines = []
    
    # Print individual extracted texts with confidence
    output_lines.append("Individual Extractions:")
    output_lines.append("-" * 50)
    for i, (bbox, text, conf) in enumerate(results, 1):
        output_lines.append(f"{i}. Text: '{text}' - Confidence: {conf:.2%}")
    
    output_lines.append("")
    output_lines.append("=" * 50)
    output_lines.append("")
    
    # Extract all text and append together
    extracted_texts = [text for (bbox, text, conf) in results]
    appended_text = ' '.join(extracted_texts)
    
    output_lines.append(f"Extracted Text: {appended_text}")
    
    # Add translation if requested
    if translate_to:
        translated = translate_text(appended_text, translate_to)
        output_lines.append(f"Translated ({translate_to}): {translated}")
    
    return '\n'.join(output_lines)


def main():
    """Run the main application."""
    if len(sys.argv) < 2:
        print("Usage: python main.py <image_path> [target_language]")
        print("\nExamples:")
        print("  python main.py image.png           # Extract text only")
        print("  python main.py image.png es        # Extract and translate to Spanish")
        print("  python main.py image.png fr        # Extract and translate to French")
        print("  python main.py image.png hi        # Extract and translate to Hindi")
        print("\nCommon language codes: es (Spanish), fr (French), de (German),")
        print("  hi (Hindi), zh-CN (Chinese), ja (Japanese), ar (Arabic)")
        sys.exit(1)
    
    image_path = sys.argv[1]
    translate_to = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not Path(image_path).exists():
        print(f"Error: Image file not found: {image_path}")
        sys.exit(1)
    
    print(f"Processing image: {image_path}")
    print("Extracting text with confidence >= 50%")
    if translate_to:
        print(f"Translating to: {translate_to}")
    print("-" * 50)
    
    results = extract_text_from_image(image_path)
    formatted_output = format_results(results, translate_to)
    
    print("Extracted Text:")
    print("-" * 50)
    print(formatted_output)


if __name__ == "__main__":
    main()
