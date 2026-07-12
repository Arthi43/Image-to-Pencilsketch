# Image to Pencil Sketch (Flask + OpenCV)

A simple Flask web application that converts an uploaded image into a **pencil sketch** style image using **OpenCV**.

## Features
- Upload an image from your browser
- Converts it to a pencil-sketch effect
- Shows original + processed sketch
- Provides a download link for the generated sketch

## Demo / Screens
- Home page: `/`
- Result page: served after upload

## Tech Stack
- **Flask** (web server)
- **OpenCV (opencv-python)** (image processing)
- **NumPy** (array operations)

## How It Works
1. User uploads an image via the home page.
2. Server saves it under `static/uploads/`.
3. The app generates the sketch:
   - Convert to grayscale
   - Invert grayscale
   - Apply Gaussian blur
   - Invert blurred image
   - Divide grayscale by inverted blur (sketch effect)
4. Output is saved to `static/processed/` with prefix `sketch_`.

## Project Structure
- `AI.py` - Flask application and sketch generation logic
- `requirements.txt` - Python dependencies
- `static/uploads/` - uploaded images (input)
- `static/processed/` - generated sketches (output)

## Setup
### 1) Install dependencies
```bash
pip install -r requirements.txt
```

### 2) Run the app
```bash
python AI.py
```

Then open:
- http://127.0.0.1:5000

## Endpoints
- `GET /` - Upload form
- `POST /upload` - Processes the uploaded image and returns a result page

## Notes
- The app runs in **debug mode** when started directly with `python AI.py`.
- This is intended for local use / development.

## License
Add your license here (e.g., MIT).

