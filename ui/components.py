import streamlit as st
import json
from typing import Dict, Any, List, Optional, Tuple
from PIL import Image

# Config imports
from config.vibe_configs import VIBE_CONFIGS
# Ensure config/consumption_data.py exists as per previous instructions
try:
    from config.consumption_data import CONSUMPTION_SCENARIOS, SUBJECT_TO_SCENARIO_MAP
except ImportError:
    # Fallback to prevent crash if file missing, though functionality will be limited
    CONSUMPTION_SCENARIOS = {"default": []}
    SUBJECT_TO_SCENARIO_MAP = {}

# -----------------------------
# Asset Definitions
# -----------------------------
MARKETPLACE_CAMERA_ANGLES = [
    {"label": "Eye Level", "image_path": "assets/angles/eye_level.jpg", "value": "eye_level"},
    {"label": "Low Angle", "image_path": "assets/angles/low_angle.jpg", "value": "low_angle"},
    {"label": "High Angle", "image_path": "assets/angles/high_angle.jpg", "value": "high_angle"},
    {"label": "Bird's Eye", "image_path": "assets/angles/birds_eye.jpg", "value": "birds_eye"},
]

class UIComponents:
    """Reusable UI components for the application"""

    @staticmethod
    def render_header():
        st.markdown('<h1 class="main-header">Context Chameleon</h1>', unsafe_allow_html=True)
        st.markdown(
            '<p class="sub-header">Transform Your Product into Marketing Gold with AI-Powered Context Generation</p>',
            unsafe_allow_html=True
        )

    @staticmethod
    def render_upload_section() -> Optional[Image.Image]:
        """Render image upload section and return uploaded image"""
        st.markdown("### 📤 Upload Product Image")
        uploaded_file = st.file_uploader(
            "Choose a product image (PNG/JPG)",
            type=["png", "jpg", "jpeg"],
            help="Upload a clear product image with transparent or simple background for best results"
        )

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(image, caption="📦 Source Asset", use_container_width=True)
            return image

        return None

    @staticmethod
    def render_analysis_section(
            image: Image.Image,
            analysis: Dict[str, Any],
            on_analyze_callback,
            on_reanalyze_callback
    ):
        """Render image analysis section with controls"""
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if analysis is None:
                if st.button("🔍 Analyze Image with Gemini", use_container_width=True):
                    on_analyze_callback()
            else:
                if st.button("🔄 Re-analyze Image", use_container_width=True):
                    on_reanalyze_callback()

        if analysis:
            UIComponents._render_analysis_display(analysis)

    @staticmethod
    def _render_analysis_display(analysis: Dict[str, Any]):
        """Display analysis results"""
        with st.expander("🔬 View Gemini Image Analysis", expanded=False):
            st.json(analysis)

            st.markdown("### 📊 Key Insights")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Scene Type", analysis.get("scene_type", "unknown"))
            with col2:
                st.metric("Lighting", analysis.get("lighting", {}).get("type", "unknown"))
            with col3:
                confidence = analysis.get('metadata_confidence', 0)
                st.metric("Confidence", f"{confidence:.0%}")

            st.markdown("**Scene Description:**")
            st.write(analysis.get("global_description", "N/A"))

    @staticmethod
    def _get_consumption_scenarios(image_analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Determines which consumption scenarios to show based on Gemini analysis.
        """
        if not image_analysis or "subjects" not in image_analysis:
            return CONSUMPTION_SCENARIOS.get("default", [])

        product_desc = image_analysis["subjects"][0].get("detailed_description", "").lower()
        
        # Default to 'default' if no better match is found
        scenario_category = "default"

        # Find the best matching scenario category
        for keyword, category in SUBJECT_TO_SCENARIO_MAP.items():
            if keyword in product_desc:
                scenario_category = category
                break  # Stop at first match

        return CONSUMPTION_SCENARIOS.get(scenario_category, CONSUMPTION_SCENARIOS.get("default", []))
    # -------------------------------------------------------
    # NEW: Unified Vibe & Config Renderer
    # -------------------------------------------------------
    @staticmethod
    def render_vibe_selection_and_config(image_analysis: Dict[str, Any]) -> Tuple[List[str], Dict[str, Any]]:
        """
        Unified render function that handles Vibe Selection AND their specific configurations.
        Returns: (selected_vibes_list, configuration_dict)
        """
        st.markdown("### 🎨 Select Marketing Vibes")
        st.markdown("Select vibes to configure specific marketing contexts.")

        selected_vibes = []
        configurations = {}

        # --- 1. Marketplace Clean (Custom Block) ---
        with st.container():
            # Layout: Checkbox on left, Expander on right
            col_checkbox, col_content = st.columns([0.05, 0.95])
            with col_checkbox:
                # Spacer to align checkbox with expander header
                st.write("") 
                mp_selected = st.checkbox("Select Marketplace", key="vibe_check_marketplace", label_visibility="hidden")
            
            with col_content:
                # The expander state is tied to the checkbox
                with st.expander("🛒 Marketplace Clean", expanded=mp_selected):
                    st.caption("Pure white background, e-commerce standard.")
                    
                    if mp_selected:
                        selected_vibes.append("Marketplace Clean")
                        st.markdown("##### 🎥 Camera Angle")
                        # Use the Grid Selector
                        selected_angle = UIComponents._render_image_grid_selector(
                            options=MARKETPLACE_CAMERA_ANGLES,
                            key_prefix="mp_angle",
                            default_value="eye_level"
                        )
                        configurations["Marketplace Clean"] = {"camera_angle": selected_angle}
                    else:
                        st.info("Select the checkbox to enable configuration.")

        # --- 2. Consumption/Active (Custom Block) ---
        with st.container():
            col_checkbox, col_content = st.columns([0.05, 0.95])
            with col_checkbox:
                st.write("") 
                consumption_selected = st.checkbox("Select Consumption/Active", key="vibe_check_consumption", label_visibility="hidden")

            with col_content:
                with st.expander("🍔 Consumption/Active", expanded=consumption_selected):
                    st.caption("Show product in a real-world scenario.")
                    
                    if consumption_selected:
                        # This vibe requires analysis to be useful
                        if not image_analysis:
                            st.warning("Please analyze the image first to see relevant scenarios.")
                        else:
                            selected_vibes.append("Consumption/Active")
                            st.markdown("##### 🚶 Scenario")
                            
                            # Get scenarios dynamically based on analysis
                            scenarios = UIComponents._get_consumption_scenarios(image_analysis)
                            
                            # Adapt scenarios for the grid selector
                            scenario_options = [
                                {"label": s["label"], "image_path": s["image_path"], "value": s["id"]}
                                for s in scenarios
                            ]

                            # Get default value for the grid
                            default_scenario = scenario_options[0]['value'] if scenario_options else ""

                            selected_scenario = UIComponents._render_image_grid_selector(
                                options=scenario_options,
                                key_prefix="consumption_scenario",
                                default_value=default_scenario
                            )
                            configurations["Consumption/Active"] = {"scenario_id": selected_scenario}
                    else:
                        st.info("Select the checkbox to enable configuration.")



        # --- 4. Other Vibes (Generic Loop) ---
        # We exclude the ones we already manually rendered
        manual_vibes = ["Marketplace Clean", "Consumption/Active"]
        
        st.markdown("#### Additional Vibes")
        
        # Filter vibes to be rendered in the generic loop
        other_vibes = {
            name: data for name, data in VIBE_CONFIGS.items() 
            if name not in manual_vibes
        }

        cols = st.columns(3)
        for idx, (vibe_name, vibe_data) in enumerate(other_vibes.items()):
            col = cols[idx % 3]
            with col:
                is_selected = st.checkbox(
                    f"{vibe_data['emoji']} {vibe_name}",
                    key=f"vibe_{vibe_name}"
                )
                if is_selected:
                    selected_vibes.append(vibe_name)
                
                # Simple card description
                st.caption(vibe_data.get('description', ''))

        return selected_vibes, configurations

    @staticmethod
    def _render_image_grid_selector(options: List[Dict], key_prefix: str, default_value: str) -> str:
        """
        Reusable grid selector for images.
        Automatically uses a placeholder if the local image file is missing.
        """
        import os # Make sure to import os at top of file, or inside here

        ss_key = f"selected_{key_prefix}"
        
        # Initialize state
        if ss_key not in st.session_state and default_value:
            st.session_state[ss_key] = default_value

        cols = st.columns(4)
        for idx, option in enumerate(options):
            col = cols[idx % 4]
            with col:
                is_selected = st.session_state.get(ss_key) == option['value']
                
                # Check if local file exists
                image_to_show = option['image_path']
                if not os.path.exists(image_to_show):
                    # Use a web placeholder if local file is missing
                    # This ensures the Grid Layout stays "Big" and "Beautiful"
                    safe_label = option['label'].replace(" ", "+")
                    image_to_show = f"https://placehold.co/600x400/png?text={safe_label}"

                # Render Image
                st.image(image_to_show, use_container_width=True)

                # Selection Button
                if st.button(
                    f"{'✅ ' if is_selected else ''}{option['label']}", 
                    key=f"btn_{key_prefix}_{option['value']}",
                    use_container_width=True,
                    type="primary" if is_selected else "secondary"
                ):
                    st.session_state[ss_key] = option['value']
                    st.rerun()
        
        return st.session_state.get(ss_key)

    @staticmethod
    def render_technical_details(selected_vibes: List[str], vibe_configs: Dict[str, Any] = None):
        """Render technical payload details for selected vibes"""
        if not selected_vibes:
            return

        st.markdown("---")
        with st.expander("🔬 Under the Hood: API Payloads", expanded=False):
            st.markdown("See the exact technical parameters sent to the API.")

            for vibe_name in selected_vibes:
                st.markdown(f"**{vibe_name}**")
                
                # Get base payload
                if vibe_name in VIBE_CONFIGS:
                    payload = VIBE_CONFIGS[vibe_name]["payload"].copy()
                else:
                    payload = {"note": "Dynamic generation payload"}

                # Merge specific configs if any (e.g., angle)
                if vibe_configs and vibe_name in vibe_configs:
                    payload.update(vibe_configs[vibe_name])

                st.json(payload)

    @staticmethod
    def render_generation_results(generated_images: Dict[str, Image.Image]):
        """Render generated images with download buttons"""
        if not generated_images:
            return

        st.markdown("---")
        st.markdown("### 🖼️ Generated Marketing Assets")

        cols = st.columns(len(generated_images))

        for idx, (vibe_name, image) in enumerate(generated_images.items()):
            with cols[idx]:
                # Try to find emoji, default to sparkle
                emoji = VIBE_CONFIGS.get(vibe_name, {}).get("emoji", "✨")
                st.image(image, caption=f"{emoji} {vibe_name}", use_container_width=True)

                from services.image_service import ImageService
                img_bytes = ImageService.image_to_bytes(image)

                st.download_button(
                    label="⬇️ Download",
                    data=img_bytes,
                    file_name=f"{vibe_name.replace(' ', '_').lower()}_asset.png",
                    mime="image/png",
                    use_container_width=True
                )

    @staticmethod
    def render_placeholder_content():
        """Render placeholder content when no image is uploaded"""
        st.info("👆 Please upload a product image to get started")
        st.markdown("### 💡 Example: How It Works")
        st.markdown("""
        **Context Chameleon** transforms your product images into marketing assets:
        1. **Upload** - Your product image (works best with transparent backgrounds)
        2. **Analyze** - Gemini understands your object (Shoe? Drink? Chair?)
        3. **Configure** - Choose specific angles or consumption scenarios.
        4. **Generate** - AI places your product in professional contexts.
        """)

    @staticmethod
    def render_footer():
        """Render application footer"""
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666; padding: 20px;'>
            <p>Powered by <strong>Bria FIBO Engine</strong></p>
            <p style='font-size: 0.8rem;'>Precision Controllable Generation</p>
        </div>
        """, unsafe_allow_html=True)
