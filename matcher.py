import os
import shutil
from typing import List, Tuple, Optional
import pandas as pd
from deepface import DeepFace

class FaceMatcher:
    def __init__(self, dataset_dir: str = "downloaded_images", matched_images_dir: str = "matched_images"):
        """
        Initialize the FaceMatcher with the directories for dataset images and matched images.
        Ensures that the matched_images directory exists.
        """
        self.dataset_dir = dataset_dir
        self.matched_images_dir = matched_images_dir
        os.makedirs(self.matched_images_dir, exist_ok=True)

    def clear_matched_images_dir(self):
        """
        Clears all files and directories within the matched_images directory.
        """
        for filename in os.listdir(self.matched_images_dir):
            file_path = os.path.join(self.matched_images_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Remove file or link
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Remove directory
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

    def compare_images_deepface(self, test_img_path: str, db_path: str, threshold: float = 0.6) -> Tuple[List[dict], Optional[str]]:
        """
        Performs face matching using DeepFace.

        Parameters:
            test_img_path (str): Path to the test image.
            db_path (str): Directory containing dataset images.
            threshold (float): Threshold value for matching (not used directly in this snippet).

        Returns:
            A tuple where the first element is a list of dictionaries containing match details,
            and the second element is an error message (if any).
        """
        try:
            # Run DeepFace find function to compare the test image with the dataset
            results: List[pd.DataFrame] = DeepFace.find(
                img_path=test_img_path,
                db_path=db_path,
                detector_backend="retinaface",
                align=True
            )

            if len(results) == 0:
                return [], "No matches found."

            df = results[0]
            matched_images = []

            # Iterate through the results DataFrame
            for _, row in df.iterrows():
                distance = row['distance']
                match_rate = 100 * distance  # Calculate match rate as 100 * distance
                matched_image_name = os.path.basename(row['identity'])

                # Append the match details to the list
                matched_images.append({
                    "file_name": matched_image_name,
                    "distance": distance,
                    "match_rate": match_rate
                })

                # Save the matched image to the matched_images directory
                src_path = os.path.join(db_path, matched_image_name)
                dest_path = os.path.join(self.matched_images_dir, matched_image_name)
                shutil.copy(src_path, dest_path)

            return matched_images, None

        except Exception as e:
            return [], str(e)
