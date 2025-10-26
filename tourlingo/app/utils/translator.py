import os
import sys
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class IndicTranslator:
    def __init__(self, model_dir="models/indictrans2"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_dir = model_dir
        
        # Language codes for IndicTrans2
        self.lang_codes = {
            'hindi': 'hin_Deva',
            'marathi': 'mar_Deva',
            'tamil': 'tam_Taml',
            'telugu': 'tel_Telu',
            'bengali': 'ben_Beng',
            'gujarati': 'guj_Gujr',
            'kannada': 'kan_Knda',
            'malayalam': 'mal_Mlym',
            'punjabi': 'pan_Guru',
            'urdu': 'urd_Arab',
            'english': 'eng_Latn'
        }
        
        self.load_model()
    
    def load_model(self):
        """Load IndicTrans2 model"""
        try:
            # Use distilled model for faster inference
            model_name = "ai4bharat/indictrans2-en-indic-dist-200M"
            
            print(f"Loading model on {self.device}...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                trust_remote_code=True
            )
            self.model = AutoModelForSeq2SeqLM.from_pretrained(
                model_name,
                trust_remote_code=True
            ).to(self.device)
            
            print("Model loaded successfully!")
            
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    def translate(self, text, source_lang='english', target_lang='hindi'):
        """
        Translate text from source to target language
        
        Args:
            text: Input text to translate
            source_lang: Source language name
            target_lang: Target language name
        
        Returns:
            Translated text
        """
        try:
            src_code = self.lang_codes.get(source_lang.lower(), 'eng_Latn')
            tgt_code = self.lang_codes.get(target_lang.lower(), 'hin_Deva')
            
            # Prepare input
            input_text = f"{src_code} {text}"
            
            inputs = self.tokenizer(
                input_text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            ).to(self.device)
            
            # Generate translation
            with torch.no_grad():
                generated_tokens = self.model.generate(
                    **inputs,
                    forced_bos_token_id=self.tokenizer.convert_tokens_to_ids(tgt_code),
                    max_length=512,
                    num_beams=5,
                    num_return_sequences=1
                )
            
            # Decode output
            translation = self.tokenizer.batch_decode(
                generated_tokens,
                skip_special_tokens=True
            )[0]
            
            return translation
            
        except Exception as e:
            print(f"Translation error: {e}")
            return text
    
    def batch_translate(self, texts, source_lang='english', target_lang='hindi'):
        """Translate multiple texts efficiently"""
        return [self.translate(text, source_lang, target_lang) for text in texts]
