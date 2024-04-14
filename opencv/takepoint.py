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
    datatext = open(
        d_dir + str(file_count) + ".csv", "a", newline="")
    filewriter = csv.writer(datatext)
    for categorys in video_main_file:
        file_path = os.path.join(main_dir, categorys)
        list_of_gesture_video = os.listdir(file_path)
        for file in list_of_gesture_video:
            # 迴圈讀取資料夾中影片
            data_count += 1
            write_xy(file_path + "//" + file, filewriter)
            if data_count >= 6400:
                datatext.close()
                file_count += 1
                datatext = open(d_dir + str(file_count) + ".csv","w",newline="",)
                filewriter = csv.writer(datatext)
                data_count = 0
    print("all write finish!")


def write_xy(videopath, filename):
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
                # print(landmark_list)
                frame_landmarks_list.append(landmark_list)
                # print(frame_landmarks_list)
        else:
            break

    if len(frame_landmarks_list) < 13:  # Check the length of landmark_list before writing
        print(videopath+" is not enough data")

    elif len(frame_landmarks_list) > 30:
        print(videopath+" is too much data")

    elif len(frame_landmarks_list) > 21 and len(frame_landmarks_list) <= 30:
        while len(frame_landmarks_list) > 21:
            frame_landmarks_list.pop()
            if len(frame_landmarks_list) > 21:
                frame_landmarks_list.pop(0)
        flat_frame_landmarks_list = sum(frame_landmarks_list, [])
        if "up" in videopath:
            flat_frame_landmarks_list.extend(['1', '0', '0'])
        if "down" in videopath:
            flat_frame_landmarks_list.extend(["0", "1", "0"])
        filename.writerow(flat_frame_landmarks_list)

    elif len(frame_landmarks_list) < 21 and len(frame_landmarks_list) >= 13:
        while len(frame_landmarks_list) < 21:
            first_frame = frame_landmarks_list[0]
            second_frame = frame_landmarks_list[1]
            average_frame = [
                format((float(x) + float(y)) / 2, ".10f")
                for x, y in zip(first_frame, second_frame)
            ]
            frame_landmarks_list.insert(1, average_frame)
        flat_frame_landmarks_list = sum(frame_landmarks_list, [])
        if "up" in os.path.basename(videopath):
            flat_frame_landmarks_list.extend(['1', '0', '0'])
        if "down" in os.path.basename(videopath):
            flat_frame_landmarks_list.extend(["0", "1", "0"])
        filename.writerow(flat_frame_landmarks_list)
    elif len(frame_landmarks_list) == 21:
        flat_frame_landmarks_list = sum(frame_landmarks_list, [])
        if "up" in os.path.basename(videopath):
            flat_frame_landmarks_list.extend(['1', '0', '0'])
        if "down" in os.path.basename(videopath):
            flat_frame_landmarks_list.extend(["0", "1", "0"])
        filename.writerow(flat_frame_landmarks_list)
    # flat_frame_landmarks_list = [
    #     item for sublist in frame_landmarks_list for item in sublist
    # ]
    # filename.writerow(flat_frame_landmarks_list)
    print(videopath+" finish")
    cap.release()
    cv2.destroyAllWindows()
    return 0

if __name__ == "__main__":
    main_dir = "opencv//video"
    s_dir = "opencv"
    write_data_csv(main_dir, s_dir)
    # datatext = open(
    #     s_dir + str(1) + ".csv", "w", newline="")
    # filewriter = csv.writer(datatext)
    # write_xy("opencv//video//up//from_video1_standard_0.mp4", filewriter)
    print("all finish")
