import cv2
import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv('cut3_test.csv')
    file_path = df['video'][0]
    print("opecv video")
    cap = cv2.VideoCapture(file_path)
    if cap.isOpened():
        print(file_path + ' opened')
    else:
        print('Fail to open ' + file_path)
        exit()
    fps = cap.get(cv2.CAP_PROP_FPS)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),  int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    index = 0
    for row in df.iterrows():
        output = df['direction'][index]
        videoWriter = cv2.VideoWriter(file_path + "_"+ output +".mp4",cv2.VideoWriter_fourcc("I", "4", "2", "0"), fps, size)
        if(videoWriter.isOpened()):
            print('VideoWriter is opened')
        start_frame = 0
        time = 3600
        for t in df['start'][index].split(':'):
            start_frame = start_frame + int(t) * time * fps
            time = time / 60
        time = 3600
        end_frame = 0
        for t in df['end'][index].split(':'):
            end_frame = end_frame + int(t) * time * fps
            time = time / 60
        success, frame = cap.read()  # 读取第一帧
        frame_index = 1
        while success:
            if start_frame < frame_index <= end_frame:
                videoWriter.write(frame)  # 将截取到的画面写入“新视频”
            success, frame = cap.read()  # 循环读取下一帧
            frame_index = frame_index + 1
        videoWriter.release()
        index+=1
    cap.release()