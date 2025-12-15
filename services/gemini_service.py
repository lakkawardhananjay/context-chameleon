
import json
import io
from typing import Dict, Any, Optional
from PIL import Image
import google.generativeai as genai

from config.settings import Settings
from config.prompts import GEMINI_ANALYSIS_PROMPT


class GeminiService:
    """Service for interacting with Google Gemini API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(Settings.GEMINI_MODEL)
    
    def analyze_image(self, image: Image.Image) -> Optional[Dict[str, Any]]:
        """
        Analyze image using Gemini and return structured JSON description
        
        Args:
            image: PIL Image object to analyze
            
        Returns:
            Dictionary containing structured image analysis or None on error
        """
        try:
            # Convert image to bytes
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            buffered.seek(0)
            
            # Send to Gemini
            response = self.model.generate_content([
                GEMINI_ANALYSIS_PROMPT,
                image
            ])
            
            # Parse JSON response
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            response_text = self._clean_json_response(response_text)
            
            analysis = json.loads(response_text)
            return analysis
            
        except Exception as e:
            raise Exception(f"Gemini Analysis Error: {str(e)}")
    
    @staticmethod
    def _clean_json_response(text: str) -> str:
        """Remove markdown formatting from JSON response"""
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()

