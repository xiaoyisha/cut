import pandas as pd
import cv2

# 优化后
# 注意，没有改变视频编码格式
inipath = 'cut3_test.xlsx'
inis = pd.read_excel(inipath, names=['videoindex', 'direction', 'start', 'end'],
                     dtype=str)
videoindices = inis['videoindex'].unique()
inilist = []
for videoindex in videoindices:
    inilist.append(inis[inis['videoindex'] == videoindex])
# print(inilist)
cnt = 0
for ini in inilist:
    ini = ini.reset_index(drop=True)  # ini是每一个视频单独对应的几行
    print(cnt)
    print(ini)
    cnt += 1
    video_name = ini['videoindex'][0]
    video_path = '8_20_record/' + video_name + '.mp4'
    videoCapture = cv2.VideoCapture(video_path)
    if videoCapture.isOpened():
        print(video_path + ' opened')
    else:
        print('Fail to open ' + video_path)
        continue
    fps = videoCapture.get(cv2.CAP_PROP_FPS)
    size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    start_frames = []
    end_frames = []
    video_writers = []

    # 下面是分别生成这三个数组
    for i in range(len(ini)):
        start_frame = 0
        time = 3600
        for t in ini.iloc[i]['start'].split(':'):
            start_frame = start_frame + int(t) * time * fps
            time = time / 60
        time = 3600
        end_frame = 0
        for t in ini.iloc[i]['end'].split(':'):
            end_frame = end_frame + int(t) * time * fps
            time = time / 60
        start_frames.append(start_frame)
        end_frames.append(end_frame)
        direction = ini.iloc[i]['direction']
        vw = cv2.VideoWriter('hh' + video_name + "_" + direction + ".mp4", cv2.VideoWriter_fourcc("I", "4", "2", "0"),
                             fps, size)
        if (vw.isOpened()):
            print('VideoWriter is opened')
        video_writers.append(vw)

    success, frame = videoCapture.read()  # 读取第一帧
    frame_index = 1
    while success:
        for i in range(len(ini)):
            if start_frames[i] < frame_index <= end_frames[i]:
                video_writers[i].write(frame)  # 将截取到的画面写入“新视频”
        success, frame = videoCapture.read()  # 循环读取下一帧
        frame_index = frame_index + 1
        print(frame_index)
    for i in range(len(ini)):
        video_writers[i].release()
    videoCapture.release()
