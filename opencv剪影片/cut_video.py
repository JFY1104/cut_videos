import cv2
import mediapipe as mp
import os
import csv

def clip_video(video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video file")
        return

    start_frames = []
    end_frames = []
    selecting_start = True

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Video", frame)

        key = cv2.waitKey(100) & 0xFF
        if key == ord('q'):
            if selecting_start:
                start_frames.append(cap.get(cv2.CAP_PROP_POS_FRAMES))
                selecting_start = False
                print("Start frame selected:", start_frames[-1])
            else:
                end_frames.append(cap.get(cv2.CAP_PROP_POS_FRAMES))
                selecting_start = True
                print("End frame selected:", end_frames[-1])
        elif key == ord('w'):
            break

    with open('selected_segments.csv', 'w', newline='') as csvfile:
        with open('selected_segments.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write filename
            filename = os.path.basename(video_path)
            writer.writerow([filename])

            # Write start frames
            writer.writerow(['start_frame'] + start_frames)

            # Write end frames
            writer.writerow(['end_frame'] + end_frames)

    # ... existing code ...
    cap.release()
    cv2.destroyAllWindows()
    output_clips(video_path, os.path.join(output_path, "standard/_standard"), start_frames, end_frames)


    # for shift_frames in [1,3,5,7,9]:

    #     start_frames_shifted = [frame - shift_frames for frame in start_frames]
    #     end_frames_shifted = [frame - shift_frames for frame in end_frames]
    #     output_clips(video_path, os.path.join(output_path, f"forward/{video_path}_forward{shift_frames}frames"), start_frames_shifted, end_frames_shifted)

    #     start_frames_shifted = [frame + shift_frames for frame in start_frames]
    #     end_frames_shifted = [frame + shift_frames for frame in end_frames]
    #     output_clips(video_path, os.path.join(output_path, f"backward/{video_path}_backward{shift_frames}frames"), start_frames_shifted, end_frames_shifted)



def output_clips(video_path, output_path, start_frames, end_frames):
    for i in range(len(start_frames)):
        start_frame = start_frames[i]
        end_frame = end_frames[i]

        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if start_frame < 0:
            print("End frame exceeds total frames. Skipping clip.")
            continue
        if end_frame > total_frames:
            print("End frame exceeds total frames. Skipping clip.")
            continue
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        frame_count = end_frame - start_frame

        out = cv2.VideoWriter(f"{output_path}_{i}part.mp4", cv2.VideoWriter_fourcc(*'mp4v'), cap.get(cv2.CAP_PROP_FPS), (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

        while frame_count > 0:
            ret, frame = cap.read()
            if not ret:
                break

            out.write(frame)
            frame_count -= 1

        cap.release()
        out.release()

        print(f"Video clip {i} saved to:", f"{output_path}_{i}.mp4")

# Usage example
clip_video("1.mp4", "video")



