import socket
import time
from threading import Thread
import sys

class UdpSerBase():
    def __init__(self, ip, port, bufsiz = 1024, dokitime = 600):
        self.ip = ip
        self.port = port
        self.bufsiz = bufsiz
        self.dokitime = dokitime
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        self.clients = {('0.0.0.0', 0): {'role': 'root'}}
        self.exit = False
        self.head = '/:>'
        self.funclis = {
            'EHE': self.connect,
            'CEK': self.checkConnect,
            'DOK': self.DokiDoki,
        }
        self.cmdlis = {
            '/exit': self.serverClose,
            '/showclients': self.showClients,
        }

    def DokiDoki(self, addr, data):
        if data == '':
            self.sock.sendto('Just Monika..'.encode(), addr)

    def connect(self, addr, data):
        if data == '':
            self.sock.sendto('Ehe te nan da yo!'.encode(), addr)

    def checkConnect(self, addr, data):
        self.sendto(('recved: ' + data).encode(), addr)

    def checkDoki(self):
        while(True):
            if(self.exit): break
            tmp = self.clients
            erase = []
            for key in tmp:
                if(tmp[key]['role'] != 'root' and time.time() - tmp[key]['lastdoki'] > self.dokitime):
                    erase.append(key)
                    #print('Addr ' + str(key) + ' have not Doki for ' + str(self.dokitime) + ' seconds. System will kill it.')
            for key in erase:
                self.clients.pop(key)
            time.sleep(2)

    def command(self):
        while(True):
            if(self.exit): break
            cmd = input(self.head)
            if(len(cmd) == 0 or cmd[0] != '/'):
                print('Command must start with \'/\'.')
                continue
            cmdlis = cmd.split(' ')
            self.head = self.cmdlis.get(cmdlis[0])(cmdlis[1:])

    def showClients(self, data):
        print(self.clients)
        return self.head

    def serverClose(self, data):
        print('Server Closed..')
        self.exit = True
        tmpsock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        tmpsock.sendto('KILL'.encode(), ('127.0.0.1', self.port))
        tmpsock.close()
        return 'Bye/:>'

    def run(self):
        Dokithread = Thread(target = self.checkDoki)
        Dokithread.start()
        Comthread =  Thread(target = self.command)
        Comthread.start()
        while(1):
            msg, addr = self.sock.recvfrom(self.bufsiz)
            if(self.exit): break
            if not(addr in self.clients.keys()):
                self.clients[addr] = {'role': 'client'}
            self.clients[addr]['lastdoki'] = time.time()
            msg = msg.decode()
            sign, data = tuple(msg.split('/:>'))
            Thread(target = self.funclis.get(sign), args = (addr, data)).run()
        self.sock.close()

server = UdpSerBase('0.0.0.0', 21567, dokitime = 5)
server.run()

