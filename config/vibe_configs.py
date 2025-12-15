
from typing import Dict, Any

VIBE_CONFIGS: Dict[str, Dict[str, Any]] = {
    
  "Marketplace Clean": {
  "emoji": "🛒",
  "description": "Marketplace-compliant e-commerce presentation with a pure white background and neutral studio lighting",
  "payload": {
    "lighting_mode": "soft_box",
    "background_prompt": "pure white or very light neutral background, smooth matte finish, completely non-distracting, no gradients or textures",
    "camera_angle": "None",
    "structure_lock": 0.9,
    "force_camera_angle": "false",
    "color_temperature": "neutral",
    "shadow_intensity": "very subtle, soft, diffused, directly beneath product only",
    "atmosphere": "clean, modern, professional, premium e-commerce aesthetic",
    "modifications_from_original": [
      "Enforced a pure white or light neutral background to meet global marketplace image standards.",
      "Standardized camera angle to a slightly elevated front-quarter view commonly used for product listings.",
      "Applied soft, even, diffused lighting to clearly reveal product form and surface details.",
      "Removed any environmental context, props, or lifestyle elements for catalog consistency.",
      "Preserved accurate product proportions, colors, and functional realism.",
      "Optimized the overall presentation for marketplace approval and customer trust."
    ]
  }
},
"Consumption/Active": {
        "emoji": "🧗",
        "description": "Product in action. Real-world usage scenarios.",
        "payload": {
            "lighting_mode": "natural_outdoor", # Default base, will be overridden
            "background_prompt": "high quality lifestyle photography, natural lighting, depth of field",
            "camera_angle": "eye_level",
            "structure_lock": 0.6, # Slightly lower lock to allow for hand/body interaction
            "color_temperature": "neutral",
            "shadow_intensity": "soft",
            "atmosphere": "dynamic_lifestyle"
        }
    },

    "Midnight Luxury": {
        "emoji": "🌃",
        "description": "Neon/dark lighting, urban context",
        "payload": {
            "lighting_mode": "neon_dramatic",
            "background_prompt": "dark urban cityscape at night with neon lights, cyberpunk aesthetic, luxury atmosphere",
            "camera_angle": "low_angle",
            "structure_lock": 0.90,
            "color_temperature": "cool",
            "shadow_intensity": "dramatic",
            "atmosphere": "moody_cinematic"
        }
    },

    "Insta Lifestyle": {
        "emoji": "📸",
        "description": "Aesthetic, influencer-style shot with natural lighting and soft focus.",
        "payload": {
            "lighting_mode": "golden_hour",
            # THE MAGIC PROMPT:
            "background_prompt": (
                "aesthetic lifestyle photography, product placed on a textured light oak table, "
                "soft morning sunlight casting dappled shadows from plants, "
                "blurred cozy modern living room background, "
                "creamy bokeh, shallow depth of field (f/1.8), "
                "high resolution social media content"
            ),
            # THE SETTINGS:
            # We use 0.88 lock to allow the lighting to 'wrap' around the product slightly 
            # so it sits naturally in the scene (blending pixels at the edges).
            "structure_lock": 0.88, 
            "color_temperature": "warm_golden",
            "shadow_intensity": "medium_soft",
            "atmosphere": "aspirational, organic, warm, authentic"
        }
    },
    "Hero Spotlight": {
        "emoji": "✨",
        "description": "A dramatic, high-contrast 'hero shot' of the product against a dark, textured background.",
        "payload": {
            "lighting_mode": "dramatic_spotlight",
            "background_prompt": "dark, subtly textured background, deep shadows, elegant, luxurious, focus on product",
            "camera_angle": "low_angle",
            "structure_lock": 0.95,
            "color_temperature": "neutral",
            "shadow_intensity": "strong_contrast",
            "atmosphere": "premium_dramatic"
        }
    },
    "Tech Abstract": {
        "emoji": "🔮",
        "description": "A clean, futuristic look with cool lighting and abstract geometric backgrounds.",
        "payload": {
            "lighting_mode": "cool_led_soft",
            "background_prompt": "abstract geometric background, glowing blue and purple lines, subtle grid patterns, technological, futuristic, clean, sleek",
            "camera_angle": "eye_level",
            "structure_lock": 0.92,
            "color_temperature": "cool",
            "shadow_intensity": "minimal_soft",
            "atmosphere": "futuristic_tech"
        }
    }
}
