import os
import cv2
import pandas as pd
import mediapipe as mp
import csv
import mediapipe.python.solutions.hands as mpsh
def write_data_csv(main_dir, d_dir):
    video_main_file = os.listdir(main_dir)
    data_count = 0
    file_count = 1  
    for categorys in video_main_file:
        file_path = os.path.join(main_dir, categorys)
        list_of_gesture_video = os.listdir(file_path)
        for file in list_of_gesture_video:
            # 迴圈讀取資料夾中影片
            data_count += 1
            with open(d_dir + str(file_count) + ".csv", "a", newline="") as datatext:
                filewriter = csv.writer(datatext)
                write_abnormal_data(file_path + "//" + file, filewriter)
            if data_count >= 6400:
                datatext.close()
                file_count += 1
                data_count = 0
    print("all write finish!")

def write_abnormal_data(videopath, filewriter):
    cap = cv2.VideoCapture(videopath)
    mphands = mpsh
    hands = mphands.Hands()
    frame_landmarks_list = []

    while cap.isOpened():
        ret, frame = cap.read()
        if ret != False:
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
                frame_landmarks_list.append(landmark_list)

                if len(frame_landmarks_list) == 21:
                    # 寫入 CSV
                    filewriter.writerow(frame_landmarks_list)
                    flat_frame_landmarks_list = sum(frame_landmarks_list, [])
                    flat_frame_landmarks_list.extend(['0', '0', '1'])
                    # 將起始幀向前移動一個位置
                    frame_landmarks_list.pop(0)
        else:
            break

    cap.release()