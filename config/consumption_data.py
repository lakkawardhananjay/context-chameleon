from typing import Dict, List, Any

# 1. THE MAPPING
# Gemini detects "Subject". We look for these keywords in the description.
# If Gemini says "A silver aluminum can...", we match "can".
SUBJECT_TO_SCENARIO_MAP = {
    "beer": "beverage_can",
    "stout": "beverage_can",
    "ale": "beverage_can",
    "lager": "beverage_can",
    "soda": "beverage_can",
    "can": "beverage_can",
    "beverage": "beverage_can",
    "drink": "beverage_can", 
    "shoe": "footwear",
    "sneaker": "footwear",
    "boot": "footwear",
    "runner": "footwear",
    "trainer": "footwear",
    "footwear": "footwear",   
    "bottle": "bottle_glass",
    "glass": "bottle_glass",
    "chair": "furniture",
    "sofa": "furniture",
    "couch": "furniture"
}

# 2. THE SCENARIOS
CONSUMPTION_SCENARIOS: Dict[str, List[Dict[str, str]]] = {
    "beverage_can": [
        {
            "id": "holding_drink",
            "label": "Hand Holding",
            # Make sure this file exists in assets/consumption/ or it will look broken
            "image_path": "assets/consumption/hand_holding_can.jpg", 
            "prompt_modifier": "extreme close-up, photorealistic commercial photography of a real human hand naturally holding an aluminum beverage can, relaxed grip with visible fingers and thumb placement, subtle skin texture, natural creases, fine details of knuckles and fingernails, realistic proportions, no distortion. Soft natural lighting with gentle highlights reflecting off the metallic can surface, accurate aluminum reflections, condensation droplets visible on the can suggesting cold temperature. Shallow depth of field, creamy bokeh background, lifestyle environment blurred and unobtrusive (outdoor café, casual urban setting, or modern lifestyle scene). Shot on a high-end DSLR camera, 85mm lens, f/1.8 aperture, ISO 100, professional color grading, cinematic tones, clean whites, balanced contrast. Advertising-style composition, product clearly readable and centered, brand-safe framing, modern premium aesthetic, realistic shadows, no harsh lighting. High resolution, ultra-sharp focus on hand and can, commercial beverage advertisement, lifestyle product photography, authentic human interaction, natural pose, no text overlays, no logos unless specified, no extra fingers, no deformed anatomy, no unrealistic reflections.",
            "negative_prompt": "bottle cap, can lid, closed container, unopened, sealed, lid on, cap on, screw top, cap on bottle, bottle with cap, closed bottle"
        },
        {
            "id": "drinking",
            "label": "Drinking",
            "image_path": "assets/consumption/drinking.jpg",
            "prompt_modifier": "a happy person drinking from the beverage container, party atmosphere, bokeh background, high quality commercial advertisement, photorealistic, sharp focus on the product, captured mid-action.",
            # Add negative prompt directly here
            "negative_prompt": "bottle cap, can lid, closed container, unopened, sealed, lid on, cap on, screw top, cap on bottle, bottle with cap, closed bottle"
        },
        {
            "id": "table_pour",
            "label": "Ice Cold",
            "image_path": "assets/consumption/ice_cold.jpg",
            "prompt_modifier": "the can placed on a wooden table with condensation droplets, cold refreshing atmosphere, summer vibe"
        },
        {
            "id": "pouring_can",
            "label": "Pouring",
            "image_path": "assets/consumption/pouring_bottle.jpg",
            "prompt_modifier": "dynamic high-speed photography, frozen motion. The product is tilted, pouring its liquid contents into a premium glass. Splash details, droplets, liquid texture, visible carbonation/viscosity. Professional studio lighting highlighting the liquid stream.",
            "negative_prompt": "bottle cap, can lid, closed container, unopened, sealed, lid on, cap on, screw top, cap on bottle, closed bottle, spilled mess, dirty glass, broken glass, defying gravity, viscous slime, unrealistic liquid color",
            "guidance_scale": 4
        }
    ],
    "bottle_glass": [
        {
            "id": "pouring_from_bottle",
            "label": "Pouring",
            "image_path": "assets/consumption/pouring_bottle.jpg",
            "prompt_modifier": "dynamic high-speed photography, frozen motion. The product is tilted, pouring its liquid contents into a premium glass. Splash details, droplets, liquid texture, visible carbonation/viscosity. Professional studio lighting highlighting the liquid stream.",
            "negative_prompt": "bottle cap, can lid, closed container, unopened, sealed, lid on, cap on, screw top, cap on bottle, closed bottle, spilled mess, dirty glass, broken glass, defying gravity, viscous slime, unrealistic liquid color",
            "guidance_scale": 4
        },
        {
            "id": "open_bottle_on_table",
            "label": "Opened on Table",
            "image_path": "assets/consumption/bottle_on_table.jpg",
            "prompt_modifier": "The bottle is open and placed on a stylish bar or table, ready to be served, with a glass nearby.",
            "negative_prompt": "closed container, unopened, sealed, lid on, cap on, screw top, cap on bottle, closed bottle"
        }
    ],
    "footwear": [
        {
            "id": "tying_laces",
            "label": "Tying Laces",
            "image_path": "assets/consumption/tying_shoe.jpg",
            "prompt_modifier": "a person bending down tying the shoelaces, urban street level perspective, focus on the shoes",
            "negative_prompt": "extra limbs, distorted feet, more than two feet"
        },
        {
            "id": "walking",
            "label": "Walking Motion",
            "image_path": "assets/consumption/walking_shoe.jpg",
            "prompt_modifier": "low angle shot of feet walking on pavement, motion blur, urban city background, streetwear aesthetic",
            "negative_prompt": "extra limbs, distorted feet, more than two feet, blurry shoes"
        },
        {
            "id": "performance_action",
            "label": "Performance",
            "image_path": "assets/consumption/performance_shoe.jpg",
            "prompt_modifier": "dynamic action photography, athlete in mid-stride, foot landing with impact, jumping, sprinting motion, showing shoe's grip and cushioning on [specific surface: track, trail, court].",
            "negative_prompt": "static, slow motion, walking, standing still, relaxed"
        },
        {
            "id": "lifestyle_casual",
            "label": "Lifestyle",
            "image_path": "assets/consumption/lifestyle_shoe.jpg",
            "prompt_modifier": "casual lifestyle photography, feet casually crossed, shoe resting on [specific surface: coffee shop floor, urban pavement, park bench], relaxed pose, integrated with fashionable clothing. Soft ambient lighting.",
            "negative_prompt": "intense workout, formal setting, muddy, strenuous activity"
        }
    ],
    "default": [
         {
            "id": "generic_lifestyle",
            "label": "Lifestyle Context",
            "image_path": "assets/consumption/generic.jpg",
            "prompt_modifier": "placed in a modern lifestyle home environment, sunlight, cozy atmosphere, interior design photography",
            "negative_prompt": "blurry, distorted, ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, bad anatomy, watermark, signature, cut off, low contrast, underexposed, overexposed, bad art, beginner, amateur, distorted face"
        },
        {
            "id": "outdoor_nature",
            "label": "Outdoor Nature",
            "image_path": "assets/consumption/nature.jpg",
            "prompt_modifier": "placed on a rock in a forest, nature background, sunlight filtering through trees, eco-friendly vibe",
            "negative_prompt": "blurry, distorted, ugly, tiling, poorly drawn, out of frame, extra limbs, disfigured, deformed, body out of frame, bad anatomy, watermark, signature, cut off, low contrast, underexposed, overexposed, bad art, beginner, amateur"
        }
    ]
}