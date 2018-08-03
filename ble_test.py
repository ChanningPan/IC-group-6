'''
python BLE 及串口功能
date:Tue Jul 31 18:45:13 CST 2018
Author: LaoYuan
Notes:
  a.servo对应的机械臂关节:
    servo A -- elbow
    servo B -- shoulder
    servo C -- wrist X
    servo D -- wrist Y
    servo E -- wrist Z
    servo F -- base
    servo G -- craw
'''

from bluepy import btle
import os
import binascii
import serial

class Ardui_BLE_controller(object):
    '''BLE控制'''

    def __init__(self):

        self.ble_addr = ''
        self.ble_name = 'Group6'
        self.service_uuid = '47452000-0f63-5b27-9122-728099603712'
        self.ble_conn = ''
        self.arm_service = ''
        self.ble_strenth = '' # 信号强度

        # servo characteristic uuid
        self.servo_uuid = {'A':'47452001-0f63-5b27-9122-728099603712',\
                    'B':'47452002-0f63-5b27-9122-728099603712', \
                    'C':'47452003-0f63-5b27-9122-728099603712', \
                    'D':'47452004-0f63-5b27-9122-728099603712', \
                    'E':'47452005-0f63-5b27-9122-728099603712', \
                    'F':'47452006-0f63-5b27-9122-728099603712', \
                    'G':'47452008-0f63-5b27-9122-728099603712', \
                    'reset':'47452007-0f63-5b27-9122-728099603712' }

        # servo characteristic object
        self.servo_charac = {'A':'','B':'','C':'','D':'','E':'','F':'','G':'','reset':''}


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
        check_val = 0
        charac_count = 0

        print('---------------service---------------')
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
                if service.uuid == self.service_uuid:
                    self.arm_service = service
            if not self.arm_service:
                print('No specific rob_arm service found')
                return False

        except Exception:
            print('When proccessing service, bluetooth connection or transmission failed with given MAC')

        print('---------------characteristic---------------')
        try:
            if not self.arm_service:
                print('Locating to service failed !')
            charac_dic = service.getCharacteristics()
            if not charac_dic:
                print('No characteristic has been found')
                return False
            for charac in charac_dic:
                for key in self.servo_uuid:
                    if charac.uuid == self.servo_uuid[key]:
                        self.servo_charac[key] = charac

        except Exception:
            print('When proccessing characteristics, bluetooth connection or transmission failed with given MAC')

        for key in self.servo_charac:
            check_val = check_val or self.servo_charac[key]
            charac_count += 1
            if not self.servo_charac[key]:
                print('servo %s did not found, which can not be used later' % (key))
            else:
                print('Found servo %s with uuid of %s' % (key, self.servo_uuid[key]))

        if not check_val :
            print('Got no characteristic with given uuid, EXIT')
            return False
        
        print('------------Summary-----------')
        print('Find service and characteristcs succeed')
        print('Found 1 srvice and %d characteristics' % charac_count)
        print('------------end of connect-----------\n')
        return True

    def charac_read(self,name):
        if not self.servo_charac[name]:
            print('Dest servo %s doesn\'t exist' % name)
            return False
        if name == 'reset':
            print('reset can not be read')
            return False
        data = self.servo_charac[name].read()
        # data = data.decode('utf8')
        return data

    def charac_write(self,name,data):
        if not self.servo_charac[name]:
            print('Dest servo %s doesn\'t exist' % name)
            return False
        try:
            if type(name) == str:
                in_buf = bytes(name,'utf8')
            else:
                in_buf = bytes(name)
            # self.servo_charac[name].write(data.encode('utf8'))
            self.servo_charac[name].write(in_buf)
        except Exception as e:
            print('Write data failed\n',e)
            return False
        return True

    def read_all(self):
        for key in self.servo_charac:
            if key == 'reset':
                continue
            data = self.charac_read(key)
            if not data:
                pass
            else:
                print('servo %s values %d' % (key, data[0]))

    def dis_connect(self):
        self.ble_conn.disconnect()
        return True


def main():
    controller = Ardui_BLE_controller()
    if not controller.find_ardui():
        os._exit(1)
    if not controller.get_service():
        os._exit(1)
    controller.read_all()
    controller.charac_write('B',180)
    controller.dis_connect()

    

if __name__ == '__main__':
    main()