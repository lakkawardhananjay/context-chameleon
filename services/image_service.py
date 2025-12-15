import io
from typing import Tuple
from PIL import Image, ImageDraw, ImageFont

from config.settings import Settings
from config.vibe_configs import VIBE_CONFIGS


class ImageService:
    """Service for image processing and mock generation"""
    
    COLOR_SCHEMES = {
        "Summer Splash": {
            "gradient": [(255, 215, 0), (255, 182, 193), (135, 206, 250), (255, 239, 213)],
            "accent_color": (255, 223, 0),
            "elements": "sun"
        },
        "Midnight Luxury": {
            "gradient": [(26, 26, 46), (15, 52, 96), (88, 24, 69), (199, 0, 57)],
            "accent_color": (199, 0, 57),
            "elements": "neon"
        },
        "Hero Spotlight": {
            "gradient": [(30, 30, 30), (60, 60, 60), (90, 90, 90), (120, 120, 120)],
            "accent_color": (255, 215, 0),
            "elements": "spotlight"
        },
        "Tech Abstract": {
            "gradient": [(0, 0, 50), (20, 20, 80), (40, 40, 120), (60, 60, 150)],
            "accent_color": (0, 255, 255),
            "elements": "tech"
        }
    }
    
    @staticmethod
    def generate_mock_image(
        vibe_name: str,
        product_image: Image.Image,
        width: int = None,
        height: int = None
    ) -> Image.Image:
        """
        Generate a mock marketing image by compositing product onto styled background
        
        Args:
            vibe_name: Name of the vibe to apply
            product_image: Source product image
            width: Output width (defaults to Settings.DEFAULT_IMAGE_WIDTH)
            height: Output height (defaults to Settings.DEFAULT_IMAGE_HEIGHT)
            
        Returns:
            Composite PIL Image
        """
        width = width or Settings.DEFAULT_IMAGE_WIDTH
        height = height or Settings.DEFAULT_IMAGE_HEIGHT
        
        # Create styled background
        background = ImageService._create_styled_background(vibe_name, width, height)
        
        # Prepare and composite product
        product = ImageService._prepare_product_image(product_image, width, height)
        product_x = (width - product.width) // 2
        product_y = (height - product.height) // 2
        background.paste(product, (product_x, product_y), 
                        product if product.mode == 'RGBA' else None)
        # Add decorative labels
        ImageService._add_labels(background, vibe_name, width, height)
        return background
    @staticmethod
    def _create_styled_background(
        vibe_name: str,
        width: int,
        height: int
    ) -> Image.Image:
        """Create a gradient background with decorative elements"""
        scheme = ImageService.COLOR_SCHEMES.get(vibe_name, 
                                                ImageService.COLOR_SCHEMES["Midnight Luxury"])
        
        # Create base with gradient
        img = Image.new('RGB', (width, height), scheme["gradient"][0])
        draw = ImageDraw.Draw(img)
        
        # Apply gradient
        gradient_colors = scheme["gradient"]
        num_colors = len(gradient_colors)
        section_height = height // num_colors
        
        for i in range(height):
            section = min(i // section_height, num_colors - 2)
            progress = (i % section_height) / section_height
            
            c1 = gradient_colors[section]
            c2 = gradient_colors[section + 1]
            
            blended = tuple(
                int(c1[j] + (c2[j] - c1[j]) * progress)
                for j in range(3)
            )
            
            draw.line([(0, i), (width, i)], fill=blended)
        
        # Add decorative elements
        ImageService._add_decorative_elements(draw, scheme, width, height)
        
        return img
    
    @staticmethod
    def _add_decorative_elements(
        draw: ImageDraw.Draw,
        scheme: dict,
        width: int,
        height: int
    ):
        """Add decorative elements based on vibe style"""
        if scheme["elements"] == "sun":
            for radius in [100, 80, 60]:
                draw.ellipse(
                    [width - 250 - radius, 120 - radius, 
                     width - 250 + radius, 120 + radius],
                    fill=scheme["accent_color"]
                )
        elif scheme["elements"] == "neon":
            for i in range(6):
                y = height // 2 + i * 40 - 100
                draw.rectangle([80, y, width - 80, y + 4], 
                             fill=scheme["accent_color"])
        elif scheme["elements"] == "spotlight":
            # Add a circular spotlight effect
            draw.ellipse(
                [(width - 300) // 2, (height - 300) // 2, (width + 300) // 2, (height + 300) // 2],
                fill=scheme["accent_color"] + (50,) # semi-transparent
            )
        elif scheme["elements"] == "tech":
            # Add some futuristic lines/grid
            # Ensure proper alpha for lines
            line_color = scheme["accent_color"] + (50,) 
            for i in range(0, width, 50):
                draw.line([(i, 0), (i - height, height)], fill=line_color, width=2)
            for i in range(0, height, 50):
                draw.line([(0, i), (width, i)], fill=line_color, width=2)
        else:  # minimal
            draw.rectangle([width - 300, height - 300, width - 80, height - 80],
                         outline=scheme["accent_color"], width=4)
    
    @staticmethod
    def _prepare_product_image(
        product_image: Image.Image,
        canvas_width: int,
        canvas_height: int
    ) -> Image.Image:
        """Resize and prepare product image for compositing"""
        product = product_image.copy()
        
        max_size = int(min(canvas_width, canvas_height) * Settings.MAX_PRODUCT_SIZE_RATIO)
        product.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        if product.mode != 'RGBA':
            product = product.convert('RGBA')
        
        return product
    
    @staticmethod
    def _add_labels(
        image: Image.Image,
        vibe_name: str,
        width: int,
        height: int
    ):
        """Add title and mock preview labels to image"""
        draw = ImageDraw.Draw(image)
        
        try:
            font_title = ImageFont.truetype("arial.ttf", 48)
            font_badge = ImageFont.truetype("arial.ttf", 24)
        except:
            font_title = ImageFont.load_default()
            font_badge = ImageFont.load_default()
        
        # Determine text colors
        text_color = (255, 255, 255) if vibe_name == "Midnight Luxury" else (0, 0, 0)
        shadow_color = (0, 0, 0) if vibe_name != "Midnight Luxury" else (255, 255, 255)
        
        # Draw title
        emoji = VIBE_CONFIGS[vibe_name]["emoji"]
        title_text = f"{emoji} {vibe_name}"
        
        title_bbox = draw.textbbox((0, 0), title_text, font=font_title)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (width - title_width) // 2
        title_y = 40
        
        draw.text((title_x + 2, title_y + 2), title_text, fill=shadow_color, font=font_title)
        draw.text((title_x, title_y), title_text, fill=text_color, font=font_title)
        
        # Draw mock preview badge
        badge_text = "🎨 MOCK PREVIEW - Bria FIBO Simulation"
        badge_bbox = draw.textbbox((0, 0), badge_text, font=font_badge)
        badge_width = badge_bbox[2] - badge_bbox[0]
        badge_x = (width - badge_width) // 2
        badge_y = height - 60
        
        padding = 15
        badge_bg = [badge_x - padding, badge_y - 8, 
                   badge_x + badge_width + padding, badge_y + 28]
        draw.rectangle(badge_bg, fill=(0, 0, 0, 180))
        draw.rectangle(badge_bg, outline=(255, 255, 255), width=2)
        
        draw.text((badge_x, badge_y), badge_text, fill=(255, 255, 255), font=font_badge)
    
    @staticmethod
    def image_to_bytes(image: Image.Image, format: str = "PNG") -> bytes:
        """Convert PIL Image to bytes"""
        buffered = io.BytesIO()
        image.save(buffered, format=format)
        return buffered.getvalue()