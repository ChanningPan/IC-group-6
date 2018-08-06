'''
系统的启动部分
创建时间:Sun Aug  5 15:36:03 BST 2018
作者:Zhang Tingyuan
注释:

'''

import os
import ble_module
import simple_arm

class Arm(object):

    def __init__(self):
        '''初始化硬件 and 软件,包括:通过蓝牙连接并获取arduino / 获取摄像头信息 / 初始化其他系统'''

        # 找到摄像头
        usb_pipe = os.popen('lsusb')
        pipe_out = usb_pipe.read()
        pipe_out = pipe_out.split('\n')

        self.arm_model = simple_arm.Arm(130, 130, 120, Arm.minimum_change)
        self.contr = ble_module.ble_controller()
        self.contr.get_service()

    def goto(self,x,y,z):
        rads = self.arm_model.goto(x,y,z)
        self.contr.charac_write('F',rads[0]) # base
        self.contr.charac_write('B',rads[1]) # shoulder
        self.contr.charac_write('A',rads[2]) # elbow
        # self.contr.charac_write('D',rads[3]) # wrist Y

if __name__ == '__main__':
    arm = Arm()
    arm.goto(110,45,80)
    