from rpi import Rpi

def main():

    ui = Rpi()
    ui.mainloop()

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    pass


