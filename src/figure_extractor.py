import cv2
import fitz  # PyMuPDF
import numpy as np
import os
import logging
from typing import List
from PIL import Image

logger = logging.getLogger(__name__)

class FigureExtractor:
    def __init__(self):
        """Initialize figure extractor."""
        logger.info(f"Using OpenCV version: {cv2.__version__}")
        self.output_dir = "output/figures"
        os.makedirs(self.output_dir, exist_ok=True)

    def _save_figure(self, image: np.ndarray, index: int) -> str:
        """Save figure to file and return the file path."""
        output_path = os.path.join(self.output_dir, f"figure_{index}.png")
        try:
            cv2.imwrite(output_path, image)
            return output_path
        except Exception as e:
            logger.error(f"Error saving figure {index}: {str(e)}")
            return None

    def _is_valid_figure(self, image: np.ndarray) -> bool:
        """Check if the image is a valid figure."""
        if image is None:
            return False
            
        # Add minimum size requirements
        min_width = 100
        min_height = 100
        height, width = image.shape[:2]
        
        if width < min_width or height < min_height:
            return False
            
        # Add basic image quality check
        if image.mean() < 10 or image.mean() > 245:  # Too dark or too bright
            return False
            
        return True

    def extract_figures(self, pdf_path: str) -> List[str]:
        """Extract figures from PDF and return list of saved figure paths."""
        try:
            doc = fitz.open(pdf_path)
            figure_paths = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                image_list = page.get_images(full=True)
                
                for img_index, img_info in enumerate(image_list):
                    try:
                        xref = img_info[0]
                        base_image = doc.extract_image(xref)
                        
                        if not base_image or "image" not in base_image:
                            continue
                            
                        image_bytes = base_image["image"]
                        nparr = np.frombuffer(image_bytes, np.uint8)
                        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                        
                        if image is not None and self._is_valid_figure(image):
                            figure_index = len(figure_paths) + 1
                            figure_path = self._save_figure(image, figure_index)
                            
                            if figure_path:
                                figure_paths.append(figure_path)
                                logger.debug(f"Saved figure {figure_index} from page {page_num + 1}")
                    
                    except Exception as e:
                        logger.warning(f"Failed to process image {img_index} on page {page_num}: {str(e)}")
                        continue
            
            logger.info(f"Extracted {len(figure_paths)} figures")
            return figure_paths
            
        except Exception as e:
            logger.error(f"Error extracting figures: {str(e)}")
            raise
        finally:
            if 'doc' in locals():
                doc.close()
