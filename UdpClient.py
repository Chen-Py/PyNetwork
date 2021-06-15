import socket
import time
class UdpCliSock():
    def __init__(self, ip, port, bufsiz = 1024, timeout = 5):
        self.ip = ip
        self.port = port
        self.bufsiz = bufsiz
        self.timeout = timeout
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock.settimeout(self.timeout)
        self.state = self.connect()

    def connect(self):
        try:
            self.signal('EHE')
            reply = self.recv()
            if reply == 'Ehe te nan da yo!': return 'Connected'
        except:
            return 'Unconnected'
        return 'Unconnected'


    def signal(self, sign, data = None):
        if data == None: data = ''
        self.send(sign + '/:>' + data)

    def send(self, msg):
        self.sock.sendto(msg.encode(), (self.ip, self.port))

    def sendbyte(self, msg):
        self.sock.sendto(msg, (self.ip, self.port))

    def recv(self):
        return self.sock.recvfrom(self.bufsiz)[0].decode()

    def recvbyte(self):
        return self.sock.recvfrom(self.bufsiz)[0].decode()

    def close(self):
        self.sock.close()
client = UdpCliSock('127.0.0.1', 21567)
print(client.state)
time.sleep(1)
client.signal('DOK')
