import socket
import time
from threading import Thread

class UdpSerBase():
    def __init__(self, ip, port, bufsiz = 1024, dokitime = 600):
        self.ip = ip
        self.port = port
        self.bufsiz = bufsiz
        self.dokitime = dokitime
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        self.clients = {('0.0.0.0', 0): {'role': 'root'}}
        self.funclis = {
            'EHE': self.whatMeaning,
            'CEK': self.checkConnect,
            'DOK': self.DokiDoki,
        }
    def DokiDoki(self, addr, data):
        if data == '':
            self.sock.sendto('Just Monika..'.encode(), addr)
    def whatMeaning(self, addr, data):
        if data == '':
            self.sock.sendto('Ehe te nan da yo!'.encode(), addr)
    def checkConnect(self, addr, data):
        self.sendto(('recved: ' + data).encode(), addr)

    def checkDoki(self):
        while(True):
            tmp = self.clients
            erase = []
            for key in tmp:
                if(tmp[key]['role'] != 'root' and time.time() - tmp[key]['lastdoki'] > self.dokitime):
                    erase.append(key)
                    #print('Addr ' + str(key) + ' have not Doki for ' + str(self.dokitime) + ' seconds. System will kill it.')
            for key in erase:
                self.clients.pop(key)
            time.sleep(1)
    def run(self):
        thread = Thread(target = self.checkDoki)
        thread.start()
        while(1):
            print(self.clients)
            print('Waiting...')
            msg, addr = self.sock.recvfrom(self.bufsiz)
            if not(addr in self.clients.keys()):
                self.clients[addr] = {'role': 'client'}
            self.clients[addr]['lastdoki'] = time.time()
            msg = msg.decode()
            print(msg)
            sign, data = tuple(msg.split('/:>'))
            self.funclis.get(sign)(addr, data)
        thread.stop()

server = UdpSerBase('0.0.0.0', 21567, dokitime = 5)
server.run()

