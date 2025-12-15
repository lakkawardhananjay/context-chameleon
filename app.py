import streamlit as st
import time
from PIL import Image
import os

from config.settings import Settings
from services.gemini_service import GeminiService
from services.bria_service import BriaService
from services.image_service import ImageService
from ui.styles import get_custom_css
from ui.components import UIComponents

from utils.session_state import SessionState

# Page Configuration
st.set_page_config(
    page_title=Settings.PAGE_TITLE,
    page_icon="🎨",
    layout=Settings.PAGE_LAYOUT,
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Initialize session state
SessionState.initialize()


def analyze_image_handler(image: Image.Image, gemini_key: str):
    """Handle image analysis"""
    with st.spinner("🔍 Analyzing image with Gemini AI..."):
        try:
            gemini_service = GeminiService(gemini_key)
            analysis = gemini_service.analyze_image(image)
            SessionState.set_image_analysis(analysis)
            st.success("✅ Image analysis complete!")
            st.rerun()
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")


def generate_assets_handler(
    image: Image.Image,
    selected_vibes: list,
    gemini_key: str,
    bria_key: str,
    vibe_configs: dict = {}
):
    """
    Handle asset generation
    vibe_configs: Dictionary containing specific settings per vibe 
    (e.g., {'Marketplace Clean': {'camera_angle': 'low_angle'}, 
            'Consumption/Active': {'scenario_id': 'hand_holding'}})
    """
    st.markdown("### 🎬 Generating Your Marketing Assets...")

    progress_bar = st.progress(0)
    status_text = st.empty()

    for idx, vibe_name in enumerate(selected_vibes):
        # Fetch emoji safely
        from config.vibe_configs import VIBE_CONFIGS
        emoji = VIBE_CONFIGS.get(vibe_name, {}).get("emoji", "✨")
        
        status_text.markdown(f"**Processing:** {vibe_name} {emoji}")

        try:
            analysis = SessionState.get_image_analysis()
            if not analysis:
                st.error("Image analysis required. Please analyze the image first.")
                continue

            # Extract specific config for this vibe if available
            specific_config = vibe_configs.get(vibe_name, {})

            with st.spinner(f"🤖 Generating {vibe_name} with Bria FIBO..."):
                bria_service = BriaService(bria_key)
                
                # Pass vibe config (which may contain scenario_id for Consumption/Active)
                generated_image = bria_service.generate_image(
                    image, 
                    vibe_name, 
                    analysis,
                    specific_config=specific_config  # Pass specific config for the vibe
                )

                if generated_image:
                    SessionState.add_generated_image(vibe_name, generated_image)
                else:
                    st.error(f"Failed to generate {vibe_name}")

        except Exception as e:
            st.error(f"Error generating {vibe_name}: {str(e)}")
            import traceback
            st.error(traceback.format_exc())

        progress_bar.progress((idx + 1) / len(selected_vibes))

    status_text.markdown("**✅ Generation Complete!**")
    time.sleep(0.5)
    progress_bar.empty()
    status_text.empty()

    st.success("🎉 All marketing assets generated successfully!")
    st.balloons()


def main():
    """Main application entry point"""

    gemini_key = os.environ.get("GEMINI_API_KEY")
    bria_key = os.environ.get("BRIA_API_KEY")

    if not gemini_key:
        st.error("GEMINI_API_KEY not found in environment variables. Please set it in the .env file.")
        st.stop()
    if not bria_key:
        st.error("BRIA_API_KEY not found in environment variables. Please set it in the .env file.")
        st.stop()

    # Render header
    UIComponents.render_header()

    # Upload section
    uploaded_image = UIComponents.render_upload_section()

    if uploaded_image is not None:
        SessionState.set_uploaded_image(uploaded_image)

        # Analysis section
        if gemini_key:
            st.markdown("---")
            UIComponents.render_analysis_section(
                uploaded_image,
                SessionState.get_image_analysis(),
                on_analyze_callback=lambda: analyze_image_handler(uploaded_image, gemini_key),
                on_reanalyze_callback=lambda: analyze_image_handler(uploaded_image, gemini_key)
            )

        st.markdown("---")

        # Get selected vibes and configs using existing method
        analysis_data = SessionState.get_image_analysis()
        selected_vibes, vibe_configs = UIComponents.render_vibe_selection_and_config(analysis_data)
        
        # Debug: Show what was selected
        with st.expander("🔍 Debug Selection", expanded=False):
            st.write(f"Selected vibes: {selected_vibes}")
            st.write(f"Vibe configs: {vibe_configs}")
            
            # If Consumption is selected, show scenario info
            if "Consumption/Active" in selected_vibes:
                scenario_id = vibe_configs.get("Consumption/Active", {}).get("scenario_id")
                if scenario_id:
                    st.write(f"Selected scenario ID: {scenario_id}")

        # Technical details
        UIComponents.render_technical_details(selected_vibes, vibe_configs)

        # Generation button
        if selected_vibes:
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🚀 Generate Campaign Assets", use_container_width=True, type="primary"):
                    # For Consumption vibe, check if scenario is selected
                    if "Consumption/Active" in selected_vibes:
                        scenario_id = vibe_configs.get("Consumption/Active", {}).get("scenario_id")
                        if not scenario_id:
                            st.warning("⚠️ Please select a scenario for the Consumption/Active vibe")
                            st.stop()
                    
                    generate_assets_handler(
                        image=uploaded_image,
                        selected_vibes=selected_vibes,
                        gemini_key=gemini_key,
                        bria_key=bria_key,
                        vibe_configs=vibe_configs
                    )
                        
            # Display results
            UIComponents.render_generation_results(SessionState.get_generated_images())
        else:
            if uploaded_image:
                st.info("👆 Select at least one marketing vibe to begin generation")

    else:
        # Placeholder content
        UIComponents.render_placeholder_content()

    # Footer
    UIComponents.render_footer()


if __name__ == "__main__":
    main()