import cv2
import os
import numpy as np
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Get all files in the directory
video_dir = "opencv//video//down"
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

video_dir = "opencv//video//up"
video_files = [
    f
    for f in os.listdir(video_dir)
    if os.path.isfile(os.path.join(video_dir, f)) and f.endswith(".mp4")
]
for video_file in video_files:
    cap = cv2.VideoCapture(os.path.join(video_dir, video_file))
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_counts.append(frame_count)


# Calculate the average and median frame count
average_frame_count = np.mean(frame_counts)
median_frame_count = np.median(frame_counts)
std_dev_frame_count = np.std(frame_counts)
print(f"The standard deviation of frame count is {std_dev_frame_count}")
print(f"The average frame count is {average_frame_count}")
print(f"The median frame count is {median_frame_count}")
