This project demonstrates a real-time hand gesture control system that enhances the gaming experience of Need for Speed. By leveraging MediaPipe for hand landmark detection, OpenCV for image processing, and PyAutoGUI for simulating key presses, the system allows players to intuitively control game actions using their hands.

Key Features:

Real-time hand detection: MediaPipe accurately detects hand landmarks in real-time, providing precise information about hand positions and orientations.
Gesture recognition: The system recognizes specific hand gestures, such as open palms, closed fists, and finger pointing, to map them to corresponding game actions.
Game control integration: Detected gestures are translated into key presses that simulate actions like accelerating, braking, and steering, providing a seamless and interactive gaming experience.
Technologies used:

MediaPipe: A framework for building multimodal applications, used for hand landmark detection.
OpenCV: A computer vision library for image processing and analysis.
PyAutoGUI: A Python library for simulating mouse and keyboard input.
How it works:

Capture video: The system captures video from a webcam or other input device.
Detect hands: MediaPipe's hand landmark detection model is applied to each frame to locate and track hand positions.
Recognize gestures: Specific hand gestures are identified based on the positions of the detected landmarks.
Simulate key presses: Corresponding key presses are simulated using PyAutoGUI, controlling the game's actions.
