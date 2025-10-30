# 🌍 Tourlingo - Multilingual Travel Assistant

**Tourlingo** is a Flask-based web application that helps travelers by providing real-time translation, location extraction, and travel recommendations across multiple Indian languages.

## Features

- **Multilingual Translation**: Translate English text to Hindi, Marathi, Tamil, and Telugu using AI4Bharat's IndicTrans2 model
- **Location Recognition**: Automatically extract locations, attractions, and organizations from text using spaCy NER
- **Smart Recommendations**: Get place suggestions powered by Google Maps API
- **Modern UI**: Clean, responsive interface with smooth animations
- **Real-time Processing**: Fast translation and entity extraction

## Tech Stack

- **Backend**: Flask 3.0.0, Python 3.11
- **ML Models**: 
  - IndicTrans2 (AI4Bharat) for translation
  - spaCy en_core_web_md for Named Entity Recognition
  - PyTorch for model inference
- **APIs**: Google Maps Places API
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **OCR**: Tesseract (for future image text extraction)

## Project Structure
```
tourlingo/
├── app/
│ ├── main.py
│ ├── init.py
│ ├── templates/
│ │ └── index.html
│ ├── static/
│ └── utils/
│ ├── init.py
│ ├── translator.py
│ ├── ner_extractor.py
│ └── maps_helper.py
├── data/
├── venv/
├── .env
├── requirements.txt
└── README.md
```
