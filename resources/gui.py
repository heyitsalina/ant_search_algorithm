from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
from kivy.graphics import Rectangle, Color, Ellipse
from kivy.core.window import Window
from kivy.clock import Clock
from resources.simulation import Simulation
from resources.food import Food
from resources.colony import Colony


sim = Simulation()

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
    update_world():
        calculate the next epoch and update canvas
    update_canvas():
        update the canvas
    transform_array():
        transform the array to get show it right on the screen
    toggle_simulation():
        change whether the simulation is running or not
    """

    def __init__(self, **kwargs):
        super(SimulationWidget, self).__init__(**kwargs)
        self.is_running = False
        self.update_canvas()

    def update_canvas(self):
        self.canvas.clear()
        self.size = (Window.size[0], Window.size[1] - 100)
        self.pos = (0, 100)
        with self.canvas:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

            for colony in sim.colonies:
                Image(source=r"..\images\colony.png", pos=colony.coordinates, size=(100, 100))

            for food in sim.food:
                Image(source=r"..\images\apple.png", pos=food.coordinates, size=(100, 100))

            Color(0, 0, 0, 1)  # Black points
            for colony in sim.colonies:
                for ant in colony.ants:
                    Ellipse(pos=ant.coordinates,
                            size=(15, 15))

    def update_world(self, dt):
        if self.is_running:
            sim.next_epoch()
            self.update_canvas()
            
    def transform_array(self, array):
        return array[array.shape[0]-1::-1, :].T

    def toggle_simulation(self, instance):
        self.is_running = not self.is_running
        instance.text = 'Stop' if self.is_running else 'Start'


class FoodButton(Button):
    pass


class ColonyButton(Button):
    pass


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
    food_button : FoodButton()
        the food button
    colony_button : ColonyButton()
        the colony button
    
    Methods
    -------
    change_window_size():
        change the size of the window and update the canvas
    on_food_press():
        executed after pressing the food button
    on_colony_press():
        executed after pressing the colony button
    place_food():
        place the food on the canvas
    place_colony():
        place the colony on the canvas
    """
    
    def __init__(self, simulation_widget, **kwargs):
        super(ButtonWidget, self).__init__(**kwargs)
        self.simulation_widget = simulation_widget

        self.food_button = FoodButton(text='Food', height=100, size_hint_y=None, size_hint_x=None)
        self.colony_button = ColonyButton(text='Colony', height=100, size_hint_y=None, size_hint_x=None)

        self.food_button.bind(on_press=self.on_food_button_press)
        self.colony_button.bind(on_press=self.on_colony_button_press)

        sizes = [(480, 360), (720, 480), (1080, 720), (1920, 1080), (2560, 1440)]
        sizes.reverse()
        dropdown = DropDown()

        for size in sizes:
            btn = Button(text=str(size[0]) + 'x' + str(size[1]), size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            btn.bind(on_release=lambda btn, size=size: self.change_window_size(size))
            dropdown.add_widget(btn)

        size_button = Button(text='Size', size_hint=(None, None))

        size_button.bind(on_release=dropdown.open)

        dropdown.bind(on_select=lambda instance, x: setattr(size_button, 'text', x))

        self.dropdown = dropdown

        food_colony_layout = BoxLayout(orientation='horizontal', spacing=0, padding=0)
        food_colony_layout.add_widget(self.food_button)
        food_colony_layout.add_widget(self.colony_button)
        food_colony_layout.add_widget(size_button)

        start_stop_button = Button(
            text='Start', on_press=self.simulation_widget.toggle_simulation, height=100, size_hint_y=None,
            size_hint_x=None
        )

        buttons_layout = BoxLayout(orientation='horizontal', spacing=500, padding=0, size_hint_y=None)
        buttons_layout.add_widget(food_colony_layout)
        buttons_layout.add_widget(start_stop_button)

        self.add_widget(buttons_layout)

        self.food_button_pressed = False
        self.colony_button_pressed = False

    def change_window_size(self, window_size):
        Window.size = window_size
        Clock.schedule_once(lambda dt: self.simulation_widget.update_canvas(), 0.1)

    def on_food_button_press(self, instance):
        self.simulation_widget.bind(on_touch_down=self.place_food)
       
    def on_colony_button_press(self, instance):
        self.simulation_widget.bind(on_touch_down=self.place_colony)

    def place_food(self, instance, touch):
        with self.simulation_widget.canvas:
            Image(source=r"..\images\apple.png", pos=(touch.x - 50, touch.y - 50), size=(100, 100))
        self.simulation_widget.unbind(on_touch_down=self.place_food)
        sim.add_food(Food(size=(100, 100), coordinates=(touch.x-50, touch.y-50), amount_of_food=1000))

    def place_colony(self, instance, touch):
        with self.simulation_widget.canvas:
            Image(source=r"..\images\colony.png", pos=(touch.x - 50, touch.y - 50), size=(100, 100))
        self.simulation_widget.unbind(on_touch_down=self.place_colony)
        sim.add_colony(Colony(amount=1000, size=(100, 100), coordinates=(touch.x-50, touch.y-50), color="black"))


if __name__ == "__main__":
    GUI().run()