# python BLE 及串口功能
# date:Tue Jul 31 18:45:13 CST 2018
# Author: Yuan
# Note:
#

from bluepy import btle
import os

class Ardui_BLE_controller(object):
    '''BLE控制'''

    def __init__(self):

        self.ble_addr = ''
        self.ble_name = 'Group6'
        self.ble_strenth = ''
        self.ble_conn = ''
        self.arm_service = ''
        self.servoA = ''
        self.servoB = ''
        self.servoC = ''
        self.servoD = ''
        self.servoE = ''
        self.servoF = ''


    def find_ardui(self):
        '''找到我们的arduino设备'''
        timeout = 3
        scanner = btle.Scanner()
        devices = scanner.scan(timeout=timeout)
        print('Found %d devices in %d seconds' % (len(devices), timeout))
        for dev in devices:
            ble_addr = dev.addr
            if dev.getValueText(9) == self.ble_name:
                print('Found group\'s arduino ble')
                print('Name: ',self.ble_name)
                print('Address:',ble_addr)
                self.ble_addr = ble_addr
        if self.ble_addr:
            return True
        else:
            print('Oops, robotic arm didn\'t find, try again')
            return False
    
    def get_service(self):
        '''定位所有的service和characristic'''

        print('\n')
        self.ble_addr = '98:4f:ee:10:7a:4f'
        if not self.ble_addr:
            print('No ble address been recorded.')
            return False
        try:
            ble_conn = btle.Peripheral(self.ble_addr)
            self.ble_conn =ble_conn
            services_dic = ble_conn.getServices()
            print('This Peripheral contains following service\'s uuid.')
            for service in services_dic:
                print(service.uuid)
                if service.uuid == '47452000-0f63-5b27-9122-728099603712':
                    self.arm_service = service
            
            if not self.arm_service:
                print('No specific arm service found')
                return False

            
            

        except Exception:
            print('bluetooth connection or transmission failed with given MAC')

def main():
    controller = Ardui_BLE_controller()
    if not controller.find_ardui():
        os._exit(1)
    controller.get_service()

if __name__ == '__main__':
    main()