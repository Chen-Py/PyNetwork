from ServerBase import *
class FuncList(ServeList):
    
    def __init__(self):
        ServeList.__init__(self)
        self.val = None;
        self.funcRegister({'ADD': self.plus,
            'GET': self.get,
            })
        print(self.getFuncList())
        #self.addFunc('ADD', self.plus)
        #self.addFunc('GET', self.get)

    def get(self):
        self.send(str(self.val))
    
    def plus(self):
        val = int(self.recv())
        val += 1
        self.val = val
        self.send(str(val))
        

SB = ServerBase(FuncList, '0.0.0.0', 21567)
SB.run()
