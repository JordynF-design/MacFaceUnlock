import cv2
import os
import glob

recognizer = cv2.face.LBPHFaceRecognizer_create()

images = []
labels = []

for filename in glob.glob("faces/*.jpg"):
    image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

    if image is not None:
        images.append(image)
        labels.append(1)

if not images:
    print("❌ No face samples found.")
    exit()

recognizer.train(images, __import__("numpy").array(labels))

recognizer.write("face_model.yml")

print(f"✅ Model trained with {len(images)} face samples.")
print("🔐 Saved as face_model.yml")
