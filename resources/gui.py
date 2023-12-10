import numpy as np
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.graphics import Rectangle, Color, Ellipse
from kivy.core.window import Window
from kivy.clock import Clock


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

        simulation_widget = SimulationWidget()
        button_widget = ButtonWidget(simulation_widget)

        root.add_widget(simulation_widget)
        root.add_widget(button_widget)

        Clock.schedule_interval(lambda dt: simulation_widget.update_world(dt), 0.1)

        return root
    

class SimulationWidget(Widget):
    """
    This class is the actual widget for the simulation.
    ...

    Attributes
    ----------
    is_running : bool
        indicates whether the simulation is running
    size : tuple
        size of the simulation canvas
    pos : tuple
        position of the canvas

    Methods
    -------
    generate():     for demonstration purposes only!
        generates random matrix
    update_world():
        generate new points if running
    update_canvas():
        show the points on the screen
    transform_array():
        transform the array to get show it right on the screen
    toggle_simulation():
        change whether the simulation is running or not
    """

    def __init__(self, **kwargs):
        super(SimulationWidget, self).__init__(**kwargs)
        self.is_running = False
        self.generate()

    def generate(self):
        self.array = np.random.choice([0, 1], size=(90, 160))
        self.array = self.transform_array(self.array)
        self.points = np.array(np.where(self.array == 1)).T
        self.update_canvas()

    def update_canvas(self):
        self.canvas.clear()
        self.size = (Window.size[0], Window.size[1] - 100)
        self.pos = (0, 100)
        with self.canvas:
            Color(1, 1, 1, 1)  # White background
            self.rect = Rectangle(pos=self.pos, size=self.size)

            Color(0, 0, 0, 1)  # Black points
            for point in self.points:
                Ellipse(pos=(point[0] / self.array.shape[0] * self.size[0], point[1] / self.array.shape[1] * self.size[1] + 100),
                        size=(5, 5))

    def update_world(self, dt):
        if self.is_running:
            self.pos = (0, 100)
            self.size = (Window.size[0], Window.size[1] - 100)
            self.array = np.random.choice([0, 1], size=(90, 160))
            self.array = self.transform_array(self.array)
            self.points = np.array(np.where(self.array == 1)).T
            self.update_canvas()

    def transform_array(self, array):
        return array[array.shape[0]-1::-1, :].T


    def toggle_simulation(self, instance):
        self.is_running = not self.is_running
        instance.text = 'Stop' if self.is_running else 'Start'


class ButtonWidget(BoxLayout):
    """
    This class is the widget for all the buttons.
    ...
    
    Attributs
    ---------
    simulation_widget : SimulationWidget()
        instance of the SimulationWidget() to connect both widgets
    dropdown : DropDown()
        drop down menu to select the size of the window
    
    Methods
    -------
    change_window_size():
        change the size of the window and update the canvas
    """
    
    def __init__(self, simulation_widget,**kwargs):
        super(ButtonWidget, self).__init__(**kwargs)
        self.simulation_widget = simulation_widget

        food_button = Button(text='Food', height=100, size_hint_y=None, size_hint_x=None)
        colonie_button = Button(text='Colony', height=100, size_hint_y=None, size_hint_x=None)

        sizes = [(480, 360), (720, 480), (1080, 720), (1920, 1080), (2560, 1440)]
        sizes.reverse()
        dropdown = DropDown()

        for size in sizes:
            btn = Button(text=str(size[0]) + 'x' + str(size[1]), size_hint_y = None, height = 40)
            btn.bind(on_release = lambda btn: dropdown.select(btn.text))
            btn.bind(on_release=lambda btn, size=size: self.change_window_size(size))
            dropdown.add_widget(btn)

        size_button= Button(text ='Size', size_hint =(None, None))
        
        size_button.bind(on_release = dropdown.open)

        dropdown.bind(on_select = lambda instance, x: setattr(size_button, 'text', x))

        self.dropdown = dropdown


        food_colonie_layout = BoxLayout(orientation='horizontal', spacing=0, padding=0)
        food_colonie_layout.add_widget(food_button)
        food_colonie_layout.add_widget(colonie_button)
        food_colonie_layout.add_widget(size_button)

        start_stop_button = Button(text='Start', on_press=self.simulation_widget.toggle_simulation, height=100, size_hint_y=None, size_hint_x=None)

        buttons_layout = BoxLayout(orientation='horizontal', spacing=500, padding=0, size_hint_y=None)
        buttons_layout.add_widget(food_colonie_layout)
        buttons_layout.add_widget(start_stop_button)

        self.add_widget(buttons_layout)

    def change_window_size(self, window_size):
        Window.size = window_size
        Clock.schedule_once(lambda dt: self.simulation_widget.update_canvas(), 0.1)



if __name__ == "__main__":
    GUI().run()