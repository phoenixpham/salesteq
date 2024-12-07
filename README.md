# PDF Metadata Extraction and Storage with Qdrant

## Project Overview
This project implements a Python script to extract and store metadata from PDFs using Qdrant vector store. It enables efficient semantic search and supports the following functionalities:
- **Text Extraction:** Captures text with page and paragraph metadata
- **Table Extraction**: Identifies and preserves table structure
- **Image Extraction**: Uses OCR to generate meaningful descriptions of images
- **Semantic Search** Leverages vector embeddings for retrieval-augmented queries

## Requirements
- Python 3.8+
- Qdrant Vector Database: ensure Qdrant is running locally
- Tesseract OCR: required for image processing

### Python Dependencies
Install the required packages:
```bash
pip install pymupdf pytesseract pillow qdrant-client sentence-transformers numpy pdfplumber
```

### Tesseract Installation
- Ubuntu/Debian: `sudo apt-get install tesseract-ocr`
- macOS: `brew install tesseract`
- Windows: Download from Tesseract GitHub repository

## Setup and Configuration
1. Ensure Qdrant is running locally (default: localhost:6333)
2. Place the PDF file (e.g. `Algorithms_and_Flowcharts.pdf`) in the same directory as the script
3. Modify `pdf_path` in `main()` if using a different file (Optional)

## Features
- Extracts text from PDF and stores it with with page and paragraph metadata
- Identifies and extracts table-like content while maintaining rows and columns
- Performs OCR on images to generate descriptions and embedded images
- Stores all metadata in Qdrant vector store for efficient querying
- Supports semantic search across extracted content using vector embeddings

## Results
### Extracted Metadata
After running the script on `Algorithms_and_Flowcharts.pdf`, the following metadata was stored in Qdrant:
1. **Text Metadata**
   - Example Text Extracted:
     ```json
     {
       "text": "A flowchart shows diagrammatically the steps required to complete a task and the order that they are to be performed.",
       "page": 2,
       "paragraph": 2
     }
     ```
2. **Table Metadata**
   - Example Text Extracted:
     ```json
     {
       "table": [
         ["Operator", "Description"],
         ["+", "Addition"],
         ["-", "Subtraction"],
         ["*", "Multiplication"],
         ["/", "Division"]
         ["^", "Power of"],
         ["MOD", "Modulus division (gives the remainder)"],
         ["DIV", "Integer division (gives the whole number)"]
       ],
       "description": "Table 1 on page 5",
       "page": 5
     }
     ```
3. **Image Metadata**
   - Example Text Extracted:
     ```json
     {
       "description": "Image 2 on page 7",
       "page": 7,
       "image_index": 2
     }
     ```

## Query Examples
The following queries were tested after storing metadata in Qdrant:
1. `"What are flowcharts?"`
   - Response:
   ```css
   A flowchart shows diagrammatically the steps required to complete a task.
   ```
2. `"What are the types of loops described?"`
   - Response:
   ```css
   Types of loops: Count-controlled loop, Condition-controlled loop.
   ```
3. `"Describe the operators in the document."`
   - Response:
   ```css
   Addition (+), Subtraction (-), Multiplication (*), Division (/), Power of (^), Modulus division (MOD), Integer division (DIV).
   ```

## Challenges and Limitations
- Table extraction is basic and may require more sophisticated libraries for complex table layouts
- Image description relies on OCR, which can be imperfect, especially for non-textual images like diagrams
- Requires Tesseract OCR for image processing

## Potential Improvements
- Implement more advanced table detection and extraction using specialized libraries
- Use a more sophisticated model for image descriptions
- Add support for more complex PDF structures
- Add a simple web interface for uploading PDFs and querying metadata

## Submission Details
- Submitted by: Phoenix Pham
- Submission Date: 12/7/2024
- Contact: phoenixpham@berkeley.edu
