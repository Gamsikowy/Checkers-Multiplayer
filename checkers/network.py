import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.112"
        self.port = 3333
        self.addr = (self.server, self.port)
        self.id = self.connect()
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
            print('Send exception', e)

    def receive(self, size):
        try:
            return self.client.recv(size).decode()
        except socket.error as e:
            print('Receive exception', e)