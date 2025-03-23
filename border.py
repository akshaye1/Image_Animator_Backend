from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageChops
import random
import numpy as np



def add_torn_stroke_border_with_texture(input_path, output_path, texture_path, border_size=50, stroke_width=10, roughness=15, blur_radius=2, shadow_offset=(10, 10), shadow_blur=8, shadow_opacity=100, texture_opacity=150):
    # Load image and convert to RGBA
    img = Image.open(input_path).convert("RGBA")
    width, height = img.size
    
    # Create a canvas with extra space for the border
    new_width = width + 2 * border_size
    new_height = height + 2 * border_size
    canvas = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))
    canvas.paste(img, (border_size, border_size), img)
    
    # Create a mask from the image's transparency (detect subject shape)
    alpha_channel = img.split()[3]
    subject_mask = alpha_channel.point(lambda p: p > 128 and 255)
    subject_outline = subject_mask.filter(ImageFilter.FIND_EDGES)
    
    # Extract the coordinates of the subject's edge
    edge_coords = np.argwhere(np.array(subject_outline))
    edge_coords = [(y + border_size, x + border_size) for x, y in edge_coords]
    
    # Introduce roughness to the stroke path
    rough_outline = [(x + random.randint(-roughness, roughness), y + random.randint(-roughness, roughness)) for x, y in edge_coords]
    
    # Create a mask for the jagged stroke effect
    mask = Image.new("L", (new_width, new_height), 0)
    draw = ImageDraw.Draw(mask)
    draw.line(rough_outline, fill=255, width=stroke_width, joint='curve')
    mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))
    
    # Create the white stroke border ONLY on the outer edges
    stroke_border = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))
    draw_stroke = ImageDraw.Draw(stroke_border)
    draw_stroke.line(rough_outline, fill=(255, 255, 255, 255), width=stroke_width, joint='curve')
    final_result = Image.alpha_composite(canvas, stroke_border)
    
    # Add shadow under the stroke
    shadow = Image.new("L", (new_width, new_height), 0)
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.line(
        [(x + shadow_offset[0], y + shadow_offset[1]) for x, y in rough_outline],
        fill=shadow_opacity, width=stroke_width
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(shadow_blur))
    shadow_rgba = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))
    shadow_rgba.putalpha(shadow)
    final_result = Image.alpha_composite(shadow_rgba, final_result)
    
    # Load texture and blend it in
    texture = Image.open(texture_path).convert("RGBA")
    texture = texture.resize((width, height))  # Resize texture to match image size
    
    # Create a mask using the subject's alpha channel
    # This ensures texture only applies to the actual person/subject
    subject_alpha_mask = Image.new("L", (new_width, new_height), 0)
    subject_alpha_mask.paste(alpha_channel, (border_size, border_size))
    
    # Place texture on canvas
    texture_canvas = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))
    texture_canvas.paste(texture, (border_size, border_size))
    
    # Apply the texture with transparency ONLY to the subject area using the alpha mask
    texture_canvas.putalpha(ImageChops.multiply(texture_canvas.split()[3], subject_alpha_mask))
    
    # Adjust texture opacity
    texture_canvas = Image.blend(
        Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0)),
        texture_canvas, 
        alpha=texture_opacity / 255
    )
    
    # Ensure the subject remains fully visible without being covered
    final_result = Image.alpha_composite(final_result, canvas)
    
    # Composite the texture with the result
    final_result = Image.alpha_composite(final_result, texture_canvas)
    
    if final_result.mode == "RGBA":
        final_result = final_result.convert("RGB")

    # Save the final image
    # final_result.save(output_path.replace(".jpg", ".png"))
    final_result.save(output_path)

# Usage
# add_torn_stroke_border_with_texture(
#     input_path=r"C:\OMKAR\Arbhaat\umesh kulkarni.jpg",
#     output_path="output_torn_stroke_border.jpg",
#     texture_path=r"C:\AKSHAY\Projects\flow-vision-landing-main\flow-vision-landing-main\uploads\crumpled-craft-beige-paper.jpg",
#     border_size=50,
#     stroke_width=20,
#     roughness=15,
#     blur_radius=2,
#     shadow_offset=(10, 10),
#     shadow_blur=8,
#     shadow_opacity=100,
#     texture_opacity=130
# )