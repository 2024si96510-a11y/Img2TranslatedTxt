"""Test for DoorImage.jpeg text extraction with German translation."""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import extract_text_from_image, translate_text, format_results


def test_door_image_extraction_with_german_translation():
    """Test that DoorImage.jpeg extracts text and translates to German correctly."""
    # Mock EasyOCR Reader
    with patch('main.easyocr.Reader') as mock_reader, \
         patch('main.GoogleTranslator') as mock_translator_class:
        
        # Setup EasyOCR mock
        mock_reader_instance = MagicMock()
        mock_reader.return_value = mock_reader_instance
        
        # Mock the readtext method to return expected results
        mock_results = [
            ([[0, 0], [100, 0], [100, 20], [0, 20]], "What", 0.95),
            ([[100, 0], [150, 0], [150, 20], [100, 20]], "are", 0.92),
            ([[150, 0], [200, 0], [200, 20], [150, 20]], "the", 0.93),
            ([[200, 0], [250, 0], [250, 20], [200, 20]], "Best", 0.94),
            ([[250, 0], [350, 0], [350, 20], [250, 20]], "Colours", 0.91),
            ([[350, 0], [400, 0], [400, 20], [350, 20]], "for", 0.92),
            ([[400, 0], [420, 0], [420, 20], [400, 20]], "a", 0.90),
            ([[420, 0], [480, 0], [480, 20], [420, 20]], "Plain", 0.93),
            ([[480, 0], [550, 0], [550, 20], [480, 20]], "Door?", 0.92),
        ]
        mock_reader_instance.readtext.return_value = mock_results
        
        # Setup GoogleTranslator mock
        mock_translator_instance = MagicMock()
        mock_translator_class.return_value = mock_translator_instance
        mock_translator_instance.translate.return_value = "Was sind die besten Farben für eine einfache Tür?"
        
        # Test extraction
        image_path = "uploads/DoorImage.jpeg"
        results = extract_text_from_image(image_path)
        
        # Verify extraction results
        assert len(results) == 9, f"Expected 9 text segments, got {len(results)}"
        
        # Extract the text from results
        extracted_texts = [text for (bbox, text, conf) in results]
        full_text = ' '.join(extracted_texts)
        
        # Assert the expected extracted text
        assert full_text == "What are the Best Colours for a Plain Door?", \
            f"Expected 'What are the Best Colours for a Plain Door?', got '{full_text}'"
        
        # Test translation to German
        translated_text = translate_text(full_text, target_language='de')
        
        # Verify translation was called with correct parameters
        mock_translator_class.assert_called_with(source='auto', target='de')
        mock_translator_instance.translate.assert_called_with(full_text)
        
        # Verify the translated text
        expected_german = "Was sind die besten Farben für eine einfache Tür?"
        assert translated_text == expected_german, \
            f"Expected German translation '{expected_german}', got '{translated_text}'"
        
        # Test format_results with translation
        formatted_output = format_results(results, translate_to='de')
        
        # Verify both texts appear in formatted output
        assert full_text in formatted_output, "Extracted text not found in output"
        assert expected_german in formatted_output, "German translation not found in output"
        assert "Translated (de):" in formatted_output, "Translation label not found in output"
        
        print(f"✓ Successfully extracted: {full_text}")
        print(f"✓ Successfully translated to German: {translated_text}")


def test_door_image_translation_preserves_confidence():
    """Test that translation doesn't affect confidence scores."""
    with patch('main.easyocr.Reader') as mock_reader, \
         patch('main.GoogleTranslator') as mock_translator_class:
        
        mock_reader_instance = MagicMock()
        mock_reader.return_value = mock_reader_instance
        
        mock_results = [
            ([[0, 0], [100, 0], [100, 20], [0, 20]], "What", 0.95),
            ([[100, 0], [150, 0], [150, 20], [100, 20]], "are", 0.92),
        ]
        mock_reader_instance.readtext.return_value = mock_results
        
        mock_translator_instance = MagicMock()
        mock_translator_class.return_value = mock_translator_instance
        mock_translator_instance.translate.return_value = "Was sind"
        
        image_path = "uploads/DoorImage.jpeg"
        results = extract_text_from_image(image_path)
        
        # Verify confidences are preserved
        assert results[0][2] == 0.95, "First confidence score changed"
        assert results[1][2] == 0.92, "Second confidence score changed"
        
        # Verify all confidences are above threshold
        for bbox, text, conf in results:
            assert conf >= 0.5, f"Confidence {conf} for '{text}' is below threshold 0.5"
        
        print("✓ Confidence scores preserved after translation")
