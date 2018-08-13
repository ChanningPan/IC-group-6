# -*- coding: utf-8 -*-
import cv2
import os
import numpy as np
import socket
yellow_min = [11,43,46]
yellow_max = [34,255,255]

blue_min = [100 , 128 , 46]
blue_max = [124 , 255 , 255]

black_min = [0, 0, 0]
black_max = [180, 255, 46]

white_min = [0,0,221]
white_max = [180,30,255]
green_min = [78,43,46]
green_max = [99,255,255]
def show_webcam(mirror=False):
    data_ma = data_proc()
    cam = cv2.VideoCapture(0)
    while not cam.isOpened():
        cam.open('/dev/bus/usb/001/02')
    while True:
        ret, image = cam.read()
        h, w, _ = image.shape #读取图像长宽
        if mirror: 
            image = cv2.flip(image, 1)
        #gray = cv2.cvtColor(image , cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(image ,(5,5) ,0)
        image = blur
        #HSV颜色识别，分离手掌和背景
        HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        H, S, V = cv2.split(HSV)
        LowerBlue = np.array(blue_min)
        UpperBlue = np.array(blue_max)
        mask = cv2.inRange(HSV, LowerBlue, UpperBlue)
        BlueThings = cv2.bitwise_and(image, image, mask=mask)
        
        #二值化
        gray = cv2.cvtColor(BlueThings , cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray ,20, 255, cv2.THRESH_BINARY)[1]
        
        #闭运算，填充孔洞
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        #dilated = cv2.dilate(thresh,kernel)
        #轮廓检测
        _,contours,hierarchy = cv2.findContours(closed, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for i in range(len(contours)):
            cnt = contours[i]
            area = cv2.contourArea(cnt) #计算轮廓面积
            if(area > (h/14*w/14)): #只有大轮廓才被考虑
                M = cv2.moments(cnt)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                data_ma.append(cX,cY)
                
                cv2.circle(image, (cX, cY), 7, (0, 255, 255), -1)
                str = "center(%d,%d)" %(cX,cY)
                cv2.putText(image, str, (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
                cv2.drawContours(image, cnt, -1, (0, 255, 0), 2)
                continue
                
        #cv2.drawContours(image, c_max, -1, (255, 255, 255), thickness=-1)
        
        cv2.imshow('my webcam', image)
        cv2.imshow('my webcam2', thresh)
        
        if cv2.waitKey(1) == 27: 
            break  # esc to quit
    cv2.destroyAllWindows()
    cam.release()

class data_proc(object):
    def __init__(self):
        self.count = 0
        self.max = 10 # ke geng gai

        self.x_list = []
        self.y_list = []
        self.x_avg = 0
        self.y_avg = 0
        
        pc_addr = '192.168.43.21'
        self.sk = socket.socket()
        self.sk.connect((pc_addr,6666))
    def average(self):
        amountx = 0
        amounty = 0
        print(self.x_list,self.y_list)
        for x in self.x_list:
            amountx += x
        self.x_avg = int(amountx/self.max)
        for y in self.y_list:
            amounty += y
        self.y_avg = int(amounty/ self.max)
        print("x avg =",self.x_avg)
        print ("y avg = ",self.y_avg)
        pass

    def append(self,x,y):
        self.x_list.append(x)
        self.y_list.append(y)
        self.count += 1
        if self.count >= self.max:
            self.average()
            self.send() 
            self.count = 0 
            self.x_list = []
            self.y_list = []
        pass

    def send(self):
        msg = str(self.x_avg) + '::' + str(self.y_avg)
        msg = msg.encode('utf8')
        print('Sending x_avg=%d & y_avg=%d' % (self.x_avg,self.y_avg))
        self.sk.send(msg)
        pass
def main():
    show_webcam()


if __name__ == '__main__':
	main()
