import cv2
import mediapipe as mp

# Initialize MediaPipe
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

height, width = 480, 640    

# Make lines and points thicker
landmark_style = mp_drawing.DrawingSpec(thickness=2, circle_radius=5, color=(255, 0, 0))
connection_style = mp_drawing.DrawingSpec(thickness=2, color=(0, 255, 0))

# Start pose detection
pose = mp_pose.Pose()

# Start webcam
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

while True:
    ret, frame = cap.read()

    # Stop if camera fails
    if not ret:
        break

    # Convert to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process frame
    results = pose.process(rgb)

    # If body detected
    if results.pose_landmarks:

        # Draw skeleton
        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=landmark_style,
            connection_drawing_spec=connection_style
        )

        # Get nose coordinates
        nose = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]

        # Convert normalized → pixel
        h, w, _ = frame.shape
        x = int(nose.x * w)
        y = int(nose.y * h)

        # Print in terminal
        print("Nose:", x, y)


        
    # Show video
    cv2.imshow("Body Tracking + Nose", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) == ord('q'):
        break

# Release everything
cap.release()
cv2.destroyAllWindows()