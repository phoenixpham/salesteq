import os
import re
import json
from typing import List, Dict, Any

import fitz  # PyMuPDF for PDF processing
import pytesseract  # OCR
from PIL import Image
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import numpy as np
from sentence_transformers import SentenceTransformer

class PDFMetadataExtractor:
    def __init__(self, pdf_path: str, qdrant_host: str = 'localhost', qdrant_port: int = 6333):
        """
        Initialize PDF Metadata Extractor with Qdrant vector store
        
        :param pdf_path: Path to the PDF file
        :param qdrant_host: Qdrant server host
        :param qdrant_port: Qdrant server port
        """
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
        
        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(host=qdrant_host, port=qdrant_port)
        
        # Collection name
        self.collection_name = "pdf_metadata_collection"
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Create collection if not exists
        self.create_qdrant_collection()
    
    def create_qdrant_collection(self):
        """
        Create Qdrant collection for storing PDF metadata
        """
        try:
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
        except:
            # Collection might already exist
            pass
    
    def extract_text_with_metadata(self) -> List[Dict[str, Any]]:
        """
        Extract text from PDF with metadata
        
        :return: List of dictionaries containing text and metadata
        """
        text_metadata = []
        for page_num, page in enumerate(self.doc, 1):
            text = page.get_text()
            paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
            
            for para_num, paragraph in enumerate(paragraphs, 1):
                text_metadata.append({
                    'text': paragraph,
                    'page': page_num,
                    'paragraph': para_num
                })
        
        return text_metadata
    
    def extract_tables(self) -> List[Dict[str, Any]]:
        """
        Extract tables from PDF (Note: Basic extraction, might need more advanced library)
        
        :return: List of dictionaries containing table data
        """
        tables = []
        for page_num, page in enumerate(self.doc, 1):
            # This is a basic approach and might need more sophisticated table detection
            text = page.get_text()
            potential_tables = [
                block for block in text.split('\n\n') 
                if '|' in block or '\t' in block
            ]
            
            for table_num, table_text in enumerate(potential_tables, 1):
                tables.append({
                    'table': table_text,
                    'description': f'Table {table_num} on page {page_num}',
                    'page': page_num
                })
        
        return tables
    
    def extract_images(self) -> List[Dict[str, Any]]:
        """
        Extract images from PDF
        
        :return: List of dictionaries containing image metadata and descriptions
        """
        images = []
        for page_num, page in enumerate(self.doc, 1):
            image_list = page.get_images(full=True)
            
            for img_index, img_info in enumerate(image_list, 1):
                xref = img_info[0]
                base_image = self.doc.extract_image(xref)
                image_bytes = base_image["image"]
                
                # Use pytesseract to get image description
                pil_image = Image.open(BytesIO(image_bytes))
                description = pytesseract.image_to_string(pil_image)
                
                images.append({
                    'description': description.strip() or f'Image {img_index} on page {page_num}',
                    'page': page_num,
                    'image_index': img_index
                })
        
        return images
    
    def store_in_qdrant(self, data: List[Dict[str, Any]]):
        """
        Store extracted metadata in Qdrant vector store
        
        :param data: List of metadata dictionaries
        """
        points = []
        for idx, item in enumerate(data):
            # Generate embedding
            if 'text' in item:
                embedding = self.embedding_model.encode(item['text']).tolist()
            elif 'description' in item:
                embedding = self.embedding_model.encode(item['description']).tolist()
            else:
                continue
            
            points.append(
                PointStruct(
                    id=idx,
                    vector=embedding,
                    payload=item
                )
            )
        
        # Upsert points into Qdrant
        self.qdrant_client.upsert(
            collection_name=self.collection_name,
            points=points
        )
    
    def query_qdrant(self, query: str, top_k: int = 5):
        """
        Query Qdrant vector store
        
        :param query: Search query
        :param top_k: Number of top results to return
        :return: List of query results
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Search in Qdrant
        search_result = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k
        )
        
        return [result.payload for result in search_result]
    
    def process_pdf(self):
        """
        Main method to process PDF and store metadata
        """
        # Extract and store text metadata
        text_metadata = self.extract_text_with_metadata()
        self.store_in_qdrant(text_metadata)
        
        # Extract and store table metadata
        table_metadata = self.extract_tables()
        self.store_in_qdrant(table_metadata)
        
        # Extract and store image metadata
        image_metadata = self.extract_images()
        self.store_in_qdrant(image_metadata)
        
        print("PDF metadata extraction and storage completed.")

def main():
    # Path to the PDF
    pdf_path = 'Algorithms_and_Flowcharts.pdf'
    
    # Create extractor
    extractor = PDFMetadataExtractor(pdf_path)
    
    # Process PDF
    extractor.process_pdf()
    
    # Example query
    query = "What are flowcharts?"
    results = extractor.query_qdrant(query)
    
    print("\nQuery Results:")
    for result in results:
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()