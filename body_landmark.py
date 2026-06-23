import cv2
import mediapipe as mp

# Step 1: Load MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Step 2: Make lines and points thick
landmark_style = mp_drawing.DrawingSpec(thickness=5, circle_radius=5,color=(255,0,0))
connection_style = mp_drawing.DrawingSpec(thickness=5,color=(0,0,255))

# Step 3: Start pose detection
pose = mp_pose.Pose()

# Step 4: Start webcam
cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Step 5: Convert image to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Step 6: Detect body
    result = pose.process(rgb)

    # Step 7: Draw body skeleton
    if result.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame,
            result.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=landmark_style,
            connection_drawing_spec=connection_style
        )

    # Step 8: Show output
    cv2.imshow("Body Tracking", frame)

    # Press 'q' to stop
    if cv2.waitKey(1) == ord('q'):
        break

# Step 9: Close everything
cap.release()
cv2.destroyAllWindows()