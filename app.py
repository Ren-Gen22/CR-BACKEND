import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from matcher import FaceMatcher

app = Flask(__name__)
CORS(app)
matcher=FaceMatcher()

# Directory to save matched images temporarily
MATCHED_IMAGES_DIR = "matched_images"
DATASET_DIR = "downloaded_images"  # Directory containing the dataset images

@app.route('/upload', methods=['POST'])
def upload_and_search():
    matcher.clear_matched_images_dir()  # Clear the matched_images directory

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        file_path = "uploaded_image.jpg"
        file.save(file_path)

        matched_images, error = matcher.compare_images_deepface(file_path, DATASET_DIR)

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
