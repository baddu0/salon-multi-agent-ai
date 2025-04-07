import zmq

context = zmq.Context()
socket = context.socket(zmq.XPUB)
socket.bind("tcp://*:5555")

print("ZeroMQ broker running on port 5555")

try:
    while True:
        message = socket.recv()
        socket.send(message)
except KeyboardInterrupt:
    print("Broker stopped")
finally:
    socket.close()
    context.term()

