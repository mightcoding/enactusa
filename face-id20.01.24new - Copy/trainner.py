# path/filename: face_recognition_training.py
import os
import cv2
import numpy as np
from PIL import Image

# Initialize the face recognizer (LBPHFaceRecognizer)
recognizer = cv2.face.LBPHFaceRecognizer_create()
path = 'static/photos'

def getImagesWithID(path):
    # Ensure the path exists
    if not os.path.exists(path):
        print(f"The directory {path} does not exist.")
        return None, None

    # List all .png files in the directory
    image_paths = os.listdir("static\photos")
    faces = []
    IDs = []

    for image_path in image_paths:
        # Open the image and convert to grayscale
        face_img = Image.open(f"static\photos\{image_path} ").convert('L')
        face_np = np.array(face_img, 'uint8')

        # Extract ID from filename
        try:
            ID = int(image_path[:image_path.index("_")])
            print(ID)
        except ValueError:
            # Skip files that don't follow the expected naming convention
            print(f"Skipping file {image_path} due to naming convention.")
            continue

        faces.append(face_np)
        IDs.append(ID)

    if not faces:
        print("No valid images found.")
        return None, None

    print("Image processing complete.")
    return np.array(IDs), faces

# Only proceed if the path is correct and contains images
IDs, faces = getImagesWithID(path)
if IDs is not None and faces is not None:
    recognizer.train(faces, IDs)
    # Ensure the recognizer directory exists
    if not os.path.exists('recognizer'):
        os.makedirs('recognizer')
    recognizer.save('recognizer/trainingData.yml')
    print("Training complete and data saved.")
else:
    print("Training could not be completed due to previous errors.")
