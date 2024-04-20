import os
import cv2
import pandas as pd
import mediapipe as mp
import csv
import mediapipe.python.solutions.hands as mpsh
import numpy as np


def shift_frame(frame, dx, dy):
    # 創建轉換矩陣
    M = np.float32([[1, 0, dx], [0, 1, dy]])

    # 進行平移操作
    shifted = cv2.warpAffine(frame, M, (frame.shape[1], frame.shape[0]))

    return shifted


def write_data_csv(main_dir, d_dir):

    with open(d_dir + str(3) + ".csv", "w", newline="") as datatext:
        filewriter = csv.writer(datatext)
        write_xy("opencv//video//down//from_video1_standard_4.mp4", filewriter)
    print("all write finish!")


def write_xy(videopath, filename):
    cap = cv2.VideoCapture(videopath)
    mphands = mpsh
    hands = mphands.Hands()
    frame_landmarks_list = []
    while cap.isOpened():
        ret, frame = cap.read()
        if ret != False:
            frame = shift_frame(frame, 50, 0)
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(imgRGB)
            if result.multi_hand_landmarks:
                landmark_list = []
                for hand in result.multi_hand_landmarks:
                    for landmarks in hand.landmark:
                        x = format(landmarks.x, ".10f")
                        y = format(landmarks.y, ".10f")
                        landmark_list.append(x)
                        landmark_list.append(y)
                    break
                # print(landmark_list)
                frame_landmarks_list.append(landmark_list)
                # print(frame_landmarks_list)
        else:
            break
        cv2.imshow('Frame', frame)

        # 如果按下 'q' 鍵，則退出迴圈
        if cv2.waitKey(200) & 0xFF == ord('q'):
            break
        flat_frame_landmarks_list = sum(frame_landmarks_list, [])
        filename.writerow(flat_frame_landmarks_list)

write_data_csv("opencv//video//down", "opencv")