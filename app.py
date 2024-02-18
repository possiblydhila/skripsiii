from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
from tensorflow.keras.preprocessing import image
from google.cloud import storage
from PIL import Image
import numpy as np
import tensorflow as tf
import tempfile
import os
import time
from gunicorn.app.base import BaseApplication

app = Flask(__name__)

# Configuration Google Cloud Storage
BUCKET_NAME = 'ember-predict'

# Create Google Cloud Storage client using service account JSON file
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)

# Load the model
model = tf.keras.models.load_model("best_modelBGTTTZ.h5")

class_labels = ['Autistic', 'Non-Autistic']

@app.route('/', methods=['GET'])
def index():
    return "Jalan brow"

@app.route('/predict', methods=['POST'])
def predict():
    # Get the uploaded image
    file = request.files['image']

    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
    temp_path = temp_file.name

    # Save the uploaded file to the temporary location
    file.save(temp_path)

    # Read and preprocess the image
    img = image.load_img(temp_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0

    # Get the start time
    start_time = time.time()

    # Make predictions
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions)
    predicted_label = class_labels[predicted_class]
    confidence_score = predictions[0][predicted_class]

    # Get the end time
    end_time = time.time()

    # Compute the elapsed time
    elapsed_time = end_time - start_time

    # Cleanup: Remove the temporary file
    temp_file.close()
    os.remove(temp_path)

    # Prepare the response
    response = {
        'predicted_label': predicted_label,
        'confidence_score': float(confidence_score),
        'elapsed_time': elapsed_time
    }
    return jsonify(response)

class Server(BaseApplication):
    def _init_(self, app, options=None):
        self.options = options or {}
        self.application = app
        super()._init_()

    def load_config(self):
        for key, value in self.options.items():
            self.cfg.set(key, value)

    def load(self):
        return self.application


if __name__ == '__main__':
    # app.run(debug=True)
    options = {
        'bind': '0.0.0.0:5000',
        'workers': 4 
    }
    server = Server(app, options)
    server.run()
