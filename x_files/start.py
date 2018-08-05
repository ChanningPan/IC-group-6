'''
系统的启动部分
创建时间:Sun Aug  5 15:36:03 BST 2018
作者:Zhang Tingyuan
注释:

'''

import os
 
def init():
    '''初始化硬件 and 软件,包括:通过蓝牙连接并获取arduino / 获取摄像头信息 / 初始化其他系统'''

    usb_pipe = os.popen('lsusb')
    pipe_out = usb_pipe.read()
    pipe_out = pipe_out.split('\n')
