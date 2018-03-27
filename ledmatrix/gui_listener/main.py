"""
The GUI listener is used for development and has the tasks:

(1) To open a Tk window which can be used to view the images
    displayed on the matrix

(2) To open a http listener which waits for a 32x32 image to be
    posted and display the image on the screen

(3) To relay any commands to the server process using ZeroMQ

"""
import argparse
from gui import Gui


DEFAULT_PORT = "8080"

def main():
    
    parser = argparse.ArgumentParser(description="GUI Listener")
    parser.add_argument("-port", required=False, default=DEFAULT_PORT)
    args = parser.parse_args()

    print "Arguments %s" % args

    ui = Gui()
    ui.mainloop()

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    pass


