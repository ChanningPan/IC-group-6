import socket

class data_proc(object):
    def __init__(self):
        self.coount = 0
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
        for x in self.x_list:
            amountx += x
        self.x_avg = amountx/self.max
        for y in self.y_list:
            amounty += y
        self.y_avg = amounty/ self.max
        print("x avg =",self.x_avg)
        print ("y avg = ",self.y_avg)
        pass

    def append(self,x,y):
        self.x_list.append(x)
        self.y_list.append(y)
        self.coount += 1
        if count >= self.max:
            self.average()
            self.send()
            self.x_list = []
            self.y_list = []
        pass

    def send(self):
        msg = str(self.x_avg) + '::' + str(self.y_avg)
        msg = msg.encode('utf8')
        print('Sending x_avg=%d & y_avg=%d' % (self.x_avg,self.y_avg))
        self.sk.send(msg)
        pass