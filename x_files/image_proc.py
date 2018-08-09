'''
多线程图像并发调度
创建时间:Wed Aug  8 20:49:55 BST 2018
作者:Jiang Ren, Zhang Tingyuan
注释:
加入手部识别方法
'''

import threading
import os
import cv2
import numpy as np
import signal
import tkinter
from PIL import Image,imageTk

cam_key_word = 'C270'

class img_proc(object):
    '''img class'''
    is_end = False

    def __init__(self,method='color'):
        '''now start'''
        self.watcher = None
        if method == 'color':
            self.classifier_method = self.class_by_color
        elif method == 'shape':
            self.classifier_method = self.class_by_shape
        elif method == 'motion':
            self.classifier_method = self.class_by_motion

        self.get_img = False
        
        # 找到webcam
        pipe = os.popen('lsusb')
        text = pipe.read()
        if cam_key_word in text:
            text = text.split('\n')
            for line in text:
                if cam_key_word in line:
                    break
            text = line.split(' ')
            self.cam_path = '/dev/bus/usb/' + text[1] + '/' + text[3][:-1]
            print('Found webcam at %s' % self.cam_path)
        else:
            print('Could not find web cam')
            os._exit(1)

        # 创建webcam对象
        cam = cv2.VideoCapture(1)
        self.cam = cam
        # self.cam.open(self.cam_path)
        if self.cam.isOpened():
            print('Successfully opened cam')
        else:
            print('Failed to open cam')
        while True:
            ret, image = cam.read()
            tkinter.
        # thread init
        self.t_classifier = threading.Thread(target=self.classifier_method)
        self.t_reader = threading.Thread(target=self.read_frame)
        
    def run(self):
        # self.t_reader.start()
        # self.t_classifier.start()
        # signal.signal(signal.SIGINT,self.end_proc)
        # print('All threads has been run')
        # self.t_classifier.join()
        # self.t_reader.join()
        # if self.get_img:
        #     cv2.imshow('origin image',self.image)
        pass

    def read_frame(self):
        while True:
            if self.is_end:
                break
            ret, image = self.cam.read()
            if ret:
                self.image = image
                self.get_img = True
                # cv2.imshow('origin image',image)
            else:
                self.get_img = False

    def class_by_color(self):
        '''使用颜色进行分类'''
        yellow_min = [11,43,46]
        yellow_max = [34,255,255]
        blue_min = [100 , 60 , 100]
        blue_max = [120 , 120 , 180]
        black_min = [0, 0, 0]
        black_max = [180, 255, 46]
        white_min = [0,0,221]
        white_max = [180,30,255]
        green_min = [78,43,46]
        green_max = [99,255,255]

        while True:
            if self.is_end:
                break
            if not self.get_img:
                continue
            image = emptyImage = np.zeros(self.image.shape,np.uint8)
            image = self.image.copy()
            h, w, _ = image.shape #读取图像长宽
            #gray = cv2.cvtColor(image , cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(image ,(5,5) ,0)
            image = blur
            #HSV颜色识别，分离手掌和背景
            HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            H, S, V = cv2.split(HSV)
            LowerBlue = np.array(green_min)
            UpperBlue = np.array(green_max)
            mask = cv2.inRange(HSV, LowerBlue, UpperBlue)
            BlueThings = cv2.bitwise_and(image, image, mask=mask)
            
            #二值化
            gray = cv2.cvtColor(BlueThings , cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray ,30, 255, cv2.THRESH_BINARY)[1]
            
            #闭运算，填充孔洞
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))
            closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            #dilated = cv2.dilate(thresh,kernel)
            #轮廓检测
            _,contours,hierarchy = cv2.findContours(closed, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            for i in range(len(contours)):
                cnt = contours[i]
                area = cv2.contourArea(cnt) #计算轮廓面积
                if(area > (h/10*w/10)): #只有大轮廓才被考虑
                    M = cv2.moments(cnt)
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    
                    cv2.circle(image, (cX, cY), 7, (0, 255, 255), -1)
                    str = "center(%d,%d)" %(cX,cY)
                    cv2.putText(image, str, (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
                    cv2.drawContours(image, cnt, -1, (0, 255, 0), 2)
                    continue
                    
            #cv2.drawContours(image, c_max, -1, (255, 255, 255), thickness=-1)
            
            # cv2.imshow('classifier by color', image)
            # cv2.imshow('threshold image', thresh)

    def end_proc(self,a,b):
        cv2.destroyAllWindows()
        self.cam.release()
        self.is_end = True

if __name__ == '__main__':
    proc = img_proc()
    proc.run()