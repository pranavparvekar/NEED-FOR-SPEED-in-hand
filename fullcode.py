import cv2
import mediapipe as mp
import pyautogui

# Initialize MediaPipe and PyAutoGUI
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Initialize variables to track key states
keys_pressed = {'up': False, 'down': False, 'left': False, 'right': False}

# Define a function to get pixel coordinates
def get_pixel_coords(landmark, width, height):
    return int(landmark.x * width), int(landmark.y * height)

with mp_hands.Hands(
        max_num_hands=2,  # Allow two hands
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7) as hands:

    while True:
        success, frame = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Flip the frame horizontally for a mirror-like effect
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(frame_rgb)

        # Initialize gesture flags
        is_open_hand = False
        is_closed_fists = False
        hand_position_left = None  # Can be 'left', 'right', or 'center'

        if result.multi_hand_landmarks:
            landmarks_list = []
            # Get the coordinates of the left and right hands
            for hand_landmarks, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get image dimensions
                h, w, _ = frame.shape
                landmarks_list.append([hand_landmarks, handedness.classification[0].label])

            if len(landmarks_list) == 2:  # If two hands are detected
                hand1_landmarks, hand1_label = landmarks_list[0]
                hand2_landmarks, hand2_label = landmarks_list[1]

                # Right and left hands detection
                if hand1_label == 'Left':
                    left_hand_landmarks = hand1_landmarks
                    right_hand_landmarks = hand2_landmarks
                else:
                    left_hand_landmarks = hand2_landmarks
                    right_hand_landmarks = hand1_landmarks

                # Get coordinates for wrists and thumbs
                left_wrist_x, left_wrist_y = get_pixel_coords(left_hand_landmarks.landmark[0], w, h)
                right_wrist_x, right_wrist_y = get_pixel_coords(right_hand_landmarks.landmark[0], w, h)

                left_thumb_x, left_thumb_y = get_pixel_coords(left_hand_landmarks.landmark[4], w, h)
                right_thumb_x, right_thumb_y = get_pixel_coords(right_hand_landmarks.landmark[4], w, h)

                # Check if hands are closed
                left_fingers_closed = all([left_hand_landmarks.landmark[i].y > left_hand_landmarks.landmark[i - 2].y for i in [8, 12, 16, 20]])
                right_fingers_closed = all([right_hand_landmarks.landmark[i].y > right_hand_landmarks.landmark[i - 2].y for i in [8, 12, 16, 20]])

                # Determine gestures
                both_hands_open = not left_fingers_closed and not right_fingers_closed
                both_hands_closed = left_fingers_closed and right_fingers_closed
                right_open_left_closed = not right_fingers_closed and left_fingers_closed
                left_open_right_closed = not left_fingers_closed and right_fingers_closed

                # Thumb up detection (for reverse directions)
                left_thumb_up = left_thumb_y < left_hand_landmarks.landmark[3].y
                right_thumb_up = right_thumb_y < right_hand_landmarks.landmark[3].y

            # Perform actions based on gestures
            # Accelerate
            if both_hands_open and not keys_pressed['up']:
                pyautogui.keyDown('up')
                keys_pressed['up'] = True
            elif not both_hands_open and keys_pressed['up']:
                pyautogui.keyUp('up')
                keys_pressed['up'] = False

            # Reverse
            if both_hands_closed and not keys_pressed['down']:
                pyautogui.keyDown('down')
                keys_pressed['down'] = True
            elif not both_hands_closed and keys_pressed['down']:
                pyautogui.keyUp('down')
                keys_pressed['down'] = False

            # Steer Right
            if right_open_left_closed and not keys_pressed['right']:
                pyautogui.keyDown('right')
                keys_pressed['right'] = True
            elif not right_open_left_closed and keys_pressed['right']:
                pyautogui.keyUp('right')
                keys_pressed['right'] = False

            # Steer Left
            if left_open_right_closed and not keys_pressed['left']:
                pyautogui.keyDown('left')
                keys_pressed['left'] = True
            elif not left_open_right_closed and keys_pressed['left']:
                pyautogui.keyUp('left')
                keys_pressed['left'] = False

            # Reverse Left
            if left_thumb_up and not keys_pressed['left']:
                pyautogui.keyDown('down')
                pyautogui.keyDown('left')
                keys_pressed['down'] = True
                keys_pressed['left'] = True
            elif not left_thumb_up and (keys_pressed['down'] and keys_pressed['left']):
                pyautogui.keyUp('down')
                pyautogui.keyUp('left')
                keys_pressed['down'] = False
                keys_pressed['left'] = False

            # Reverse Right
            if right_thumb_up and not keys_pressed['right']:
                pyautogui.keyDown('down')
                pyautogui.keyDown('right')
                keys_pressed['down'] = True
                keys_pressed['right'] = True
            elif not right_thumb_up and (keys_pressed['down'] and keys_pressed['right']):
                pyautogui.keyUp('down')
                pyautogui.keyUp('right')
                keys_pressed['down'] = False
                keys_pressed['right'] = False

            # Display gesture info on frame
            cv2.putText(frame, f'Gesture: {"Accelerate" if both_hands_open else "Reverse" if both_hands_closed else "None"}',
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(frame, f'Steering: {"Right" if right_open_left_closed else "Left" if left_open_right_closed else "None"}',
                        (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        else:
            # Release all keys if no hand is detected
            for key in keys_pressed:
                if keys_pressed[key]:
                    pyautogui.keyUp(key)
                    keys_pressed[key] = False

        # Display the resulting frame
        cv2.imshow('NFS Hand Gesture Control', frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release resources
cap.release()
cv2.destroyAllWindows()


