# PDF Metadata Extraction and Storage with Qdrant

## Project Overview
This project implements a Python script to extract and store metadata from PDFs using Qdrant vector store. The solution supports:
- Text extraction with page and paragraph metadata
- Table detection and extraction
- Image extraction with OCR-based descriptions
- Semantic search using vector embeddings

## Requirements
- Python 3.8+
- Qdrant Vector Database
- Tesseract OCR

### Python Dependencies
Install the required packages:
```bash
pip install pymupdf pytesseract pillow pandas qdrant-client sentence-transformers numpy
```

### Tesseract Installation
- Ubuntu/Debian: `sudo apt-get install tesseract-ocr`
- macOS: `brew install tesseract`
- Windows: Download from official Tesseract GitHub repository

## Setup and Configuration
1. Ensure Qdrant is running locally (default: localhost:6333)
2. Place your PDF in the same directory as the script
3. Modify `pdf_path` in `main()` if needed

## Features
- Extracts text with page and paragraph metadata
- Identifies and extracts table-like content
- Performs OCR on images to generate descriptions
- Stores metadata in Qdrant vector store
- Supports semantic search across extracted content

## Example Usage
```python
# Create extractor
extractor = PDFMetadataExtractor('your_pdf.pdf')

# Process PDF and store metadata
extractor.process_pdf()

# Perform semantic search
results = extractor.query_qdrant("What are flowcharts?")
```

## Challenges and Limitations
- Table extraction is basic and may require more sophisticated libraries
- Image description relies on OCR, which can be imperfect
- Requires Tesseract OCR for image processing

## Potential Improvements
- Implement more advanced table detection
- Enhance image description accuracy
- Add support for more complex PDF structures

## Submission Details
- Submitted by: Phoenix Pham
- Submission Date: 12/7/2024
- Contact: phoenixpham@berkeley.edu
