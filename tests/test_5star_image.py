"""Test for 5Star.jfif text extraction."""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import extract_text_from_image


def test_5star_image_extraction():
    """Test text extraction from 5Star.jfif image."""
    # Mock EasyOCR Reader
    with patch('main.easyocr.Reader') as mock_reader:
        # Create a mock reader instance
        mock_reader_instance = MagicMock()
        mock_reader.return_value = mock_reader_instance
        
        # Mock the readtext method - 5 Star chocolate bar content
        mock_results = [
            ([[0, 0], [50, 0], [50, 25], [0, 25]], "5", 0.97),
            ([[50, 0], [120, 0], [120, 25], [50, 25]], "STAR", 0.96),
            ([[120, 0], [220, 0], [220, 25], [120, 25]], "Chocolate", 0.94),
        ]
        mock_reader_instance.readtext.return_value = mock_results
        
        # Test extraction
        image_path = "uploads/5Star.jfif"
        results = extract_text_from_image(image_path)
        
        # Verify results exist
        assert len(results) > 0, "No text extracted from 5Star image"
        
        # Extract the text from results
        extracted_texts = [text for (bbox, text, conf) in results]
        full_text = ' '.join(extracted_texts)
        
        # Verify 5 Star related text is detected
        assert any(keyword in full_text.upper() for keyword in ["5", "STAR", "5STAR"]), \
            f"Expected '5 Star' related text, got '{full_text}'"
        
        # Verify all confidences are above threshold
        for bbox, text, conf in results:
            assert conf >= 0.5, f"Confidence {conf} for '{text}' is below threshold 0.5"
        
        print(f"✓ Successfully extracted from 5Star image: {full_text}")
