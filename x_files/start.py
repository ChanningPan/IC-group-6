'''
系统的启动部分
创建时间:Sun Aug  5 15:36:03 BST 2018
作者:Zhang Tingyuan
注释:

'''

import os
import ble_module
import simple_arm
import threading
import time
import socket

class Arm(object):

    def __init__(self):
        '''初始化硬件 and 软件,包括:通过蓝牙连接并获取arduino / 获取摄像头信息 / 初始化其他系统'''

        # 找到摄像头
        usb_pipe = os.popen('lsusb')
        pipe_out = usb_pipe.read()
        pipe_out = pipe_out.split('\n')

        self.arm_model = simple_arm.Arm(130, 260)
        self.contr = ble_module.ble_controller()

        self.pix_x = 0
        self.pix_y = 0
        self.pix_z = 0

        self.real_x = 0
        self.real_y = 0
        self.real_z = 0

    def goto(self,x,y,z):
        rads = self.arm_model.goto(x,y,z)
        self.contr.charac_write('F',int(rads[0])) # base
        self.contr.charac_write('B',int(rads[1])) # shoulder
        self.contr.charac_write('A',int(rads[2])) # elbow
        # self.contr.charac_write('D',int(rads[3])) # wrist Y

    def connect(self):
        # 连接蓝牙
        self.contr.get_service()

    def pix_to_real(self,x,y,z):
        '''130mm <-> 264pix'''

        pass

    def recv_data(self,x,y,z = 100, is_pixel = True): 
        if is_pixel:
            x,y,z = self.pix_to_real(x,y,z)
        self.goto(x,y,z)
        pass

def main(arm):
    sk = socket.socket()
    sk.bind(('192.168.43.21',6666))
    sk.listen(5)
    print('Waitttting for mac connection ... ...')
    con,addr =  sk.accept()
    print('connection established')
    while True:
        msg = con.recv(2048)
        if msg == b'':
            con.close()
            print()
            main()
        coor = (msg.decode('utf8')).split('::')
        x = int(coor[0])
        y = int(coor[1])
        print('recv value of ',x,y)
        arm.recv_data(x,y,False)

if __name__ == '__main__':
    arm = Arm()
    # arm.connect()
    main(arm)
