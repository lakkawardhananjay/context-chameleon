import base64
import io
import time
from typing import Dict, Any, Optional
from PIL import Image
import requests
from config.settings import Settings
from config.vibe_configs import VIBE_CONFIGS
from config.consumption_data import CONSUMPTION_SCENARIOS


class BriaService:
    """Service for interacting with Bria FIBO API"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {"api_token": api_key, "Content-Type": "application/json"}

    def generate_image(
        self, image: Image.Image, vibe_name: str, image_analysis: Dict[str, Any], specific_config: Optional[Dict[str, Any]] = None
    ) -> Optional[Image.Image]:
        """
        Generate image using Bria FIBO API with analyzed context
        """
        try:
            # Convert image to base64
            img_base64 = self._image_to_base64(image)
            
            # UNPACK 3 VALUES NOW
            prompt, structure_lock, negative_prompt = self._construct_payload_params(
                vibe_name, image_analysis, specific_config
            )

            # Build API payload
            payload = {
                "prompt": prompt,
                "num_results": 1,
                "width": 7680, # Keep 8K resolution
                "height": 4320, # Keep 8K resolution
                "structure_guidance_scale": structure_lock, 
                "sync": True,
                "negative_prompt": negative_prompt # <--- SEND IT HERE
            }
            
            print("=== FINAL PAYLOAD BEING SENT TO BRIA ===")
            print(payload)
            print("=" * 50)

            # Make API request
            response = requests.post(
                Settings.BRIA_API_ENDPOINT,
                headers=self.headers,
                json=payload,
                timeout=120,
            )

            response.raise_for_status()
            result = response.json()

            # Handle async response if needed
            if result.get("status") == "IN_PROGRESS":
                result = self._poll_for_completion(result)
                if not result:
                    return None

            # Extract and download image
            return self._extract_generated_image(result)

        except requests.exceptions.HTTPError as e:
            error_msg = f"Bria API HTTP Error: {e}"
            if hasattr(e, "response") and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_msg += f"\nDetails: {error_data}"
                except:
                    error_msg += f"\nResponse: {e.response.text}"
            raise Exception(error_msg)
        except Exception as e:
            raise Exception(f"Bria Generation Error: {str(e)}")


    def _construct_payload_params(
        self,
        vibe_name: str,
        image_analysis: Dict[str, Any],
        specific_config: Optional[Dict[str, Any]]
    ):
        """
        Builds the prompt, determines structure lock, AND SANITIZES TEXT.
        """

        # --- A. SUBJECT EXTRACTION ---
        try:
            # Use a more robust subject extraction
            subjects = image_analysis.get("subjects", [])
            if subjects:
                all_subject_details = []
                for subject in subjects:
                    desc = subject.get('detailed_description', '')
                    colors = subject.get('primary_colors')
                    if colors:
                        desc += f" Primary colors are {', '.join(colors)}."
                    material = subject.get('material')
                    if material:
                        desc += f" Made of {material}."
                    all_subject_details.append(desc)
                subject_prompt = " ".join(all_subject_details)
            else:
                subject_prompt = "the product"
        except Exception:
            subject_prompt = "the product"

        # --- B. CONFIG LOADING ---
        base_payload = VIBE_CONFIGS.get(vibe_name, {}).get("payload", {})
        structure_lock = base_payload.get("structure_lock", 0.9)
        camera_instruction = ""
        prompt_modifier = ""
        negative_prompt = base_payload.get("negative_prompt", "")  # Get base negative

        # --- C. SCENARIO & CONFIG APPLICATION (THE FIX) ---
        scenario_id = ""
        if specific_config:
            # Correctly get scenario_id from the specific_config dictionary
            scenario_id = specific_config.get("scenario_id", "").lower()

            # If we have a scenario, find its data in CONSUMPTION_SCENARIOS
            if scenario_id:
                found_scenario = False
                for category, scenarios in CONSUMPTION_SCENARIOS.items():
                    if isinstance(scenarios, list):
                        for scenario in scenarios:
                            if scenario.get("id") == scenario_id:
                                # Apply scenario-specific prompt and negative prompt
                                if "prompt_modifier" in scenario:
                                    prompt_modifier = scenario["prompt_modifier"]
                                if "negative_prompt" in scenario:
                                    negative_prompt += ", " + scenario["negative_prompt"]
                                
                                found_scenario = True
                                break # Exit inner loop once scenario is found
                    if found_scenario:
                        break # Exit outer loop as well
                
            # Apply Camera Instruction (if any)
            if "camera_prompt" in specific_config:
                camera_instruction = specific_config["camera_prompt"]
            elif "camera_angle" in specific_config: # Fallback for old key
                 camera_instruction = f"Use a {specific_config['camera_angle'].replace('_', ' ')} camera angle."


            # Apply Structure Lock Override (if any)
            if "structure_lock" in specific_config:
                structure_lock = specific_config["structure_lock"]

        # --- D. SANITIZATION (Cap Stripper) ---
        if scenario_id and ("drinking" in scenario_id or "open" in scenario_id or "pouring" in scenario_id):
            # Force Open State
            subject_prompt = subject_prompt.replace("sealed", "opened")
            subject_prompt = subject_prompt.replace("closed", "opened")
            subject_prompt = subject_prompt.replace("cap", "")
            subject_prompt = subject_prompt.replace("lid", "")
            subject_prompt = subject_prompt.replace("cork", "")
            # Prepend the "opened" state for clarity
            if "bottle" in subject_prompt.lower():
                subject_prompt = "opened bottle of " + subject_prompt
            elif "can" in subject_prompt.lower():
                subject_prompt = "opened can of " + subject_prompt
            else:
                subject_prompt = "opened " + subject_prompt
            
            subject_prompt += ", opened neck, liquid visible at rim"

        # --- E. PROMPT ASSEMBLY ---
        bg_prompt = base_payload.get("background_prompt", "clean background")
        atmosphere = base_payload.get("atmosphere", "")
        quality_booster = "ultra-realistic, 8k resolution, cinematic lighting, professional marketing photograph."

        # Assemble the full prompt from all pieces
        full_prompt = f"{subject_prompt}. {prompt_modifier} {camera_instruction} {bg_prompt}. {atmosphere} {quality_booster}"
        # Clean up extra spaces
        full_prompt = " ".join(full_prompt.split())

        return full_prompt, structure_lock, negative_prompt    

   
   

    def _poll_for_completion(self, initial_result: Dict) -> Optional[Dict]:
        """Poll Bria API until image generation is complete"""
        request_id = initial_result.get("request_id")
        if not request_id:
            return None
        for _ in range(Settings.MAX_POLL_ATTEMPTS):
            time.sleep(Settings.POLL_INTERVAL)

            response = requests.get(
                f"{Settings.BRIA_API_ENDPOINT.rsplit('/', 2)[0]}/status/{request_id}",
                headers=self.headers,
            )
            status_data = response.json()
            if status_data.get("status") == "COMPLETED":
                return status_data
            elif status_data.get("status") == "ERROR":
                error_msg = status_data.get("error", {}).get("message", "Unknown error")
                raise Exception(f"Bria API Error: {error_msg}")

        raise Exception("Generation timeout: max polling attempts reached")

    def _extract_generated_image(self, result: Dict) -> Optional[Image.Image]:
        """Extract and download generated image from API result"""
        if "result" not in result:
            raise Exception("Unexpected response format: no 'result' field")

        # Handle different result formats
        result_data = result["result"]
        image_url = None

        if isinstance(result_data, dict) and "image_url" in result_data:
            image_url = result_data["image_url"]
        elif isinstance(result_data, list) and len(result_data) > 0:
            image_url = result_data[0].get("image_url")

        if not image_url:
            raise Exception("Could not find image URL in response")

        # Download image
        img_response = requests.get(image_url)
        img_response.raise_for_status()

        return Image.open(io.BytesIO(img_response.content))

    @staticmethod
    def _image_to_base64(image: Image.Image) -> str:
        """Convert PIL Image to base64 string"""
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()

    def _apply_user_camera_angle(
        self, vibe_name: str, theme_payload: Dict[str, Any], user_angle: str
    ):
        # Only modify for Marketplace Clean
        if vibe_name == "Marketplace Clean":
            payload = theme_payload.copy()
            payload["camera_angle"] = user_angle
            return payload
        return theme_payload
    def _extract_product_only(self, image_analysis: Dict[str, Any]) -> str:
        """Extract ONLY product details for low structure_lock scenarios"""
        subjects = image_analysis.get("subjects", [])
        if subjects:
        # Extract just the can description, not the scene
            subject_desc = subjects[0].get('detailed_description', '')
        # Clean up to remove scene context
            if "on a" in subject_desc:
             subject_desc = subject_desc.split("on a")[0] + "."
            return f"Product: {subject_desc} "
        return ""

    def _extract_scene_with_details(self, image_analysis: Dict[str, Any]) -> str:
     """Extract scene details for high structure_lock"""
     return f"Original scene: {image_analysis.get('global_description', '')}. "
