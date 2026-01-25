# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-01-25

### Added
- Initial project setup with proper Python project structure
- EasyOCR integration for text extraction from images
- Confidence threshold filtering (50% minimum) to exclude ambiguous text recognition
- Translation support using deep-translator (Google Translate)
- Multi-language translation capability with language code parameter
- Command-line interface for image processing
- Git repository initialization with proper .gitignore for Python projects
- Project metadata in pyproject.toml
- Basic test structure with pytest support
- README.md with project documentation

### Features
- Extract text from images using OCR
- Filter results by confidence score (>= 50%)
- Translate extracted text to multiple languages
- Support for common languages: Spanish (es), French (fr), German (de), Hindi (hi), Chinese (zh-CN), Japanese (ja), Arabic (ar)
- Clean output format without position coordinates and confidence scores

### Dependencies
- easyocr: OCR text extraction
- deep-translator: Text translation functionality

### Usage
```bash
# Extract text only
python src/main.py image.jpg

# Extract and translate to target language
python src/main.py image.jpg <language_code>
```

## [Unreleased]

### Planned
- Support for batch image processing
- Output to file option
- Additional OCR language support
- Custom confidence threshold parameter
- GUI interface
