import pytest
import time
from functools import partial
from kivy.core.window import Window
from kivy.clock import Clock
from resources.gui import GUI, SimulationWidget, ButtonWidget
import unittest



class TestGUI(unittest.TestCase):
    def pause(*args):
        time.sleep(0.000001)

    def run_test(self, app, *args):
        Clock.schedule_interval(self.pause, 0.000001)

        widget = ButtonWidget(SimulationWidget())
        initial_size = Window.size
        widget.change_window_size((Window.size[0] * 2, Window.size[1] * 2))

        # Schedule a function to check the assertion after a short delay
        def check(dt):
            assert Window.size != initial_size

        Clock.schedule_once(lambda dt: check(dt), 0.1)

        # Run the Kivy main loop for a short duration to allow events to be processed
        Clock.tick()

        app.stop()

    def test_create_gui(self):
        app = GUI()
        p = partial(self.run_test, app)
        Clock.schedule_once(p, 0.000001) 
        app.run()


if __name__ == "__main__":
    pytest.main()
