import cv2
import pandas as pd
import numpy as np
from datetime import time
from PyQt5.QtWidgets import QApplication
import os

def tosecond(t):
    return t.hour * 3600 + t.minute * 60 + t.second
def totime(s):
    return time(hour=int(s/3600), minute=int(s % 3600/60), second=s % 60)
def videoCut(self, inipath, length):
    inipath = inipath.replace('/', os.sep)
    inis = pd.read_excel(inipath, names=['videoindex', 'actionindex', 'action', 'start', 'end', 'X', 'Y', 'W', 'H'])
    path = os.sep.join(inipath.split(os.sep)[:-2])
    excelname = inipath.split(os.sep)[-1]
    if path == '':
        path = '.'
    if len(inipath.split(os.sep)) > 2:
        dirname = inipath.split(os.sep)[-2]
    else:
        dirname = ''
    videoindices = inis['videoindex'].unique()
    lengthlist = length.split(' ')
    assert(len(videoindices) == len(lengthlist))
    if not os.path.exists(path + os.sep + 'after_' + dirname):
        os.mkdir(path + os.sep + 'after_' + dirname)
    for videoindex in videoindices:
        ini = inis[inis['videoindex'] == videoindex]
        ini = ini.reset_index(drop=True)
        length_vedio = int(lengthlist.pop(0))
        video_path = path + os.sep + dirname + os.sep + videoindex + '.mp4'
        videoCapture = cv2.VideoCapture(video_path)
        if videoCapture.isOpened():
            self.textBrowser.append(video_path + ' opened')
            self.textBrowser.append('Total:' + str(videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)) + ' frames.')
        else:
            self.textBrowser.append('Fail to open ' + video_path)
            continue
        fps = videoCapture.get(cv2.CAP_PROP_FPS)
        # fourcc = videoCapture.get(cv2.CAP_PROP_FOURCC)
        # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        start_times = []
        end_times = []
        end_time = 0
        k = 0
        video_writers = []
        while any(ini['start'] > totime(end_time)):
            k = k + 1
            video_writers.append(cv2.VideoWriter(path + os.sep + 'after_' + dirname + os.sep + videoindex + '-' +
                                           str(k).zfill(2) + '.mp4', cv2.VideoWriter_fourcc(*'mp4v'),
                                           fps, (1920, 1080)))
            if not (video_writers[k-1].isOpened()):
                print(video_writers, path + os.sep + 'after_' + dirname + os.sep + videoindex
                      + str(k).zfill(2) + '.mp4')

            start_time = tosecond(min(ini[ini['start'] >= totime(end_time)]['start']))
            end_time = start_time + length_vedio
            end_time_1 = max(ini[(totime(start_time) <= ini['start']) & (ini['start'] < totime(end_time))]['end'])
            end_time_1 = tosecond(end_time_1)
            print(start_time, end_time_1)
            start_times.append(start_time)
            end_times.append(end_time_1)
            indicies = (inis['videoindex'] == videoindex) & (totime(start_time) <= inis['start']) & (
                        inis['start'] < totime(end_time))
            print(indicies)
            inis.loc[indicies, 'videoindex'] = inis[indicies]['videoindex'].apply(lambda x: x + '-' + str(k).zfill(2))
            inis.loc[indicies, 'start'] = inis[indicies]['start'].apply(lambda x: totime(tosecond(x) - start_time + 5))
            inis.loc[indicies, 'end'] = inis[indicies]['end'].apply(lambda x: totime(tosecond(x) - start_time + 5))

        inis.to_excel(path + os.sep + dirname + os.sep + excelname.split('.')[0] + "_new.xlsx",
                      header=['视频编号','行为编号','行为类别','起始时间','截止时间','X','Y','宽','高'],index=False)
        success, frame = videoCapture.read()  # 读取第一帧
        frame_index = 1
        while success:
            for i in range(k):
                if (start_times[i] - 5)*fps < frame_index <= end_times[i]*fps:
                    video_writers[i].write(frame)  # 将截取到的画面写入“新视频”
                    QApplication.processEvents()
            success, frame = videoCapture.read()  # 循环读取下一帧
            frame_index = frame_index + 1
            if frame_index % 10000 == 0:
                self.textBrowser.append('processing frame ' + str(frame_index))
            print(frame_index)
    cv2.destroyAllWindows()


