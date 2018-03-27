import Tkinter as tk
import PIL.Image as Image
import PIL.ImageTk as ImageTk

from zmq_relay import ZmqRelay

MATRIX_WIDTH = 32
MATRIX_HEIGHT = 32

GUI_WIDTH = 512
GUI_HEIGHT = 512
GUI_ZOOM = 12

class Gui(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self, None, None)

        frame = tk.Frame(self)
        frame.grid(row=0, column=0, sticky=tk.W)

        relay = ZmqRelay()

        # Row 1
        voldown_btn = tk.Button(frame, text="Vol-")
        playpause_btn = tk.Button(frame, text="Play/Pause", command=relay.send_playpause)
        volup_btn = tk.Button(frame, text="Vol+")

        voldown_btn.grid(row=1, column=1)
        playpause_btn.grid(row=1, column=2)
        volup_btn.grid(row=1, column=3)

        # Row 2
        setup_btn = tk.Button(frame, text="Setup")
        up_btn = tk.Button(frame, text="Up", command=relay.send_up)
        mode_btn = tk.Button(frame, text="Mode", command=relay.send_mode)

        setup_btn.grid(row=2, column=1)
        up_btn.grid(row=2, column=2)
        mode_btn.grid(row=2, column=3)

        # Row 3
        left_btn = tk.Button(frame, text="Left", command=relay.send_left)
        enter_btn = tk.Button(frame, text="Enter", command=relay.send_enter)
        right_btn = tk.Button(frame, text="Right", command=relay.send_right)

        left_btn.grid(row=3, column=1)
        enter_btn.grid(row=3, column=2)
        right_btn.grid(row=3, column=3)

        # Row 4
        zero_btn = tk.Button(frame, text="0/10+")
        down_btn = tk.Button(frame, text="Down", command=relay.send_down)
        back_btn = tk.Button(frame, text="Back")

        zero_btn.grid(row=4, column=1)
        down_btn.grid(row=4, column=2)
        back_btn.grid(row=4, column=3)

        # Bind the keys
        # self.bind("<Left>", controller.handle_left)
        # self.bind("<Right>", controller.handle_right)
        # self.bind("<Up>", controller.handle_up)
        # self.bind("<Down>", controller.handle_down)

        self.blank_image = Image.new(
            "RGB", (GUI_WIDTH, GUI_HEIGHT), color="#000000")
        self.blank_image = ImageTk.PhotoImage(self.blank_image)

        self.img_label = tk.Label(self, image=self.blank_image)
        self.img_label.image = self.blank_image

        self.img_label.grid(row=0, column=1, sticky=tk.E)

        #self.matrix = Tk_Image(label=self.img_label, zoom=16)
        self.after(0, self.start)

    def start(self):
        self.after(20, self.start)

    def write(self, im):
        """ Write an image to the display """

        w = MATRIX_WIDTH * GUI_ZOOM
        h = MATRIX_HEIGHT * GUI_ZOOM

        im = im.resize((w, h))
        im = ImageTk.PhotoImage(im)

        self._label.image = im
        self._label.configure(image=im)
