from flask import Flask, render_template, request
import cv2
import numpy as np
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Folders to store uploaded and processed images
UPLOAD_FOLDER = 'static/uploads/'
PROCESSED_FOLDER = 'static/processed/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# Home Page
@app.route('/')
def home():
    return '''
    <!doctype html>
    <html>
    <head>
        <title>Image to Pencil Sketch</title>
        <style>
            body {
                background: linear-gradient(to right, #ffb6c1, #ffe4e1);
                font-family: 'Segoe UI', sans-serif;
                color: #333;
            }
            .container {
                margin-top: 100px;
                text-align: center;
            }
            h1 {
                color: #444;
                font-size: 36px;
            }
            input[type="file"] {
                margin: 20px;
                padding: 10px;
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 8px;
            }
            input[type="submit"] {
                background-color: #ff69b4;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
            }
            input[type="submit"]:hover {
                background-color: #ff1493;
            }
        </style>
    </head>
    <body>
    <div class="container">
        <h1>🎨 Image to Pencil Sketch Converter</h1>
        <form method="post" action="/upload" enctype="multipart/form-data">
            <input type="file" name="file" accept="image/*" required>
            <br>
            <input type="submit" value="Convert to Sketch">
        </form>
    </div>
    </body>
    </html>
    '''

# Upload and process image
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Convert image to pencil sketch
        sketch_path = create_pencil_sketch(filepath, filename)

        return f'''
        <html>
        <head>
            <title>Result</title>
            <style>
                body {{
                    background-color: #fff0f5;
                    font-family: Arial, sans-serif;
                    text-align: center;
                }}
                img {{
                    margin: 20px;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                }}
                a {{
                    text-decoration: none;
                    background-color: #ff69b4;
                    color: white;
                    padding: 10px 20px;
                    border-radius: 8px;
                }}
                a:hover {{
                    background-color: #ff1493;
                }}
            </style>
        </head>
        <body>
        <h1>🖼️ Original Image</h1>
        <img src="/{filepath}" width="300">
        <h1>✏️ Pencil Sketch</h1>
        <img src="/{sketch_path}" width="300">
        <br><br>
        <a href="/{sketch_path}" download>⬇️ Download Pencil Sketch</a>
        <br><br>
        <a href="/">🔙 Back to Home</a>
        </body>
        </html>
        '''

# Function to convert image into pencil sketch
def create_pencil_sketch(input_path, filename):
    image = cv2.imread(input_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inverted_image = cv2.bitwise_not(gray_image)
    blurred = cv2.GaussianBlur(inverted_image, (21, 21), sigmaX=0, sigmaY=0)
    inverted_blur = cv2.bitwise_not(blurred)
    sketch = cv2.divide(gray_image, inverted_blur, scale=256.0)

    output_path = os.path.join(app.config['PROCESSED_FOLDER'], f'sketch_{filename}')
    cv2.imwrite(output_path, sketch)
    return output_path

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
