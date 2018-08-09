import cv2
import os
import numpy as np

'''运动检测'''

def show_webcam(mirror=False):
    cam = cv2.VideoCapture(1)
    while not cam.isOpened():
        cam.open('/dev/bus/usb/001/008')
    mog = cv2.createBackgroundSubtractorMOG2()
    bs = cv2.createBackgroundSubtractorKNN(detectShadows=True)
    es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    while True:
        ret, image = cam.read()
        h, w, _ = image.shape #读取图像长宽
        if mirror: 
            image = cv2.flip(image, 1)

        fgmask = mog.apply(image)
        th = cv2.threshold(fgmask.copy(), 150, 255, cv2.THRESH_BINARY)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(11, 11))
        closed = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel)
        _, contours, hierarchy = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for c in contours:
            if cv2.contourArea(c) > 1600:
                M = cv2.moments(c)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                
                cv2.circle(image, (cX, cY), 7, (0, 255, 255), -1)
                str = "center(%d,%d)" %(cX,cY)
                cv2.putText(image, str, (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
                
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 0), 2)
        cv2.imshow('mog', fgmask) # 未知
        cv2.imshow('thresh', th) # 二值化后的结果
        cv2.imshow('detection', image) # 检测后的结果
        if cv2.waitKey(1) == 27: 
            break  # esc to quit
    cv2.destroyAllWindows()
    cam.release()

def plot_cv():
    pass

def main():
    show_webcam()

if __name__ == '__main__':
	main()
