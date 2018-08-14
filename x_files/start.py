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
import signal
from termcolor import colored

class Arm(object):

    def __init__(self,working_craw = False):
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

        self.working_craw = working_craw

        self.all_over = False
        self.is_new_msg = False

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
        '''130mm <-> 264pix  &  (95,170,-100)'''

        arm_coor_o_x = 95
        arm_coor_o_y = 170
        arm_coor_o_z = -100
        
        arm_coor_x = x/-2 + arm_coor_o_x
        arm_coor_y = y/2 + arm_coor_o_y
        arm_coor_z = z/2 + arm_coor_o_z

        print('real position is ',arm_coor_x,arm_coor_y,arm_coor_z)
        return (arm_coor_x,arm_coor_y,arm_coor_z)
        pass

    def recv_data(self,x,y,z = 100, is_pixel = True, is_craw = False): 
        res = None
        if is_pixel:
            x,y,z = self.pix_to_real(x,y,z)
        self.goto(int(x),int(y),int(z))
        if is_craw:
            self.start_craw()
        pass

    def start_craw(self):
        # 初始状态张开
        time.sleep(1)
        if self.working_craw:
            self.contr.charac_write('G',50)
        time.sleep(1)
        pass

    def listen_socket(self,sk:socket.socket):
        '''副线程接受sk消息并解码'''
        self.sk = sk
        while True:
            try:
                msg = sk.recv(2048)
            except OSError:
                break
            if self.all_over:
                break
            msg = msg.decode('utf8')
            if not msg:
                print(colored('peer disconnect, stop','red') )
                self.thread_exit(None,None)
                return False
            self.msg = msg
            self.is_new_msg = True
            status = 'THREAD LISTEN recv msg from peer of '+msg
            print(colored(status,'blue'))

    def pop_sk_msg(self):
        '''弹出最新的sk消息,该消息已解码'''
        while True:
            if self.all_over:
                break
            if self.is_new_msg:
                self.is_new_msg = False
                return self.msg
        
        return False

    def thread_exit(self,a,b):
        print(colored('threading all over','red'))
        self.contr.dis_connect()
        self.sk.close()
        self.all_over = True


def main(arm):
    # local_addr = ('192.168.43.21',6666)
    local_addr = ('127.0.0.1',6666)
    sk = socket.socket()
    sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sk.bind(local_addr)
    sk.listen(5)
    print(colored('Waitttting for mac connection ... ...','red'))
    con,addr =  sk.accept()
    print(colored('connection established','red'))
    signal.signal(signal.SIGINT,arm.thread_exit)
    listener = threading.Thread(target=arm.listen_socket,args= (con,))
    listener.start()
    while True:
        try:
            msg = arm.pop_sk_msg()
            if not msg:
                break
            if '??' in msg:
                coor = msg.split('??')
                x = int(coor[0])
                y = int(coor[1])
                print(colored('-----------------------------','yellow'))
                print(colored('NOW processing OBJECT position of (%d,%d)'%(x,y),'yellow'))
                arm.recv_data(x,y,0,is_pixel=True,is_craw=True)
                print(colored('-------PROCESSING over-------','yellow'))
            elif '::' in msg:
                coor = msg.split('::')
                x = int(coor[0])
                y = int(coor[1])
                print(colored('-----------------------------','yellow'))
                print(colored('NOW processing OBJECT position of (%d,%d)'%(x,y),'yellow'))
                arm.recv_data(x,y,is_pixel= True)
                print(colored('-------PROCESSING over-------','yellow'))
            else:
                continue


        except ValueError:
            print(colored('math out of range, continue','red'))
            continue

if __name__ == '__main__':
    arm = Arm()
    # arm.connect()
    main(arm)
