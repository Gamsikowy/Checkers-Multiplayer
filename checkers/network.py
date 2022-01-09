import socket
# python -u "c:\Users\Anna\Desktop\test\network.py"

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.server = "192.168.56.1"
        self.server = "192.168.1.112" # hp
        # self.server = "150.254.32.141"
        self.port = 3333
        self.addr = (self.server, self.port)
        self.id = self.connect()
        print(self.id)#del
        print('Network initialized')

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            raise Exception('The server is not running')

    def send(self, data):
        try:
            self.client.send(str.encode(data))
        except socket.error as e:
            print(e)

    def receive(self, size):
        try:
            return self.client.recv(size).decode()
        except socket.error as e:
            print(e)

#n = Network()
#print(n.send("hello"))