from flask import Flask, request, send_file, jsonify
from PIL import Image
import os
from io import BytesIO
from process_img import image_routes

from border import add_torn_stroke_border_with_texture  # Import your existing function

app = Flask(__name__)

# UPLOAD_FOLDER = "uploads"
# OUTPUT_FOLDER = "outputs"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(OUTPUT_FOLDER, exist_ok=True)
app.register_blueprint(image_routes, url_prefix='/images')

if __name__ == '__main__':
    app.run(debug=True)
