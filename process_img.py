from flask import Flask, request, send_file, jsonify, Blueprint
from PIL import Image
import os
from io import BytesIO
from border import add_torn_stroke_border_with_texture

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

image_routes = Blueprint('image_routes', __name__)

@image_routes.route('/add_border', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        output_path = os.path.join(OUTPUT_FOLDER, f"processed_{file.filename}")
        file.save(input_path)

        # Run the torn border function
        add_torn_stroke_border_with_texture(
    input_path=input_path,
    output_path=output_path,
    texture_path=r"C:\AKSHAY\Projects\flow-vision-landing-main\flow-vision-landing-main\uploads\crumpled-craft-beige-paper.jpg",
    border_size=50,
    stroke_width=20,
    roughness=15,
    blur_radius=2,
    shadow_offset=(10, 10),
    shadow_blur=8,
    shadow_opacity=100,
    texture_opacity=130
)
        
        return send_file(output_path, mimetype='image/png')
