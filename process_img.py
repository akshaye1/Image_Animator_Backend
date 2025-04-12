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

@image_routes.route('/add_border', methods=['POST', 'OPTIONS'])
def process_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_name, file_extension = os.path.splitext(file.filename)

    if file:
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        temp_file = file_name[:-len(file_extension)] + ".png"
        print("temp_file", temp_file)
        output_path = os.path.join(OUTPUT_FOLDER, f"processed_{temp_file}")
        file.save(input_path)

        # Run the torn border function
        add_torn_stroke_border_with_texture(
    input_path=input_path,
    output_path=output_path,
    file_extension=file_extension,
    texture_path=r"/home/ajinkya-thorat/Downloads/crumpled-craft-beige-paper.jpg",
    border_size=50,
    stroke_width=20,
    roughness=15,
    blur_radius=2,
    shadow_offset=(10, 10),
    shadow_blur=8,
    shadow_opacity=100,
    texture_opacity=130
)       
        """For UI"""
        # res_mime_type = 'image/' + file_extension
        # response = send_file(output_path, as_attachment=True, mimetype=res_mime_type)
        # response.access_control_allow_origin = "*"

        """For postman"""
        response = send_file(output_path, as_attachment=True, mimetype='image/png')
        return response
