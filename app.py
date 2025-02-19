from deepface import DeepFace
import pandas as pd
import os
import shutil
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from typing import List


app = Flask(__name__)
CORS(app)

# Directory to save matched images temporarily
MATCHED_IMAGES_DIR = "matched_images"
DATASET_DIR = "downloaded_images"  # Directory containing the dataset images

# Ensure the directory exists
os.makedirs(MATCHED_IMAGES_DIR, exist_ok=True)

# Function to clear the matched_images directory
def clear_matched_images_dir():
    for filename in os.listdir(MATCHED_IMAGES_DIR):
        file_path = os.path.join(MATCHED_IMAGES_DIR, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove the file
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Remove the directory
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

# Function to perform face matching using DeepFace
def compare_images_deepface(test_img_path, db_path, threshold=0.6):
    try:
        results: List[pd.DataFrame] = DeepFace.find(
            img_path=test_img_path,
            db_path=db_path,
            detector_backend="retinaface",
            align=True
        )

        if len(results) == 0:
            return [], "No matches found."

        df = results[0]

        # Prepare matched images data with distance and calculated match rate
        matched_images = []
        for _, row in df.iterrows():
            distance = row['distance']
            match_rate = 100 * distance  # Calculate match rate as 100 * distance

            matched_image_name = os.path.basename(row['identity'])
            matched_images.append({
                "file_name": matched_image_name,
                "distance": distance,
                "match_rate": match_rate
            })

            # Save matched image to the matched_images directory
            src_path = os.path.join(db_path, matched_image_name)
            dest_path = os.path.join(MATCHED_IMAGES_DIR, matched_image_name)
            shutil.copy(src_path, dest_path)

        return matched_images, None

    except Exception as e:
        return [], str(e)

@app.route('/upload', methods=['POST'])
def upload_and_search():
    clear_matched_images_dir()  # Clear the matched_images directory

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        file_path = "uploaded_image.jpg"
        file.save(file_path)

        matched_images, error = compare_images_deepface(file_path, DATASET_DIR)

        if error:
            return jsonify({"error": error}), 500

        if matched_images:
            response_data = {
                "matched_images": matched_images
            }
            print(f"Matched images: {response_data}")
            return jsonify(response_data), 200
        else:
            return jsonify({"message": "No match found using DeepFace."}), 200

@app.route('/matched-images/<filename>', methods=['GET'])
def get_matched_image(filename):
    file_path = os.path.join(MATCHED_IMAGES_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='image/jpeg')
    else:
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
