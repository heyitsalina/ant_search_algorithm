import ast
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.graphics import Rectangle, Color, Ellipse
from kivy.graphics.transformation import Matrix
from kivy.core.window import Window
from kivy.clock import Clock
from resources.simulation import Simulation
from resources.food import Food
from resources.colony import Colony
from kivy.graphics import Line

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
        root = FloatLayout()

        background = BoxLayout()
        sim.bounds = (0, Window.width - 5, 100, Window.height - 5) #100 is the height of buttons; it should be dynamic later
        with background.canvas:
            Color(1, 1, 1, 1)
            Rectangle(pos=(0, 100), size=(1920, 1080))

        simulation_widget = SimulationWidget()
        button_widget = ButtonWidget(simulation_widget)
        
        background.add_widget(simulation_widget)
        root.add_widget(background)
        root.add_widget(button_widget)

        Clock.schedule_interval(lambda dt: simulation_widget.update_world(dt), 0.1)

        return root


class ResizableDraggablePicture(Scatter):
    def on_touch_down(self, touch):
        if touch.is_mouse_scrolling:
            factor = None
            if touch.button == 'scrolldown':
                if self.scale < self.scale_max:
                    factor = 1.1
            elif touch.button == 'scrollup':
                if self.scale > self.scale_min:
                    factor = 1 / 1.1
            if factor is not None:
                self.apply_transform(Matrix().scale(factor, factor, factor),
                                    anchor=touch.pos)
    

class SimulationWidget(ResizableDraggablePicture, Widget):
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

    def draw_bounds(self):
        min_x, max_x, min_y, max_y = sim.bounds
        
        with self.canvas:
            Color(0, 0, 0, 1)
            Line(rectangle=(
                min_x,
                min_y,
                max_x - min_x,
                max_y - min_y
            ), width=1)
            
    def update_canvas(self):
        self.canvas.clear()
        self.draw_bounds() 
        with self.canvas:
            for colony in sim.colonies:
                Image(source="../images/colony.png", pos=colony.coordinates, size=(100, 100))

            for food in sim.food:
                Image(source="../images/apple.png", pos=food.coordinates, size=(100, 100))

            
            for colony in sim.colonies:
                Color(*colony.color)
                for ant in colony.ants:
                    Ellipse(pos=ant.coordinates,
                            size=(5, 5))

    def update_world(self, dt):
        if self.is_running:
            sim.next_epoch()
            self.update_canvas()
            
    def transform_array(self, array):
        return array[array.shape[0]-1::-1, :].T

    def toggle_simulation(self, instance):
        self.is_running = not self.is_running
        instance.text = 'Stop' if self.is_running else 'Start'

    def on_touch_down(self, touch):
            if not self.is_running and touch.is_double_tap:
                for colony in sim.colonies:
                    if colony.coordinates[0] < touch.x < colony.coordinates[0] + 100 and \
                    colony.coordinates[1] < touch.y < colony.coordinates[1] + 100:
                        self.show_colony_popup(colony)
                        return True 
                for food in sim.food:
                    if food.coordinates[0] < touch.x < food.coordinates[0] + 100 and \
                    food.coordinates[1] < touch.y < food.coordinates[1] + 100:
                        self.show_food_popup(food)

            return super(SimulationWidget, self).on_touch_down(touch)

    def show_colony_popup(self, colony):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        ants_label = Label(text="Number of ants:")
        content.add_widget(ants_label)

        ants_input = TextInput(text=str(len(colony.ants)), multiline=False)
        content.add_widget(ants_input)

        ant_settings_label = Label(text="Step size:")
        content.add_widget(ant_settings_label)

        steps_input = TextInput(text=str(colony.ants[0].step_size), multiline=False)
        content.add_widget(steps_input)

        carry_label = Label(text="Amount to carry:")
        content.add_widget(carry_label)

        carry_input = TextInput(text=str(colony.ants[0].amount_to_carry), multiline=False)
        content.add_widget(carry_input)

        color_label = Label(text="Color:")
        content.add_widget(color_label)

        color_input = TextInput(text=str(colony.color), multiline=False)
        content.add_widget(color_input)

        apply_button = Button(text='Apply Changes', on_press=lambda btn: self.apply_ant_changes(colony, ants_input.text, steps_input.text, carry_input.text, color_input.text))
        content.add_widget(apply_button)

        self.popup = Popup(title='Colony Information',
                      content=content,
                      size_hint=(None, None), size=(400, 600))
        self.popup.open()
    
    def show_food_popup(self, food):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        food_label = Label(text="Amount of food:")
        content.add_widget(food_label)

        food_input = TextInput(text=str(food.amount_of_food), multiline=False)
        content.add_widget(food_input)

        apply_button = Button(text='Apply Changes', on_press=lambda btn: self.apply_food_changes(food, food_input.text))
        content.add_widget(apply_button)

        self.popup = Popup(title='Food Information',
                      content=content,
                      size_hint=(None, None), size=(400, 300))
        self.popup.open()
    
    def apply_ant_changes(self, colony, new_ant_count, new_step_size, new_amount_to_carry, new_color):   
        new_ant_count = int(new_ant_count)
        new_amount_to_carry = int(new_amount_to_carry)
        new_step_size = int(new_step_size)
        new_color = ast.literal_eval(new_color)
        if new_ant_count >= 0:
            colony.amount = new_ant_count
            colony.ants = []
            colony.add_ants(step_size=new_step_size, amount_to_carry=new_amount_to_carry)
            colony.color = new_color
            self.popup.dismiss()

    def apply_food_changes(self, food, new_food_amount):
        new_food_amount = int(new_food_amount)
        if new_food_amount >= 0:
            food.amount_of_food = new_food_amount
            self.popup.dismiss()


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
        if not self.simulation_widget.is_running:
            self.simulation_widget.bind(on_touch_down=self.place_food)
       
    def on_colony_button_press(self, instance):
        if not self.simulation_widget.is_running:
            self.simulation_widget.bind(on_touch_down=self.place_colony)

    def place_food(self, instance, touch):
        with self.simulation_widget.canvas:
            Image(source="../images/apple.png", pos=(touch.x - 50, touch.y - 50), size=(100, 100))
        self.simulation_widget.unbind(on_touch_down=self.place_food)
        sim.add_food(Food(size=(100, 100), coordinates=(touch.x-50, touch.y-50), amount_of_food=1000))

    def place_colony(self, instance, touch):
        with self.simulation_widget.canvas:
            Image(source="../images/colony.png", pos=(touch.x - 50, touch.y - 50), size=(100, 100))
        self.simulation_widget.unbind(on_touch_down=self.place_colony)
        sim.add_colony(Colony(amount=100, size=(100, 100), coordinates=(touch.x-50, touch.y-50), color=(0, 0, 0, 1)))


if __name__ == "__main__":
    GUI().run()