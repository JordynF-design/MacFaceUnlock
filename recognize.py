import cv2

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("❌ Could not open the camera.")
    exit()

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("face_model.yml")

print("🔐 Face recognition started.")
print("Look at the camera. Press Q to quit.")

while True:
    success, frame = camera.read()

    if not success:
        print("❌ Could not read the camera.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(100, 100)
    )

    for (x, y, w, h) in faces[:1]:
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (200, 200))

        label, confidence = recognizer.predict(face)

        if label == 1 and confidence < 70:
            text = f"MATCHED - {confidence:.1f}"
            status = (0, 255, 0)
        else:
            text = f"UNKNOWN - {confidence:.1f}"
            status = (0, 0, 255)

        cv2.rectangle(frame, (x, y), (x+w, y+h), status, 2)
        cv2.putText(
            frame,
            text,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            status,
            2
        )

    cv2.imshow("Mac Face Unlock - Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
