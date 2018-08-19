import time
from PIL import Image

from server.components.screens.screen import Screen
from server.components.layers.text_layer import TextLayer
from server.components.layers.scrolling_layer import ScrollingLayer
from server.components.screens.gif_screen_factory import GifScreenFactory

from server.data.current_conditions import NOAA_Current_Observation

STATION = "KFRG"

class ClockScreen(Screen):

    def __init__(self, device):
        self.init()
        self.is_popup = False
        self.device = device

        icon_file = "icons/gif_icons/13533_icon_thumb.gif"
        self.icon = GifScreenFactory().from_icon(icon_file)

        # Create a connection to the NOAA website 
        self.current_obs = NOAA_Current_Observation(STATION)

        # Create the weather layer
        self._create_weather_layer()

        # Cache the current weather
        self._prev_weather = self._weather()

    def enter(self):
        self.icon.enter()
        self.conditions_layer.enter()

    def exit(self):
        pass

    def suspend(self):
        self.icon.suspend()
        self.conditions_layer.suspend()

    def resume(self):
        self.icon.resume()
        self.conditions_layer.resume()

    def step(self):
        self.icon.step()
        self.conditions_layer.step()

    def _create_weather_layer(self):
        # Add the weather layer
        self.conditions_layer = ScrollingLayer(self.device, TextLayer(self._weather()), xspeed=10)

    def _time(self):
        # Return the formatted time
        return time.strftime("%I:%M", time.localtime()).lstrip("0")

    def _weather_changed(self):
        # Did the weather change?

        if self._weather() != self._prev_weather:
            self._prev_weather = self._weather()
            return True
        else:
            return False

    def _weather(self):
        # Return the current weather conditions
        return self.current_obs["weather"]

    def render(self):

        # Create a blank background
        bg = Image.new("RGBA", self.device.size)

        ### Render the time
        txt = TextLayer(self._time())
        im = txt.render()

        # Calculate position of text
        x = self.device.size[0] - im.size[0]
        y = 0

        # Paste the text on the background
        bg.paste(im, box=(x, y), mask=im)

        ### Render the icon
        icon_im = self.icon.render()
        bg.paste(icon_im, box=(0,0), mask=icon_im)

        ### Render the temperature
        temp_str = "%iF" % int(float(self.current_obs["temp_f"]))
        temp = TextLayer(temp_str)
        temp_im = temp.render()
        x = 4
        y = im.size[1] + 2 # Offset by two rows
        bg.paste(temp_im, box=(x, y), mask=temp_im)

        ### Render the conditions
        if self._weather_changed():
            self._create_weather_layer

        cond_im = self.conditions_layer.render()
        x = 0
        y = im.size[1] * 2 + 4
        bg.paste(cond_im, box=(x, y), mask=cond_im)

        return bg

    def handle_input(self, cmd):
        pass
    
