from socket import *
from threading import Thread, Condition

class ServeList(Thread):
    
    def __init__(self):
        Thread.__init__(self)
        self.bufsiz = 0
        self.clisock = None
        self.switch = {'HEL': self.hello,
                'CEK': self.checkConnect,
                }
    
    def setCliSock(self, clisocket):
        self.clisock = clisocket
    
    def setBufsiz(self, bufsiz = 1024):
        self.bufsiz = bufsiz
    
    def getFuncList(self):
        return self.switch
    
    def addFunc(self, funcname, func):
        self.switch[funcname] = func
    
    def funcRegister(self, lis):
        for key, val in lis.items():
            self.switch[key] = val
    
    def send(self, msg):
        self.clisock.send(msg.encode())
    
    def sendbyte(self, msg):
        self.clisock.send(msg)

    def recv(self):
        return self.clisock.recv(self.bufsiz).decode()
    
    def recvbyte(self):
        return self.clisock.recv(self.bufsiz)

    def hello(self):
        print('HelloWorld') 

    def checkConnect(self):
        msg = self.clisock.recv(self.bufsiz).decode()
        print('Message: ' + msg)
        self.clisock.send(('Accepted: ' + msg).encode())

    def default(self):
        print('Error')
        self.clisock.send('CodeError'.encode())

    def run(self):
        while True:
            try:
                mark = self.clisock.recv(self.bufsiz).decode()
                if(mark == ''):
                    print('Logged out')
                    break
            except:
                print('Logged out')
                break
            else:
                try:
                    self.switch.get(mark, self.default)()
                except Exception as e:
                    print(e)
                    print('Logged out')
                    break
        self.clisock.close()

class ServerBase():
    def __init__(self, ServLis, ip, port, listen = 5, bufsiz = 1024):
        self.ServLis = ServLis
        self.ip = ip
        self.port = port
        self.listen = listen
        self.bufsiz = bufsiz
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind((self.ip, self.port))
        pass

    def run(self):
        self.sock.listen(self.listen)
        while(1):
            print("Waiting...")
            clisock, addr = self.sock.accept()
            ST = self.ServLis()
            ST.setCliSock(clisock)
            ST.setBufsiz(self.bufsiz)
            ST.start()
            print('...receive from' + str(addr))
            pass
        pass
