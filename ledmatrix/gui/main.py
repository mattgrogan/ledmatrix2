"""
The GUI listener is used for development and has the tasks:

(1) To open a Tk window which can be used to view the images
    displayed on the matrix

(2) Wait for a 32x32 image to be posted and display the image 
    on the screen

(3) To relay any commands to the server process using ZeroMQ

"""
from gui import Gui

def main():

    ui = Gui()
    ui.mainloop()

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    pass


