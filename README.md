# Face Matching API with DeepFace and Flask

This project provides a simple API for face matching using the DeepFace library. It allows users to upload an image and find matching faces from a dataset of images. The API is built using Flask and supports CORS for cross-origin requests.

## Features

- **Face Matching**: Compare an uploaded image with a dataset of images using DeepFace.
- **Image Management**: Temporarily store matched images for retrieval.
- **RESTful API**: Provides endpoints for uploading images and retrieving matched images.

## Requirements

- Python 3.7+
- Flask
- Flask-CORS
- DeepFace
- Pandas
- Shutil
- OS

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Ren-Gen22/CR-BACKEND.git
   cd CR-BACKEND
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare the dataset**:
   Place your dataset images in the `downloaded_images` directory.

## Usage

1. **Run the Flask application**:

```bash
   python app.py
```

2. **Upload an image**:

Use the /upload endpoint to upload an image and find matches.

Example using curl:

```bash
curl -X POST -F "file=@path_to_your_image.jpg" http://localhost:5000/upload
```

Retrieve matched images:

Use the `/matched-images/<filename>` endpoint to retrieve matched images.

Example using curl:

```bash
  curl -O http://localhost:5000/matched-images/matched_image.jpg
```

API Endpoints

    POST /upload: Upload an image to find matching faces.

        Request: Form-data with a file field named file.

        Response: JSON with matched images data or an error message.

    GET /matched-images/<filename>: Retrieve a matched image by filename.

        Response: The matched image file or an error message.

Example Response
json
Copy

{
"matched_images": [
{
"file_name": "matched_image1.jpg",
"distance": 0.45,
"match_rate": 45.0
},
{
"file_name": "matched_image2.jpg",
"distance": 0.50,
"match_rate": 50.0
}
]
}

Configuration

    MATCHED_IMAGES_DIR: Directory to save matched images temporarily.

    DATASET_DIR: Directory containing the dataset images.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
License

This project is licensed under the MIT License. See the LICENSE file for details.
Acknowledgments

    DeepFace for the face recognition library.

    Flask for the web framework.

    Flask-CORS for handling CORS.
