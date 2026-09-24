# Mac Face Authentication

A local facial authentication prototype built with Python and OpenCV.

## Project Overview

This project demonstrates how facial recognition and liveness verification can be combined to create a local authentication system.

The application uses the Mac's camera to detect and recognize a registered face and performs a basic liveness check before granting access.

## Features

- Face detection using OpenCV
- Facial recognition using LBPH
- Face enrollment with camera samples
- Basic liveness verification
- Graphical authentication interface
- Local authentication without a cloud service
- Git/GitHub version control

## Technologies

- Python
- OpenCV
- OpenCV Contrib
- Tkinter
- Git
- GitHub

## Project Structure

```text
MacFaceUnlock/
├── app.py
├── app_v2.py
├── app_working_backup.py
├── camera_test.py
├── enroll.py
├── face_detect.py
├── face_unlock.py
├── face_unlock_v2.py
├── face_unlock_working_backup.py
├── liveness.py
├── recognize.py
├── train.py
├── README.md
└── .gitignore
