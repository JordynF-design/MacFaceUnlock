import cv2
import time

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("❌ Could not open the camera.")
    exit()

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

print("🔐 Liveness test started.")
print("Move your head LEFT, then RIGHT.")
print("Press Q to quit.")

left_seen = False
right_seen = False
start_time = time.time()

while True:
    success, frame = camera.read()

    if not success:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(100, 100)
    )

    message = "Move your head LEFT"

    if len(faces) > 0:
        x, y, w, h = faces[0]

        center_x = x + w // 2
        frame_center = frame.shape[1] // 2

        # Detect movement relative to the center of the camera.
        if center_x < frame_center - 60:
            left_seen = True

        if center_x > frame_center + 60:
            right_seen = True

        if not left_seen:
            message = "Move your head LEFT"
        elif not right_seen:
            message = "Now move your head RIGHT"
        else:
            message = "LIVENESS VERIFIED!"

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

    cv2.putText(
        frame,
        message,
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 0),
        2
    )

    cv2.imshow("Mac Face Unlock - Liveness Test", frame)

    if left_seen and right_seen:
        cv2.waitKey(1500)
        break

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()

if left_seen and right_seen:
    print("✅ LIVENESS VERIFIED!")
else:
    print("❌ Liveness test cancelled or incomplete.")
