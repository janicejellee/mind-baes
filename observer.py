import socket, pickle
import json


class ObsData:
	def __init__(self, x, y, direction):
		self.x = x
		self.y = y
		self.direction = direction









s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 50000))

while True:
	loc = input("Where did you see Mark? (two numbers sep. by spaces for x y between 0 and 9")
	direction = input("what direction was he walking in? (up, down, left, or right)")
	x = loc.split(" ")[0]
	y = loc.split(" ")[1]
	data_string = json.dumps(ObsData(x, y, direction).__dict__)
	s.sendall(pickle.dumps(ObsData(x, y, direction).__dict__))

s.close()