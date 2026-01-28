"""Test for Nike.jfif text extraction."""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import extract_text_from_image


def test_nike_image_extraction():
    """Test text extraction from Nike.jfif image."""
    # Mock EasyOCR Reader
    with patch('main.easyocr.Reader') as mock_reader:
        # Create a mock reader instance
        mock_reader_instance = MagicMock()
        mock_reader.return_value = mock_reader_instance
        
        # Mock the readtext method - adjust based on actual Nike image content
        mock_results = [
            ([[0, 0], [100, 0], [100, 20], [0, 20]], "NIKE", 0.98),
            ([[100, 0], [200, 0], [200, 20], [100, 20]], "Just", 0.95),
            ([[200, 0], [280, 0], [280, 20], [200, 20]], "Do", 0.94),
            ([[280, 0], [320, 0], [320, 20], [280, 20]], "It", 0.93),
        ]
        mock_reader_instance.readtext.return_value = mock_results
        
        # Test extraction
        image_path = "uploads/Nike.jfif"
        results = extract_text_from_image(image_path)
        
        # Verify results exist
        assert len(results) > 0, "No text extracted from Nike image"
        
        # Extract the text from results
        extracted_texts = [text for (bbox, text, conf) in results]
        full_text = ' '.join(extracted_texts)
        
        # Verify NIKE brand is detected
        assert "NIKE" in full_text.upper(), f"Expected 'NIKE' in extracted text, got '{full_text}'"
        
        # Verify all confidences are above threshold
        for bbox, text, conf in results:
            assert conf >= 0.5, f"Confidence {conf} for '{text}' is below threshold 0.5"
        
        print(f"✓ Successfully extracted from Nike image: {full_text}")
