import logging
from src.document_processor import DocumentProcessor
from src.content_analyzer import ContentAnalyzer
from src.presentation_generator import PresentationGenerator
import os

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    try:
        # Initialize components
        document_processor = DocumentProcessor()
        content_analyzer = ContentAnalyzer()
        
        # Get input path from user
        input_path = input("Enter PDF path or URL: ")
        
        # Create output path
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        output_filename = os.path.splitext(os.path.basename(input_path))[0] + "_presentation.pptx"
        output_path = os.path.join(output_dir, output_filename)
        
        # Initialize presentation generator with output path
        presentation_generator = PresentationGenerator(output_path)
        
        # Process document
        content, figures = document_processor.process_document(input_path)
        
        # Analyze content
        analyzed_content = content_analyzer.analyze_content(content)
        
        # Generate presentation
        presentation = presentation_generator.generate(analyzed_content, figures)
        
        logger.info(f"Presentation generated successfully at {output_path}")
        
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")
        raise

if __name__ == "__main__":
    main()
