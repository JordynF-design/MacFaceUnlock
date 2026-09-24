import cv2
import os

os.makedirs("faces", exist_ok=True)

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("❌ Could not open the camera.")
    exit()

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

count = 0

print("📸 Enrollment started.")
print("Look at the camera and slowly move your head.")
print("Press Q to stop.")

while count < 30:
    success, frame = camera.read()

    if not success:
        print("❌ Could not read camera.")
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

        filename = f"faces/user_{count:02d}.jpg"
        cv2.imwrite(filename, face)
        count += 1

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"Samples: {count}/30",
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    cv2.imshow("Mac Face Unlock - Enrollment", frame)

    if cv2.waitKey(100) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()

print(f"✅ Enrollment complete: {count} face samples saved.")
