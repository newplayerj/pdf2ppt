from typing import Dict, Any, List, Tuple
import logging
import os
import fitz  # PyMuPDF
from src.figure_extractor import FigureExtractor
from src.content_analyzer import ContentAnalyzer

logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self):
        """Initialize document processor with its components."""
        self.figure_extractor = FigureExtractor()
        self.content_analyzer = ContentAnalyzer()

    def _extract_text(self, pdf_path: str) -> str:
        """Extract text content from PDF."""
        try:
            text_content = ""
            with fitz.open(pdf_path) as doc:
                for page in doc:
                    text_content += page.get_text()
            return text_content
        except Exception as e:
            logger.error(f"Error extracting text: {str(e)}")
            raise

    def process_document(self, input_path: str) -> Tuple[dict, List[str]]:
        """Process document and return analyzed content and figure paths."""
        try:
            # Extract text content
            text_content = self._extract_text(input_path)
            
            # Extract figures first
            figures = self.figure_extractor.extract_figures(input_path)
            if not figures:
                logger.warning("No figures were extracted from the document")
            
            # Analyze content
            analyzed_content = self.content_analyzer.analyze_content(text_content)
            
            return analyzed_content, figures
            
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            raise
