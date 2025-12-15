
import streamlit as st
from typing import Dict, List, Any, Optional
from PIL import Image


class SessionState:
    """Manages Streamlit session state"""
    
    @staticmethod
    def initialize():
        """Initialize all session state variables"""
        if "selected_vibes" not in st.session_state:
            st.session_state.selected_vibes = []
        
        if "generated_images" not in st.session_state:
            st.session_state.generated_images = {}
        
        if "uploaded_image" not in st.session_state:
            st.session_state.uploaded_image = None
        
        if "image_analysis" not in st.session_state:
            st.session_state.image_analysis = None
    
    @staticmethod
    def set_uploaded_image(image: Optional[Image.Image]):
        """Set the uploaded image in session state"""
        st.session_state.uploaded_image = image
    
    @staticmethod
    def get_uploaded_image() -> Optional[Image.Image]:
        """Get the uploaded image from session state"""
        return st.session_state.uploaded_image
    
    @staticmethod
    def set_image_analysis(analysis: Optional[Dict[str, Any]]):
        """Set image analysis results"""
        st.session_state.image_analysis = analysis
    
    @staticmethod
    def get_image_analysis() -> Optional[Dict[str, Any]]:
        """Get image analysis results"""
        return st.session_state.image_analysis
    
    @staticmethod
    def add_generated_image(vibe_name: str, image: Image.Image):
        """Add a generated image to session state"""
        st.session_state.generated_images[vibe_name] = image
    
    @staticmethod
    def get_generated_images() -> Dict[str, Image.Image]:
        """Get all generated images"""
        return st.session_state.generated_images
    
    @staticmethod
    def clear_generated_images():
        """Clear all generated images"""
        st.session_state.generated_images = {}
