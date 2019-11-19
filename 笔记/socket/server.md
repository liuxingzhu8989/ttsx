```
import socket

s = socket.socket()
host = socket.gethostname()
port = 12345
s.bind((host, port))
s.listen(5)
while True:
    c,add = s.accept()
    print(add)
    while True:
        print(c.recv(1024).decode())
        c.send("xixxi")
    c.close()
```

