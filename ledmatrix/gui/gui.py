from __future__ import absolute_import

import Tkinter as tk
import PIL.Image as Image
import PIL.ImageTk as ImageTk

from messaging.command_connection import CommandConnection
from messaging.image_connection import ImageConnection

MATRIX_WIDTH = 32
MATRIX_HEIGHT = 32

GUI_WIDTH = 512
GUI_HEIGHT = 512
GUI_ZOOM = 16

CMD_HOST = "localhost"
CMD_PORT = 5555

IMG_HOST = "localhost"
IMG_PORT = 5556

class Gui(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self, None, None)

        frame = tk.Frame(self)
        frame.grid(row=0, column=0, sticky=tk.W)

        # Set up connection to send commands
        cmd = CommandConnection()
        cmd.connect(CMD_HOST, CMD_PORT, as_receiver=False)

        self.image_conn = ImageConnection()
        self.image_conn.connect(IMG_HOST, IMG_PORT, as_receiver=True)

        # Row 1
        voldown_btn = tk.Button(frame, text="Vol-")
        playpause_btn = tk.Button(frame, text="Play/Pause", command=cmd.send_playpause)
        volup_btn = tk.Button(frame, text="Vol+")

        voldown_btn.grid(row=1, column=1)
        playpause_btn.grid(row=1, column=2)
        volup_btn.grid(row=1, column=3)

        # Row 2
        setup_btn = tk.Button(frame, text="Setup")
        up_btn = tk.Button(frame, text="Up", command=cmd.send_up)
        mode_btn = tk.Button(frame, text="Mode", command=cmd.send_mode)

        setup_btn.grid(row=2, column=1)
        up_btn.grid(row=2, column=2)
        mode_btn.grid(row=2, column=3)

        # Row 3
        left_btn = tk.Button(frame, text="Left", command=cmd.send_left)
        enter_btn = tk.Button(frame, text="Enter", command=cmd.send_enter)
        right_btn = tk.Button(frame, text="Right", command=cmd.send_right)

        left_btn.grid(row=3, column=1)
        enter_btn.grid(row=3, column=2)
        right_btn.grid(row=3, column=3)

        # Row 4
        zero_btn = tk.Button(frame, text="0/10+")
        down_btn = tk.Button(frame, text="Down", command=cmd.send_down)
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

        self.after(0, self.start)

    def start(self):
        im = self.image_conn.receive()
        if im is not None:
            self.display(im)
        self.after(20, self.start)

    def display(self, im):
        """ Write an image to the display """

        w = MATRIX_WIDTH * GUI_ZOOM
        h = MATRIX_HEIGHT * GUI_ZOOM

        im = im.resize((w, h))

        bg = Image.new("RGB", (GUI_WIDTH, GUI_HEIGHT), color="#000000")
        bg.paste(im, (0, 0))


        bg = ImageTk.PhotoImage(bg)

        self.img_label.image = bg
        self.img_label.configure(image=bg)
