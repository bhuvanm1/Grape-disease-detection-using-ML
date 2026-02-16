import os
import random
from flask import Flask, render_template, request, session, redirect, url_for
# --- KERAS LOADING ---
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# --- Path Fix for Hugging Face/Render ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key_for_local_testing_123')

# --- LOAD AI MODEL ---
MODEL_PATH = os.path.join(BASE_DIR, 'grapecare_model.keras')
try:
    model = load_model(MODEL_PATH)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ ERROR: Could not load model from {MODEL_PATH}")
    print(f"Details: {e}")
    model = None

CLASS_NAMES = ['black_rot', 'esca', 'healthy', 'leaf_blight']

def predict_image(image_path):
    """Predicts the image and returns a result dictionary."""
    if model is None: 
        print("❌ Prediction failed: Model is not loaded.")
        return {'label_key': 'error', 'confidence': 0.0, 'severity': 0}
    try:
        img = image.load_img(image_path, target_size=(224, 224))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        print("Running prediction...")
        prediction = model.predict(img_array)[0]
        
        class_index = np.argmax(prediction)
        confidence = np.max(prediction)
        label_key = CLASS_NAMES[class_index]

        if label_key == 'healthy':
            severity = 0
        else:
            # Simple severity calculation (adjust as needed)
            severity = int((confidence - 0.3) * 120)
            severity = max(15, min(95, severity)) # Clamp between 15% and 95%

        print(f"Prediction successful: {label_key} ({confidence*100:.2f}%)")
        return {
            'label_key': label_key,
            'confidence': float(confidence),
            'severity': severity
        }
    except Exception as e:
        print(f"❌ Prediction Error: {e}")
        return {'label_key': 'error', 'confidence': 0.0, 'severity': 0}

@app.route('/')
def index():
    """Serves the main page, only for the initial load."""
    print("GET /: Loading main page.")
    # This page is now ONLY for the initial load, without results.
    return render_template('index.html', result=None, error_msg=None)

@app.route('/predict', methods=['POST'])
def predict():
    """Handles file upload, prediction, and renders the result directly."""
    print("POST /predict: Received upload.")
    
    if 'file' not in request.files:
        print("❌ /predict Error: 'file' not in request.files")
        # Don't use session or redirect. Render the page directly with the error.
        return render_template('index.html', result=None, error_msg='No file uploaded.')

    file = request.files['file']
    if file.filename == '':
        print("❌ /predict Error: file.filename is empty")
        # Render the page directly with the error.
        return render_template('index.html', result=None, error_msg='No file selected.')

    if file:
        try:
            # Save file to the /tmp folder which is writable on Hugging Face
            file_path = os.path.join('/tmp', 'temp_image.jpg')
            print(f"Saving temporary file to {file_path}")
            file.save(file_path)
            
            # Run the prediction
            prediction_result = predict_image(file_path)
            
            # Render the page directly with the prediction result
            print(f"Rendering page with result: {prediction_result['label_key']}")
            return render_template('index.html', result=prediction_result, error_msg=None)
        
        except Exception as e:
            print(f"❌ /predict Fatal Error: {e}")
            return render_template('index.html', result=None, error_msg=f'An internal error occurred: {e}')

if __name__ == '__main__':
    # Runs the app on port 7860, which is the standard for HF Spaces
    app.run(host='0.0.0.0', port=7860)