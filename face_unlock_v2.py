import cv2
import os
import time

# -----------------------------
# SETTINGS
# -----------------------------

MODEL_FILE = "face_model.yml"
FACE_CASCADE = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

# Lower confidence = better match with LBPH
MATCH_THRESHOLD = 70

# Number of successful matching frames required
REQUIRED_MATCHES = 8


# -----------------------------
# CHECK FILES
# -----------------------------

if not os.path.exists(MODEL_FILE):
    print("ERROR: face_model.yml was not found.")
    print("Train your face first with: python train.py")
    raise SystemExit


# -----------------------------
# LOAD FACE MODEL
# -----------------------------

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(MODEL_FILE)

face_cascade = cv2.CascadeClassifier(FACE_CASCADE)


# -----------------------------
# OPEN CAMERA
# -----------------------------

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("ERROR: Could not open camera.")
    raise SystemExit


print()
print("================================")
print("       MAC FACE UNLOCK V2")
print("================================")
print()
print("Looking for your face...")
print("No head movement required.")
print()


matches = 0
start_time = time.time()

# Give the camera a little time to start
time.sleep(1)


# -----------------------------
# FACE VERIFICATION LOOP
# -----------------------------

while True:

    success, frame = camera.read()

    if not success:
        print("ERROR: Could not read camera.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(100, 100)
    )

    found_match = False

    for (x, y, w, h) in faces:

        face = gray[y:y+h, x:x+w]

        label, confidence = recognizer.predict(face)

        # LBPH confidence is lower when the face is a better match
        if label == 1 and confidence < MATCH_THRESHOLD:
            found_match = True

            matches += 1

            print(
                f"Face match: {matches}/{REQUIRED_MATCHES} "
                f"(confidence: {confidence:.1f})"
            )

            cv2.rectangle(
                frame,
                (x, y),
                (x+w, y+h),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                "MATCH",
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        else:

            cv2.rectangle(
                frame,
                (x, y),
                (x+w, y+h),
                (0, 0, 255),
                2
            )

            cv2.putText(
                frame,
                "NOT RECOGNIZED",
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )

    if not found_match:
        # Slowly reset if the face disappears
        matches = max(0, matches - 1)

    # -----------------------------
    # ACCESS GRANTED
    # -----------------------------

    if matches >= REQUIRED_MATCHES:

        print()
        print("================================")
        print("      VERIFIED")
        print("      ACCESS GRANTED")
        print("================================")
        print()

        cv2.putText(
            frame,
            "ACCESS GRANTED",
            (40, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.1,
            (0, 255, 0),
            3
        )

        cv2.imshow("Mac Face Unlock V2", frame)

        cv2.waitKey(1200)

        break

    # -----------------------------
    # TIMEOUT
    # -----------------------------

    if time.time() - start_time > 15:

        print()
        print("VERIFICATION FAILED")
        print("Face was not recognized.")
        print()

        break

    cv2.imshow("Mac Face Unlock V2", frame)

    # ESC quits
    key = cv2.waitKey(1) & 0xFF

    if key == 27:
        print("Verification cancelled.")
        break


# -----------------------------
# CLEANUP
# -----------------------------

camera.release()
cv2.destroyAllWindows()