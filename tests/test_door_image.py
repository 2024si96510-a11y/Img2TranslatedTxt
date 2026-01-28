"""Test for DoorImage.jpeg text extraction."""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import extract_text_from_image


def test_door_image_extraction():
    """Test that DoorImage.jpeg extracts 'What are the Best Colours for a Plain Door?'"""
    # Mock EasyOCR Reader
    with patch('main.easyocr.Reader') as mock_reader:
        # Create a mock reader instance
        mock_reader_instance = MagicMock()
        mock_reader.return_value = mock_reader_instance
        
        # Mock the readtext method to return expected results
        # Format: (bbox, text, confidence)
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
        
        # Test extraction
        image_path = "uploads/DoorImage.jpeg"
        results = extract_text_from_image(image_path)
        
        # Verify results
        assert len(results) == 9, f"Expected 9 text segments, got {len(results)}"
        
        # Extract the text from results
        extracted_texts = [text for (bbox, text, conf) in results]
        full_text = ' '.join(extracted_texts)
        
        # Assert the expected text
        assert full_text == "What are the Best Colours for a Plain Door?", \
            f"Expected 'What are the Best Colours for a Plain Door?', got '{full_text}'"
        
        # Verify all confidences are above threshold
        for bbox, text, conf in results:
            assert conf >= 0.5, f"Confidence {conf} for '{text}' is below threshold 0.5"
        
        print(f"✓ Successfully extracted: {full_text}")
