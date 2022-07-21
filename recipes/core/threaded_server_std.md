# Create Threaded TCP/UDP Server with Standard Framework

## Solution

```python
import socket
import threading
import socketserver


class ThreadingTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = str(self.request.recv(1024), 'ascii')
        cur_thread = threading.current_thread()
        response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
        self.request.sendall(response)


def client(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        sock.sendall(bytes(message, 'ascii'))
        response = str(sock.recv(1024), 'ascii')
        print(f'Received: {response}')


if __name__ == '__main__':
    # Port 0 means to select an arbitrary unused port
    server = socketserver.ThreadingTCPServer(('localhost', 0), ThreadingTCPRequestHandler)
    with server:
        ip, port = server.server_address

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        # daemon: exit the server thread when the main thread terminates
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()
        print('Server loop running in thread:', server_thread.name)

        client(ip, port, 'Hello World 1')
        client(ip, port, 'Hello World 2')
        client(ip, port, 'Hello World 3')

        server.shutdown()
```

## References

More details to see [`socketserver`- Standard Networks Server Framework on Python Handbook](https://leven-cn.github.io/python-handbook/recipes/core/socketserver).
