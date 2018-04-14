import os, glob

from server.components.screens.gif_screen import GifScreen
from server.components.layers.gif_screen_layer import GifScreenLayer
from server.components.layers.gif_icon_layer import GifIconLayer

class GifScreenFactory(object):

    def from_folder(self, folder):
        """ Create a gif screen from a folder """

        layers = []

        current_dir = os.getcwd()
        folder = os.path.normpath(os.path.join(current_dir, folder))
        
        files = [name for name in glob.glob(os.path.join(
            folder, "*.gif")) if os.path.isfile(
                os.path.join(folder, name))]

        if len(files) == 0:
            raise ValueError("No GIF images found in %s" % folder)

        for filename in files:
            layers.append(GifScreenLayer(filename))

        screen = GifScreen(layers)

        return screen

    def from_file(self, filename):
        """ Create a gif screen from a single file """
        raise NotImplementedError

    def from_icon(self, filename):
        current_dir = os.getcwd()
        filename = os.path.normpath(os.path.join(current_dir, filename))
        
        return GifIconLayer(filename)