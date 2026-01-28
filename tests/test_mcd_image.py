"""Test for McD.jfif text extraction."""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import extract_text_from_image


def test_mcd_image_extraction():
    """Test text extraction from McD.jfif (McDonald's) image."""
    # Mock EasyOCR Reader
    with patch('main.easyocr.Reader') as mock_reader:
        # Create a mock reader instance
        mock_reader_instance = MagicMock()
        mock_reader.return_value = mock_reader_instance
        
        # Mock the readtext method - McDonald's related content
        mock_results = [
            ([[0, 0], [150, 0], [150, 30], [0, 30]], "McDonald's", 0.96),
            ([[150, 0], [250, 0], [250, 30], [150, 30]], "I'm", 0.92),
            ([[250, 0], [350, 0], [350, 30], [250, 30]], "lovin'", 0.93),
            ([[350, 0], [400, 0], [400, 30], [350, 30]], "it", 0.91),
        ]
        mock_reader_instance.readtext.return_value = mock_results
        
        # Test extraction
        image_path = "uploads/McD.jfif"
        results = extract_text_from_image(image_path)
        
        # Verify results exist
        assert len(results) > 0, "No text extracted from McDonald's image"
        
        # Extract the text from results
        extracted_texts = [text for (bbox, text, conf) in results]
        full_text = ' '.join(extracted_texts)
        
        # Verify McDonald's related text is detected
        assert any(keyword in full_text for keyword in ["McDonald", "McD", "lovin"]), \
            f"Expected McDonald's related text, got '{full_text}'"
        
        # Verify all confidences are above threshold
        for bbox, text, conf in results:
            assert conf >= 0.5, f"Confidence {conf} for '{text}' is below threshold 0.5"
        
        print(f"✓ Successfully extracted from McDonald's image: {full_text}")
