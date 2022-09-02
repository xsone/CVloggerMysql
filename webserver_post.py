import socket

arduino = socket.socket()
port = 8000
arduino.connect(('192.168.178.45', port))
z = '#123456;789678\n'
arduino.sendall(z.encode())
arduino.close()