import cv2
import pandas as pd
from PyQt5.QtWidgets import QApplication
import os

def videoCut(self, inipath):
    inipath = inipath.replace('/', os.sep)
    inis = pd.read_excel(inipath, names=['videoindex', 'actionindex', 'action', 'start', 'end', 'X', 'Y', 'W', 'H'],
                         dtype=str)
    path = os.sep.join(inipath.split(os.sep)[:-2])
    if(path == ''):
        path = '.'
    if len(inipath.split(os.sep)) > 2:
        dirname = inipath.split(os.sep)[-2]
    else:
        dirname = ''
    videoindices = inis['videoindex'].unique()
    inilist = []
    if not os.path.exists(path +os.sep+ 'after_' + dirname):
        os.mkdir(path +os.sep+ 'after_' + dirname)
    for videoindex in videoindices:
        inilist.append(inis[inis['videoindex'] == videoindex])
    for ini in inilist:
        ini = ini.reset_index(drop=True)
        video_path = path +os.sep + dirname + os.sep + ini['videoindex'][0] + '.mp4'
        videoCapture = cv2.VideoCapture(video_path)
        if videoCapture.isOpened():
            self.textBrowser.append(video_path + ' opened')
        else:
            self.textBrowser.append('Fail to open ' + video_path)
            continue
        fps = videoCapture.get(cv2.CAP_PROP_FPS)
        fourcc = videoCapture.get(cv2.CAP_PROP_FOURCC)
        self.textBrowser.append('Total:' + str(videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)) + ' frames.')
        #fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        start_frames = []
        end_frames = []
        video_writers = []
        for i in range(len(ini)):
            size = (int(ini.iloc[i]['W']), int(ini.iloc[i]['H']))
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
            video_name = ('-'.join(ini.iloc[i])).replace(':','_')
            video_name = video_name.replace('/','_')
            video_writers.append(cv2.VideoWriter(path +os.sep+ 'after_' + dirname + os.sep + video_name + '.mp4',
                                                 cv2.VideoWriter_fourcc(*'mp4v'), fps, size))
            if not(video_writers[i].isOpened()):
                print(video_writers[i],path +os.sep+ 'after_' + dirname + os.sep + video_name + '.mp4')
        success, frame = videoCapture.read()  # 读取第一帧
        frame_index = 1
        while success:
            for i in range(len(ini)):
                if start_frames[i] < frame_index <= end_frames[i]:
                    framecut = frame[int(ini.iloc[i]['Y']):int(ini.iloc[i]['Y']) + int(ini.iloc[i]['H']),
                               int(ini.iloc[i]['X']):int(ini.iloc[i]['X']) + int(ini.iloc[i]['W'])]  # 截取画面
                    video_writers[i].write(framecut)  # 将截取到的画面写入“新视频”
                    QApplication.processEvents()
            success, frame = videoCapture.read()  # 循环读取下一帧
            frame_index = frame_index + 1
            if frame_index % 10000 == 0:
                self.textBrowser.append('processing frame ' + str(frame_index))
            #print(frame_index)
        for i in range(len(ini)):
            video_writers[i].release()
    cv2.destroyAllWindows()


