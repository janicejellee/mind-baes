import socket, pickle


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 50000))
s.listen(1)
conn, addr = s.accept()
while 1:
    data_string = conn.recv(1024)
    if not data_string:
        break

    data = pickle.loads(data_string)
    print (data)
conn.close()