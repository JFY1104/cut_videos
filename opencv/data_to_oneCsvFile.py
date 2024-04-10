""" Ciallo～(∠・ω< )⌒★ """
import os
import csv
import cv2
import mediapipe.python.solutions.hands as mpsh


def str_to_float(str_list):
    """ 將str list 變 float list """
    float_list = []
    for val in str_list:
        float_list.append(float(val))
    return float_list


def point_to_float(path):
    """ 將data file中的所有資料轉為二維float list """
    list = []
    with open(path) as f:
        reader = csv.reader(f)
        for line in reader:
            list.append(str_to_float(line))
    return list


def pick(landmark, need_frame, rate):
    """ 根據need frame按百分比切分landmark rate:擴張資料用 """
    list = []
    fin = []
    error_flag = False
    total_frame = int(len(landmark))
    gap = int(total_frame*rate/need_frame)+1
    start_frame = 1
    while start_frame+((need_frame-1)*gap) < total_frame:
        list = []
        for i in range(need_frame):
            pick = start_frame+(i*gap)
            if len(landmark[pick]) != 42:
                error_flag = True
                print("error")
                break
            else:
                list += landmark[pick]
        if error_flag:
            error_flag = False
            continue
        else:
            fin.append(list)
        start_frame += 1
    return fin


def gesture_type(file_name):
    """ 製作onehot用 """
    if "上" in file_name:
        return [1, 0, 0, 0]
    elif "下" in file_name:
        return [0, 1, 0, 0]
    elif "開" in file_name:
        return [0, 0, 1, 0]
    elif "關" in file_name:
        return [0, 0, 0, 1]


def pick_and_type(dir_name, need_frame, rate):
    """ 將資料夾中的data取出 切分data 加上類別 """
    files = os.listdir(dir_name)
    fin = []
    for file in files:
        path = os.path.join(dir_name, file)
        landmark = point_to_float(path)
        picked_frame = pick(landmark, need_frame, rate)
        gesture = gesture_type(file)
        print(file)
        for list in picked_frame:
            list += gesture
        fin += picked_frame
    return fin


def write_training_csv(destination_dir, version_name, picked_frame, need_frame, rate):
    """ 將製作好的訓練資料寫入目標資料夾中的csv file"""
    with open(destination_dir+'/'+version_name+'-landmark-'+str(need_frame)+'-'+str(rate)+'.csv', "w", newline="") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(picked_frame)


def data_to_training_csv(source_dir, destination_dir, version_name, need_frame, rate):
    """ 選取來源資料夾中的data並寫入至目的資料夾的csv file中  """
    picked_frame = pick_and_type(source_dir, need_frame, rate)
    print("選取完成")
    write_training_csv(destination_dir, version_name,
                       picked_frame, need_frame, rate)
    print("寫入完成")


def rotate_img(img, angle):
    rows, cols = img.shape[:2]
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    result = cv2.warpAffine(img, M, (cols, rows))
    return result


def write_xy(videopath, datatext):
    cap = cv2.VideoCapture(videopath)
    mphands = mpsh
    hands = mphands.Hands()
    framecount = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if ret != False:
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(imgRGB)
            if result.multi_hand_landmarks:
                for hand in result.multi_hand_landmarks:
                    datatext.write("frame" + str(framecount) + ": ")
                    point = 0
                    for landmarks in hand.landmark:
                        x = int(landmarks.x * frame.shape[1])
                        y = int(landmarks.y * frame.shape[0])
                        str1 = (
                            str(point) + ":" +
                            "[" + str(x) + "," + str(y) + "]" + " "
                        )
                        datatext.write(str1)
                        point += 1
                    framecount += 1
                    datatext.write("\n")

            """ print(frame.shape[0],frame.shape[1])   """
            """ print(result.multi_hand_landmarks) """
            cv2.imshow("c1", frame)
            cv2.waitKey(1)
        else:
            break

    print("finish")
    cap.release()
    cv2.destroyAllWindows()
    return 0

# 讀影片x,y,z座標


def write_xyz(videopath, filename):
    cap = cv2.VideoCapture(videopath)
    mphands = mpsh
    hands = mphands.Hands()
    while cap.isOpened():
        ret, frame = cap.read()
        if ret != False:
            frame = rotate_img(frame, -10)  # 調整旋轉參數
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(imgRGB)
            if result.multi_hand_landmarks:
                landmark_list = []
                for hand in result.multi_hand_landmarks:
                    # lor = hand.classification
                    for landmarks in hand.landmark:
                        x = format(landmarks.x, '.10f')
                        y = format(landmarks.y, '.10f')
                        # z = format(landmarks.z,'.10f')
                        landmark_list.append(x)
                        landmark_list.append(y)
                        # landmark_list.append(z)
                    break
                filename.writerow(landmark_list)
            """ print(frame.shape[0],frame.shape[1])   """
            """ print(result.multi_hand_landmarks) """
            """ cv2.imshow("c1", frame)
            cv2.waitKey(1) """
        else:
            break
    print(videopath)
    print("finish")
    cap.release()
    cv2.destroyAllWindows()
    return 0


def write_data_csv(main_dir, d_dir):
    video_main_file = os.listdir(main_dir)
    for categorys in video_main_file:
        file_path = os.path.join(main_dir, categorys)
        list_of_gesture_video = os.listdir(file_path)
        i = 1
        for file in list_of_gesture_video:
            # 迴圈讀取資料夾中影片
            with open(d_dir+"//"+categorys+"data"+str(i)+".csv", 'w', newline="") as datatext:
                filewriter = csv.writer(datatext)
                write_xy(file_path+"\\"+file, filewriter)  # 修改此行函數以更改所需資料
            i += 1
    print("all write finish!")


if __name__ == '__main__':
    s_dir = 'csv/video_csv'
    d_dir = 'csv/0319csv'
    need_frame = 9
    rate = 0.9
    video_main_dir = ("C://Users//jack3//OneDrive//桌面//opencv剪影片")
    write_data_csv(video_main_dir, d_dir)
    # 自定義版本名稱，避免檔案覆寫
    version_name = '9frame_point'
    # data_to_training_csv(s_dir, d_dir, version_name, need_frame, rate)
