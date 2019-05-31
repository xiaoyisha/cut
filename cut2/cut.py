import cv2
import pandas as pd
import random
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
    if not type(inis['start'][0]) == time:
        inis['start'] = pd.to_datetime(inis['start']).dt.time
        inis['end'] = pd.to_datetime(inis['end']).dt.time
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
        height = videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        width = videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)
        # fourcc = videoCapture.get(cv2.CAP_PROP_FOURCC)
        # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        start_times = []
        end_times = []
        end_time = 0
        k = 0
        video_writers = []
        while any(ini['start'] > totime(end_time)):
            k = k + 1
            ranint = random.randint(1, 10)
            video_writers.append(cv2.VideoWriter(path + os.sep + 'after_' + dirname + os.sep + videoindex + '-' +
                                           str(k).zfill(2) + '.mp4', cv2.VideoWriter_fourcc(*'mp4v'),
                                           fps, (int(width),int(height))))
            if not (video_writers[k-1].isOpened()):
                print(video_writers, path + os.sep + 'after_' + dirname + os.sep + videoindex
                      + str(k).zfill(2) + '.mp4')
            start_time = min(ini[ini['start'] >= totime(end_time)]['start'])
            start_time_1 = tosecond(start_time) - ranint
            if start_time_1 < 0:
                start_time_1 = 0
            end_time = start_time_1 + length_vedio
            end_time_1 = max(ini[(start_time <= ini['start']) & (ini['start'] < totime(end_time))]['end'])
            end_time_1 = tosecond(end_time_1) if tosecond(end_time_1) > end_time else end_time
            start_times.append(start_time_1)
            end_times.append(end_time_1)
            indicies = (inis['videoindex'] == videoindex) & (start_time <= inis['start']) & (
                        inis['start'] < totime(end_time))
            inis.loc[indicies, 'videoindex'] = inis[indicies]['videoindex'].apply(lambda x: x + '-' + str(k).zfill(2))
            inis.loc[indicies, 'start'] = inis[indicies]['start'].apply(lambda x: totime(tosecond(x) - start_time_1))
            inis.loc[indicies, 'end'] = inis[indicies]['end'].apply(lambda x: totime(tosecond(x) - start_time_1))
        inis['duration'] = inis.apply(lambda row:tosecond(row['end']) - tosecond(row['start']), axis=1)
        inis = inis[['videoindex', 'actionindex', 'action', 'start', 'end', 'duration', 'X', 'Y', 'W', 'H']]
        success, frame = videoCapture.read()  # 读取第一帧
        frame_index = 1
        assert(k==len(video_writers))
        while success:
            for i in range(k):
                if start_times[i] * fps < frame_index <= end_times[i] * fps:
                    video_writers[i].write(frame)  # 将截取到的画面写入“新视频”
                    QApplication.processEvents()
            success, frame = videoCapture.read()  # 循环读取下一帧
            frame_index = frame_index + 1
            if frame_index % 100 == 0:
                print(frame_index)
            if frame_index % 10000 == 0:
                self.textBrowser.append('Processing frame ' + str(frame_index))
            if all([frame_index > x*fps for x in end_times]):
                break
        for i in range(len(video_writers)):
            video_writers[i].release()
    inis.to_excel(path + os.sep + 'after_' + dirname + os.sep + excelname.split('.')[0] + "_new.xlsx",
                  header=['视频编号', '行为编号', '行为类别', '起始时间', '截止时间', '持续时间', 'X', 'Y', '宽', '高'], index=False)
    cv2.destroyAllWindows()


