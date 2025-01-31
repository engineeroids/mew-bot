import cv2
import mediapipe as mp
import numpy as np
import math
from movement import xServo, yServo, motorOn, motorOff

# Initialize Mediapipe Face Detection and Drawing
mp_face_detection = mp.solutions.face_detection
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Initialize webcam capture
cap = cv2.VideoCapture(1)

# Set up Face Detection Model
with mp_face_detection.FaceDetection(min_detection_confidence=0.2) as face_detection, \
     mp_hands.Hands(min_detection_confidence=0.2, min_tracking_confidence=0.2) as hands:
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to RGB (Mediapipe requires RGB input)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame for face detection
        face_results = face_detection.process(rgb_frame)
        
        # Process the frame for hand landmarks
        hand_results = hands.process(rgb_frame)

        # Handle face detection
        if face_results.detections:
            for detection in face_results.detections:
                # Get the bounding box
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                x_min = int(bboxC.xmin * iw)
                y_min = int(bboxC.ymin * ih)
                x_max = int((bboxC.xmin + bboxC.width) * iw)
                y_max = int((bboxC.ymin + bboxC.height) * ih)

                # Draw bounding box
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

                # Get the center of the bounding box (normalized coordinates)
                face_center_x = (x_min + x_max) / 2
                face_center_y = (y_min + y_max) / 2

                # Normalize the coordinates between -90 and 90
                norm_x = ((face_center_x / iw) * 180) - 90
                norm_y = ((face_center_y / ih) * 180) - 90

                xServo(-norm_x)
                yServo(-norm_y)

                # Display the coordinates
                cv2.putText(frame, f"X: {norm_x:.2f}, Y: {norm_y:.2f}",
                            (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Handle hand landmarks
        if hand_results.multi_hand_landmarks:
            for handLms in hand_results.multi_hand_landmarks:
                landmarks = handLms.landmark

                # Landmark 0 is the wrist, and landmarks 4, 8, 12, 16, 20 are the fingertips
                wrist_x, wrist_y = int(landmarks[0].x * frame.shape[1]), int(landmarks[0].y * frame.shape[0])
                fingertip_ids = [4, 8, 12, 20]  # Tip of thumb, index, middle, and pinky fingers.

                distances = []
                for tip_id in fingertip_ids:
                    # Get the (x, y) positions of the fingertip
                    tip_x, tip_y = int(landmarks[tip_id].x * frame.shape[1]), int(landmarks[tip_id].y * frame.shape[0])

                    # Calculate the Euclidean distance between wrist (landmark 0) and fingertip
                    distance = math.sqrt((tip_x - wrist_x) ** 2 + (tip_y - wrist_y) ** 2)
                    distances.append(distance)

                    # Analyze the distances to determine if it's a fist or palm
                    threshold_fist = 300  # Adjust this threshold for detecting fist
                    threshold_palm = 500  # Adjust this threshold for detecting palm

                    if all(d > threshold_palm for d in distances):
                        motorOn()
                    else:
                        motorOff()
                        mp_drawing.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
        else:
            motorOff()

        # Show the result in the window
        cv2.imshow("Face and Hand Detection", frame)

        # Exit loop on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close all windows
    cap.release()
    cv2.destroyAllWindows()
