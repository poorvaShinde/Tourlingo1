import pytesseract
from PIL import Image
import cv2
import numpy as np
from typing import Dict, Tuple

class OCRProcessor:
    def __init__(self):
        """Initialize OCR processor with language support"""
        # IndicTrans2 supported languages mapped to Tesseract codes
        self.lang_map = {
            'hindi': 'hin',
            'marathi': 'mar',
            'tamil': 'tam',
            'telugu': 'tel',
            'bengali': 'ben',
            'gujarati': 'guj',
            'kannada': 'kan',
            'malayalam': 'mal',
            'english': 'eng'
        }
    
    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """
        Preprocess image for better OCR accuracy
        
        Steps:
        1. Convert to grayscale
        2. Apply thresholding
        3. Denoise
        """
        # Convert PIL Image to numpy array
        img_array = np.array(image)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
        
        return denoised
    
    def extract_text(self, image: Image.Image, languages: List[str] = None) -> Dict[str, str]:
        """
        Extract text from image in multiple languages
        
        Args:
            image: PIL Image object
            languages: List of language names (e.g., ['english', 'hindi'])
        
        Returns:
            Dict with extracted text for each language
        """
        if languages is None:
            languages = ['english', 'hindi']
        
        # Preprocess image
        processed_img = self.preprocess_image(image)
        
        results = {}
        
        for lang in languages:
            tesseract_lang = self.lang_map.get(lang.lower(), 'eng')
            
            try:
                # Extract text
                text = pytesseract.image_to_string(
                    processed_img,
                    lang=tesseract_lang,
                    config='--psm 6'  # Assume uniform block of text
                )
                
                results[lang] = text.strip()
                
            except Exception as e:
                print(f"OCR error for {lang}: {e}")
                results[lang] = ""
        
        return results
    
    def detect_language(self, image: Image.Image) -> str:
        """
        Detect primary language in image using OSD (Orientation and Script Detection)
        """
        try:
            osd_data = pytesseract.image_to_osd(image)
            # Parse script information
            for line in osd_data.split('\n'):
                if 'Script:' in line:
                    script = line.split(':')[1].strip()
                    return self._script_to_language(script)
        except:
            pass
        
        return 'english'  # Default
    
    def _script_to_language(self, script: str) -> str:
        """Map detected script to language"""
        script_map = {
            'Devanagari': 'hindi',
            'Latin': 'english',
            'Tamil': 'tamil',
            'Telugu': 'telugu',
            'Bengali': 'bengali'
        }
        return script_map.get(script, 'english')
