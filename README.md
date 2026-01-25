# Python Project

A Python project to extract the content of input image and translate the text in requested language.

## Project Structure

```
.
├── src/              # Source code
├── tests/            # Test files
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
   pip install -e .
   ```

## Usage

Run the main application:
1. Extract the content in image without translation (English)
   ```bash
   python src/main.py <image_path>
   ```
2. Extract the content in image with translation (Hindi(hi), German(de), French(fr), etc.)
   ```bash
   python src/main.py <image_path> <hi/en/fr/de/..>
   ```
   
## Testing

Run tests:
- TBD

## Development

This project follows Python best practices:
- PEP 8 style guide
- Type hints where appropriate
- Comprehensive unit tests
- Clear documentation

## License

This project is licensed under the Apache License, Version 2.0 - see the [LICENSE.md](LICENSE.md) file for details
