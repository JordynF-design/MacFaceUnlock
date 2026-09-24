# Mac Face Authentication

A local webcam-based facial authentication prototype built with Python and OpenCV.

## Features

- Real-time face detection using OpenCV
- Local facial recognition using an LBPH model
- Automatic face verification
- Multiple matching frames required before access is granted
- Tkinter graphical interface
- Local processing — facial verification is performed on the computer
- Liveness verification prototype

## How It Works

1. The webcam captures video.
2. OpenCV detects a face.
3. The trained LBPH model compares the detected face with the enrolled face.
4. Multiple matching frames are required.
5. If the face meets the recognition threshold, access is granted.

## Technologies

- Python
- OpenCV
- OpenCV Contrib
- Tkinter
- LBPH Face Recognition
- macOS
- Git/GitHub

## Project Structure

```text
MacFaceUnlock/
├── app_v2.py
├── face_unlock_v2.py
├── face_model.yml
├── enroll.py
├── train.py
├── face_detect.py
├── camera_test.py
├── liveness.py
├── .gitignore
└── README.md