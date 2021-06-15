from socket import *
from threading import Thread, Condition

class ServeList(Thread):
    
    def __init__(self):
        Thread.__init__(self)
        self.bufsiz = 1024
        self.clisock = None
        self.parent = None
        self.addr = ('0.0.0.0', 0)
        self.exit = False
        self.funclis = {
                'HEL': self.hello,
                'CEK': self.checkConnect,
                }
    def setAddr(self, addr):
        self.addr = addr

    def setParent(self, parent):
        self.parent = parent

    def setCliSock(self, clisocket):
        self.clisock = clisocket
    
    def setBufsiz(self, bufsiz = 1024):
        self.bufsiz = bufsiz
    
    def getFuncList(self):
        return self.funclis
    
    def addFunc(self, funcname, func):
        self.funclis[funcname] = func
    
    def funcRegister(self, lis):
        for key, val in lis.items():
            self.funclis[key] = val
    
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
        self.clisock.send(msg.encode())

    def default(self):
        self.clisock.send('CodeError'.encode())

    def stop(self):
        self.exit = True
        self.clisock.shutdown(2)
        self.clisock.close()

    def run(self):
        patient = 0
        while True:
            if self.exit: return
            try:
                mark = self.clisock.recv(self.bufsiz).decode()
                if(mark == ''): 
                    if patient < 10:
                        patient += 1
                        continue
                    else: break
                else: patient = 0
            except:
                break
            else:
                try:
                    self.funclis.get(mark, self.default)()
                except Exception as e:
                    print(e)
                    break
        self.parent.removeThread(self.addr)

class ServerBase():
    def __init__(self, ip, port, funclis = ServeList, listen = 5, bufsiz = 1024):
        self.funclis = funclis
        self.ip = ip
        self.port = port
        self.listen = listen
        self.bufsiz = bufsiz
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind((self.ip, self.port))
        self.clients = {}
        self.exit = False
        self.head = '/:>'
        pass

    def command(self):
        while(True):
            if(self.exit): break
            cmd = input(self.head)
            if len(cmd) == 0: continue
            if cmd[0] != '/':
                print('Command must start with \'/\'.')
                continue
            cmdlis = cmd.split(' ')
            if(cmd == '/exit'): self.serverClose()
            if(cmd == '/showclients'): self.showClients()

    def removeThread(self, addr):
        if addr in self.clients.keys():
            self.clients.pop(addr)

    def showClients(self):
        print(list(self.clients.keys()))

    def serverClose(self):
        for addr, thread in self.clients.items():
            if thread.is_alive(): thread.stop()
        self.sock.close()
        self.exit = True


    def run(self):
        self.sock.listen(self.listen)
        Cmdthread = Thread(target = self.command)
        Cmdthread.start()
        while(1):
            if self.exit: break
            try:
                clisock, addr = self.sock.accept()
            except:
                break
            else:
                self.clients[addr] = self.funclis()
                self.clients[addr].setCliSock(clisock)
                self.clients[addr].setAddr(addr)
                self.clients[addr].setParent(self)
                self.clients[addr].setBufsiz(self.bufsiz)
                self.clients[addr].start()

