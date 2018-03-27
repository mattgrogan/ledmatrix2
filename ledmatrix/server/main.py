import zmq

HOST = "*"
PORT = 5555

def main():

    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://%s:%s" % (HOST, PORT))

    print "listening for zmq messages"

    while True:
        events = socket.poll(timeout=1)

        if events:
            message = socket.recv()
            print message

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    pass