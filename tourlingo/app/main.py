from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from PIL import Image
import io
import os
from dotenv import load_dotenv

from app.utils.translator import IndicTranslator
from app.utils.ner_extractor import TravelNER
from app.utils.ocr_processor import OCRProcessor
from app.utils.maps_helper import GoogleMapsHelper

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize components
print("Initializing Tourlingo components...")
translator = IndicTranslator()
ner_extractor = TravelNER()
ocr_processor = OCRProcessor()
maps_helper = GoogleMapsHelper(api_key=os.getenv('GOOGLE_MAPS_API_KEY'))
print("Initialization complete!")

@app.route('/')
def home():
    """Home page"""
    return render_template('index.html')

@app.route('/api/translate', methods=['POST'])
def translate_text():
    """
    Translate text between languages
    
    Request JSON:
    {
        "text": "Hello, where is the nearest restaurant?",
        "source_lang": "english",
        "target_lang": "hindi"
    }
    """
    try:
        data = request.json
        text = data.get('text')
        source_lang = data.get('source_lang', 'english')
        target_lang = data.get('target_lang', 'hindi')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        translation = translator.translate(text, source_lang, target_lang)
        
        return jsonify({
            'original': text,
            'translation': translation,
            'source_lang': source_lang,
            'target_lang': target_lang
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/extract-entities', methods=['POST'])
def extract_entities():
    """
    Extract travel-related entities from text
    
    Request JSON:
    {
        "text": "I want to visit the Taj Mahal in Agra and then go to the Red Fort"
    }
    """
    try:
        data = request.json
        text = data.get('text')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        entities = ner_extractor.extract_entities(text)
        
        return jsonify({
            'text': text,
            'entities': entities
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ocr', methods=['POST'])
def process_image():
    """
    Extract text from uploaded image
    
    Form data:
    - image: Image file
    - languages: Comma-separated language codes (optional)
    """
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        image_file = request.files['image']
        languages = request.form.get('languages', 'english,hindi').split(',')
        
        # Load image
        image = Image.open(image_file.stream)
        
        # Extract text
        extracted_texts = ocr_processor.extract_text(image, languages)
        
        return jsonify({
            'extracted_texts': extracted_texts,
            'languages': languages
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/travel-assist', methods=['POST'])
def travel_assist():
    """
    Complete travel assistance pipeline:
    1. Extract entities from query
    2. Translate if needed
    3. Get location suggestions
    
    Request JSON:
    {
        "text": "Where can I find good restaurants near India Gate?",
        "target_lang": "hindi",
        "include_suggestions": true
    }
    """
    try:
        data = request.json
        text = data.get('text')
        target_lang = data.get('target_lang')
        include_suggestions = data.get('include_suggestions', True)
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        response = {
            'original_text': text
        }
        
        # Extract entities
        entities = ner_extractor.extract_entities(text)
        response['entities'] = entities
        
        # Translate if requested
        if target_lang and target_lang != 'english':
            translation = translator.translate(text, 'english', target_lang)
            response['translation'] = translation
        
        # Get location suggestions
        if include_suggestions:
            locations = ner_extractor.extract_locations_for_maps(text)
            suggestions = []
            
            for location in locations[:3]:  # Limit to 3 locations
                places = maps_helper.search_places(location)
                if places:
                    suggestions.append({
                        'query': location,
                        'places': places
                    })
            
            response['suggestions'] = suggestions
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/image-assist', methods=['POST'])
def image_assist():
    """
    Process image: OCR + Translation + Entity extraction
    
    Form data:
    - image: Image file
    - target_lang: Target language for translation
    """
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        image_file = request.files['image']
        target_lang = request.form.get('target_lang', 'english')
        
        # Load image
        image = Image.open(image_file.stream)
        
        # Detect language and extract text
        detected_lang = ocr_processor.detect_language(image)
        extracted_texts = ocr_processor.extract_text(
            image, 
            languages=['english', detected_lang]
        )
        
        # Process the extracted text
        primary_text = extracted_texts.get('english') or extracted_texts.get(detected_lang)
        
        if not primary_text:
            return jsonify({'error': 'No text detected in image'}), 400
        
        # Extract entities
        entities = ner_extractor.extract_entities(primary_text)
        
        # Translate if needed
        translation = None
        if target_lang != 'english':
            translation = translator.translate(primary_text, 'english', target_lang)
        
        return jsonify({
            'detected_language': detected_lang,
            'extracted_text': primary_text,
            'translation': translation,
            'entities': entities
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
