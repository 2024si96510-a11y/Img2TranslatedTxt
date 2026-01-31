# Python Project

A Python project to extract the content of input images and translate the detected text into a requested language. Now featuring a web-based GUI for easier interaction.

## Project Structure

```
.
├── src/              # Source code
├── tests/            # Test files
├── app.py            # Streamlit Web Application (GUI)
├── .gitignore        # Git ignore patterns
├── pyproject.toml    # Project configuration
└── README.md         # This file
```

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`

3. Install dependencies:
   ```bash
   # Install core project and CLI dependencies
   pip install -e .
   # Install additional UI and Image Processing dependencies
   pip install streamlit opencv-python pillow deep-translator easyocr
   ```

## Usage

Run the main application:

1. Web Application (Recommended)

   The project now includes a Web UI for a more interactive experience, featuring OpenCV image cleaning and a language dropdown.

   Run the Streamlit app:

   streamlit run app.py


Features: - Drag-and-drop image uploading.

   OpenCV Pre-processing: Toggle "OpenCV Clean" to improve OCR accuracy on noisy images.

Language Selection: Choose from Hindi, Spanish, French, Japanese, Arabic, or English.

Download Result: Export your translations directly as a .txt file.

2. Command Line Interface (CLI)

   You can still run the script directly from the terminal.

Extract text only (English):

   python src/main.py <image_path>


Extract and Translate:

   python src/main.py <image_path> <hi/es/fr/ja/ar/en>

## Testing

The project includes unit tests for each image processing scenario. Each test file validates text extraction for specific images.

### Available Test Files

- `test_door_image.py` - Tests extraction of "What are the Best Colours for a Plain Door?" from DoorImage.jpeg
- `test_door_image_translation_de.py` - Tests extraction and German translation from DoorImage.jpeg
- `test_nike_image.py` - Tests Nike brand text extraction from Nike.jfif
- `test_mcd_image.py` - Tests McDonald's text extraction from McD.jfif
- `test_5star_image.py` - Tests 5 Star chocolate text extraction from 5Star.jfif
- `test_india_sizes_image.py` - Tests India size chart text extraction from IndiaSizes.jfif

### Running Tests

**Run all tests:**
```bash
pytest tests/ -v
```

**Run a specific test file:**
```bash
pytest tests/test_door_image.py -v
pytest tests/test_door_image_translation_de.py -v
pytest tests/test_nike_image.py -v
pytest tests/test_mcd_image.py -v
pytest tests/test_5star_image.py -v
pytest tests/test_india_sizes_image.py -v
```

**Run tests with coverage report:**
```bash
pytest tests/ --cov=src --cov-report=term-missing
```

**Run a specific test function:**
```bash
pytest tests/test_door_image.py::test_door_image_extraction -v
```

### Test Requirements

Install test dependencies:
```bash
pip install pytest pytest-cov
```

Note: Tests use mocked EasyOCR responses to avoid actual image processing during testing, making them fast and reliable.

## Development

This project follows Python best practices:
- PEP 8 style guide
- Type hints where appropriate
- Comprehensive unit tests
- Clear documentation
- Uses OpenCV for Gaussian Thresholding to handle varied lighting in images.

## License

This project is licensed under the Apache License, Version 2.0 - see the [LICENSE.md](LICENSE.md) file for details

## Happy Contributing
