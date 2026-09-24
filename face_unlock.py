import cv2
import sys

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("CAMERA_ERROR")
    sys.exit(1)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("face_model.yml")

left_seen = False
right_seen = False
verified = False

print("MAC FACE UNLOCK")
print("Look at the camera.")
print("Move your head LEFT, then RIGHT.")

while True:
    ret, frame = camera.read()

    if not ret:
        print("CAMERA_ERROR")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(80, 80)
    )

    for (x, y, w, h) in faces:
        center_x = x + w // 2

        # Detect head movement
        if center_x < frame.shape[1] // 2 - 50:
            left_seen = True

        if center_x > frame.shape[1] // 2 + 50:
            if left_seen:
                right_seen = True

        # Face recognition
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (200, 200))

        label, confidence = recognizer.predict(face)

        if label == 1 and confidence < 70 and left_seen and right_seen:
            verified = True

        if verified:
            message = "VERIFIED - ACCESS GRANTED"
            text_color = (0, 255, 0)
        else:
            message = "Move your head LEFT, then RIGHT."
            text_color = (255, 255, 255)

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            text_color,
            2
        )

        cv2.putText(
            frame,
            message,
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            text_color,
            2
        )

    cv2.imshow("Mac Face Unlock", frame)

    # Once verified, show result briefly and exit
    if verified:
        print("VERIFIED - ACCESS GRANTED")
        cv2.waitKey(1500)
        break

    # Press Q to cancel
    if cv2.waitKey(1) & 0xFF == ord("q"):
        print("CANCELLED")
        break

camera.release()
cv2.destroyAllWindows()
