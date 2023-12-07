import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Rectangle, Color, Ellipse
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
import random
from kivy.config import Config


kivy.require('2.2.1')
Config.set('graphics', 'resizable', '0')



class GUI(App):
    """
    This class is used to create a graphical user interface (GUI) for the simulation.

     ...

    Methods
    -------
    build():
        initialize kivy window
    """

    def build(self):
        Window.size = (720, 480)
        root = BoxLayout(orientation='vertical', padding=0, spacing=0)

        simulation_widget = SimulationWidget(size=(1080, 680), pos=(0, 100))
        button_widget = ButtonWidget(simulation_widget)

        root.add_widget(simulation_widget)
        root.add_widget(button_widget)

        # Clock.schedule_interval(simulation_widget.update_points, 0.1)

        return root
    

class SimulationWidget(Widget):
    def __init__(self, **kwargs):
        super(SimulationWidget, self).__init__(**kwargs)
        self.is_running = False
        # self.pos = (0, 100)


        with self.canvas:
            Color(1, 1, 1, 1)  # White background
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def toggle_simulation(self, instance):
        self.is_running = not self.is_running
        instance.text = 'Stop' if self.is_running else 'Start'


class ButtonWidget(BoxLayout):
    def __init__(self, simulation_widget,**kwargs):
        super(ButtonWidget, self).__init__(**kwargs)
        self.simulation_widget = simulation_widget

        start_stop_button = Button(text='Start', on_press=simulation_widget.toggle_simulation, height=100, size_hint_y=None)

        food_button = Button(text='Food', height=100, size_hint_y=None)

        colonie_button = Button(text='Colonie', height=100, size_hint_y=None)

        self.add_widget(food_button)
        self.add_widget(colonie_button)
        self.add_widget(start_stop_button)


if __name__ == "__main__":
    GUI().run()