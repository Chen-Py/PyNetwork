import time
from TcpClient import *
client = TcpCliSock('127.0.0.1', 21567)
client.signal('CEK', 'Check Connection')
print(client.recv())
time.sleep(5)
client.close()