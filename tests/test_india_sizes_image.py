"""Test for IndiaSizes.jfif text extraction."""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import extract_text_from_image


def test_india_sizes_image_extraction():
    """Test text extraction from IndiaSizes.jfif image."""
    # Mock EasyOCR Reader
    with patch('main.easyocr.Reader') as mock_reader:
        # Create a mock reader instance
        mock_reader_instance = MagicMock()
        mock_reader.return_value = mock_reader_instance
        
        # Mock the readtext method - India size chart content
        mock_results = [
            ([[0, 0], [80, 0], [80, 20], [0, 20]], "India", 0.95),
            ([[80, 0], [150, 0], [150, 20], [80, 20]], "Size", 0.94),
            ([[150, 0], [220, 0], [220, 20], [150, 20]], "Chart", 0.93),
            ([[0, 25], [50, 25], [50, 45], [0, 45]], "S", 0.91),
            ([[50, 25], [100, 25], [100, 45], [50, 45]], "M", 0.92),
            ([[100, 25], [150, 25], [150, 45], [100, 45]], "L", 0.91),
            ([[150, 25], [200, 25], [200, 45], [150, 45]], "XL", 0.90),
        ]
        mock_reader_instance.readtext.return_value = mock_results
        
        # Test extraction
        image_path = "uploads/IndiaSizes.jfif"
        results = extract_text_from_image(image_path)
        
        # Verify results exist
        assert len(results) > 0, "No text extracted from IndiaSizes image"
        
        # Extract the text from results
        extracted_texts = [text for (bbox, text, conf) in results]
        full_text = ' '.join(extracted_texts)
        
        # Verify India or Size related text is detected
        assert any(keyword in full_text for keyword in ["India", "Size", "Chart"]), \
            f"Expected 'India', 'Size', or 'Chart' in extracted text, got '{full_text}'"
        
        # Verify all confidences are above threshold
        for bbox, text, conf in results:
            assert conf >= 0.5, f"Confidence {conf} for '{text}' is below threshold 0.5"
        
        print(f"✓ Successfully extracted from IndiaSizes image: {full_text}")
