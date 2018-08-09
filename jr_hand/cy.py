import cv2
import os
import numpy as np

'''图形检测(圆)'''

def show_webcam(mirror=False):
    cam = cv2.VideoCapture(1)
    while not cam.isOpened():
        cam.open('/dev/bus/usb/001/007')
    while True:
        ret, image = cam.read()
        h, w, _ = image.shape #读取图像长宽
        if mirror: 
            image = cv2.flip(image, 1)
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1,100, param1=150, param2=45, minRadius=100, maxRadius=250)
        try:
            circles = circles[0, :, :]
        except TypeError:
            a=1
        else:
            for i in circles[:]:
                cv2.circle(image, (i[0], i[1]), i[2], color=[0, 100, 0], thickness=2)  
        cv2.imshow("1",image)
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
