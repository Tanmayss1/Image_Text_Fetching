from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import cv2
import pytesseract
from PIL import Image

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config['UPLOAD_FOLDER'] = 'uploads/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def extract_text(image_path):
    try:
        # Open image using PIL (Python Imaging Library)
        img = Image.open(image_path)
        # Convert image to grayscale
        img_gray = img.convert('L')
        # Use Tesseract to extract text
        extracted_text = pytesseract.image_to_string(img_gray)
        return extracted_text
    except Exception as e:
        print("Error processing image:", e)
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_text = None
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            # Save the uploaded file temporarily
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(file_path)
            # Extract text from the uploaded image
            extracted_text = extract_text(file_path)
            # Remove the temporary file after processing
            os.remove(file_path)
            
    return render_template('index.html', extracted_text=extracted_text)

if __name__ == "__main__":
    app.run(debug=True)
