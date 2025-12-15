

def get_custom_css() -> str:
    """Return custom CSS for the application"""
    return """
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .vibe-card {
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        background: white;
        height: 100%;
    }
    .vibe-card:hover {
        border-color: #667eea;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
        transform: translateY(-2px);
    }
    .vibe-card-selected {
        border: 3px solid #667eea;
        background: linear-gradient(135deg, #667eea10 0%, #764ba210 100%);
    }
    .vibe-emoji {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    .vibe-title {
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: #333;
    }
    .vibe-description {
        font-size: 0.9rem;
        color: #666;
    }
    .tech-section {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 15px;
        margin: 20px 0;
        border-radius: 8px;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.2rem;
        font-weight: bold;
        padding: 0.75rem 2rem;
        border: none;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
</style>
"""


