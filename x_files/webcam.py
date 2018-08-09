"""
Simply display the contents of the webcam with optional mirroring using OpenCV 
via the new Pythonic cv2 interface.  Press <esc> to quit.
"""

import cv2
import os
import matplotlib

cam_key_word = 'C270'

def show_webcam(mirror=False):
    pipe = os.popen('lsusb')
    text = pipe.read()
    if cam_key_word in text:
        text = text.split('\n')
        for line in text:
            if cam_key_word in line:
                break
        text = line.split(' ')
        cam_path = '/dev/bus/usb/' + text[1] + '/' + text[3][:-1]
    cam = cv2.VideoCapture(0)
    # while not cam.isOpened():
    #     cam.open(cam_path)
    while True:
        ret, img = cam.read()
        if mirror: 
            img = cv2.flip(img, 1)
        cv2.imshow('my webcam', img)
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
