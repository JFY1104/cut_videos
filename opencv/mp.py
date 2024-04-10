import cv2
import os
import numpy as np
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Get all files in the directory
video_dir = "opencv//video//standard"
video_files = [
    f
    for f in os.listdir(video_dir)
    if os.path.isfile(os.path.join(video_dir, f)) and f.endswith(".mp4")
]

# Initialize a list to store the frame counts
frame_counts = []

# Loop through all video files
for video_file in video_files:
    cap = cv2.VideoCapture(os.path.join(video_dir, video_file))
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_counts.append(frame_count)

# Calculate the average and median frame count
average_frame_count = np.mean(frame_counts)
median_frame_count = np.median(frame_counts)

print(f"The average frame count is {average_frame_count}")
print(f"The median frame count is {median_frame_count}")
# For static images:
# with mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5) as hands:

#     cap = cv2.VideoCapture('output_clip.mp4standard_0.mp4')

#     while cap.isOpened():
#         success, image = cap.read()

#         if not success:
#             print("Ignoring empty camera frame.")
#             break

#         # Flip the image horizontally for a later selfie-view display, and convert
#         # the BGR image to RGB.
#         image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
#         # To improve performance, optionally mark the image as not writeable to
#         # pass by reference.
#         image.flags.writeable = False
#         results = hands.process(image)

#         # Draw the hand annotations on the image.
#         image.flags.writeable = True
#         image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#         if results.multi_hand_landmarks:
#             for hand_landmarks in results.multi_hand_landmarks:
#                 print('Hand landmarks:', hand_landmarks)
#                 mp_drawing.draw_landmarks(
#                     image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

#         cv2.imshow('MediaPipe Hands', image)
#         if cv2.waitKey(3000) & 0xFF == 27:
#             break

#     cap.release()
#     cv2.destroyAllWindows()
