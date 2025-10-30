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

## Prerequisites

- **Python 3.11.9** (recommended) or Python 3.10.x
- **Tesseract OCR** installed on your system
- **Google Maps API Key**
- **Windows 10/11** (or adapt commands for macOS/Linux)
- **Visual Studio Code** (recommended)
- **Internet connection** (for downloading models on first run)


