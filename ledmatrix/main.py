from __future__ import absolute_import

from gui.gui import Gui

def main():

    ui = Gui()
    ui.mainloop()

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    pass