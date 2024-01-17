import ast
from resources import config
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
    on_mouse_pos()
        notice if cursor is over the buttons
    mouse_leave_css():
        change cursor back to arrow
    mouse_enter_css():
        change cursor to hand icon
    """
    title = "Ant Search Simulation"

    def build(self):
        Window.maximize()
        Window.bind(mouse_pos=self.on_mouse_pos)

        root = FloatLayout()

        background = BoxLayout()
       
        sim.bounds = (
            - 720 / 2,
            720 / 2,
            -480 / 2,
            480 / 2 
        )

        with background.canvas:
            Color(0.6, 0.38, 0.27, 1)
            Rectangle(pos=(0, 0), size=(1920, 1080))

        simulation_widget = SimulationWidget()
        button_widget = ButtonWidget(simulation_widget)
        
        background.add_widget(simulation_widget)
        root.add_widget(background)
        root.add_widget(button_widget)

        Clock.schedule_interval(lambda dt: simulation_widget.update_world(dt), 0.1)

        return root

    def on_mouse_pos(self, *args):
        pos = args[1]
        buttons = self.root.children[0].children
        for button in buttons:
            if button.collide_point(*pos):
                Clock.schedule_once(self.mouse_enter_css, 0)
            else:
                Clock.schedule_once(self.mouse_leave_css, 0)

    def mouse_leave_css(self, *args):
        Window.set_system_cursor('arrow')

    def mouse_enter_css(self, *args):           
        Window.set_system_cursor('hand')


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
    popup : Popup()
        a simple Kivy popup that shows settings about an object when it's double clicked

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
    draw_bounds():
        draw the bounds of the simulation area on the canvas
    clear_canvas():
        clear the canvas
    on_touch_down():
        notice double clicks
    show_colony_popup():
        show a popup to change the colony settings
    show_food_popup():
        show a popup to change the food settings
    apply_ant_changes():
        apply changes made in the ant popup to the ants
    apply_food_changes():
        apply changes made in the food popup to the food objects
    adjust_view():
        change the view back to the original
    """

    def __init__(self, **kwargs):
        super(SimulationWidget, self).__init__(**kwargs)
        self.is_running = False
        self.update_canvas()
        Clock.schedule_interval(lambda instance: self.adjust_view(instance), 0.1)

    def draw_bounds(self):
        """
        Draw the bounds of the simulation area on the canvas.

        This method draws a rectangular boundary on the canvas to visualize the bounds
        of the simulation area.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        min_x, max_x, min_y, max_y = sim.bounds
        
        with self.canvas:
            Color(0, 0, 0, 1)
            Line(rectangle=(
                min_x,
                min_y,
                max_x - min_x + 5, #5 is diameter of Ellipse
                max_y - min_y + 5
            ), width=1)
            pos = (min_x, min_y)
            Image(source="../images/background.jpg", pos=pos, size=(max_x-min_x+5, max_y-min_y+5), allow_stretch = True, keep_ratio=False)
            
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

    def clear_canvas(self, instance):
        sim.food = []
        sim.colonies= []
        self.update_canvas()

    def on_touch_down(self, touch):
        if not self.is_running and touch.is_double_tap:
            transformed_touch = self.to_local(*touch.pos)
            for colony in sim.colonies:
                colony_x, colony_y = colony.coordinates
                if colony_x < transformed_touch[0] < colony_x + 100 and \
                   colony_y < transformed_touch[1] < colony_y + 100:
                    self.show_colony_popup(colony)
                    return True 

            for food in sim.food:
                food_x, food_y = food.coordinates
                if food_x < transformed_touch[0] < food_x + 100 and \
                   food_y < transformed_touch[1] < food_y + 100:
                    self.show_food_popup(food)
                    return True  

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
    
    def adjust_view(self, instance):
        if self.scale == 1 and self.pos == (self.width/2, self.height/2):
            return False
        self.scale = 1
        self.pos = (self.width/2, self.height/2)


class FoodButton(Button):
    pass


class ColonyButton(Button):
    pass


class SizeButton(Button):
    pass


class StartStopButton(Button):
    pass


class ClearCanvasButton(Button):
    pass


class AdjustViewButton(Button):
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
        drop down menu to select the size of the border
    food_button : FoodButton()
        the food button
    colony_button : ColonyButton()
        the colony button
    start_stop_button: Button()
        the start/stop button
    
    Methods
    -------
    change_border_size():
        change the size of the border
    on_food_button_press():
        executed after pressing the food button
    on_colony_button_press():
        executed after pressing the colony button
    on_clear_button_press():
        clear the canvas and stop the simulation
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

        sizes = ((2560, 1440), (1920, 1080), (1080, 720), (720, 480), (480, 360))
        dropdown = DropDown()

        for size in sizes:
            btn = Button(text=str(size[0]) + 'x' + str(size[1]), size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            btn.bind(on_release=lambda btn, size=size: self.change_border_size(size))
            dropdown.add_widget(btn)

        size_button = SizeButton(text='Size', size_hint=(None, None))

        size_button.bind(on_release=dropdown.open)

        dropdown.bind(on_select=lambda instance, x: setattr(size_button, 'text', x))

        self.dropdown = dropdown

        food_colony_layout = BoxLayout(orientation='horizontal', spacing=0, padding=0)
        food_colony_layout.add_widget(self.food_button)
        food_colony_layout.add_widget(self.colony_button)
        food_colony_layout.add_widget(size_button)

        self.start_stop_button = StartStopButton(
            text='Start', on_press=self.simulation_widget.toggle_simulation, height=100, size_hint_y=None,
            size_hint_x=None
        )

        clear_canvas_button = ClearCanvasButton(
            text="Clear",
            on_press=self.on_clear_button_press,
            height=100,
            size_hint_y=None,
            size_hint_x=None
        )

        adjust_view_button = AdjustViewButton(
            text="Adjust\n view",
            on_press=lambda instance: simulation_widget.adjust_view(instance),
            height=100,
            size_hint_x=None,
            size_hint_y=None
        )

        clear_start_layout = BoxLayout(orientation='horizontal', spacing=0, padding=0)
        clear_start_layout.add_widget(adjust_view_button)
        clear_start_layout.add_widget(clear_canvas_button)
        clear_start_layout.add_widget(self.start_stop_button)

        buttons_layout = BoxLayout(orientation='horizontal', spacing=Window.width-600, padding=0, size_hint_y=None)
        buttons_layout.add_widget(food_colony_layout)
        buttons_layout.add_widget(clear_start_layout)

        self.add_widget(buttons_layout)

        self.food_button_pressed = False
        self.colony_button_pressed = False

    def change_border_size(self, new_border_size):
        sim.bounds = (
            - new_border_size[0] / 2,
            new_border_size[0] / 2,
            - new_border_size[1] / 2,
            new_border_size[1] / 2 
        )

        self.simulation_widget.clear_canvas(0)
        self.simulation_widget.draw_bounds()

    def on_food_button_press(self, instance):
        if not self.simulation_widget.is_running:
            self.simulation_widget.bind(on_touch_down=self.place_food)
       
    def on_colony_button_press(self, instance):
        if not self.simulation_widget.is_running:
            self.simulation_widget.bind(on_touch_down=self.place_colony)       
    
    def on_clear_button_press(self, instance):
        if self.simulation_widget.is_running:
            self.start_stop_button.trigger_action(0)
        self.simulation_widget.clear_canvas(instance)
        
    def place_food(self, instance, touch):
        transformed_touch = self.simulation_widget.to_local(touch.x, touch.y)
        
        if sim.bounds[0] < transformed_touch[0]-50 < sim.bounds[1]-90 and sim.bounds[2]-25 < transformed_touch[1]-50 < sim.bounds[3]-90:
            with self.simulation_widget.canvas:
                Image(source="../images/apple.png", pos=(transformed_touch[0] - 50, transformed_touch[1] - 50), size=(100, 100))
            self.simulation_widget.unbind(on_touch_down=self.place_food)
            sim.add_food(Food(size=(100, 100), coordinates=(transformed_touch[0] - 50, transformed_touch[1] - 50), amount_of_food=1000))

    def place_colony(self, instance, touch):
        transformed_touch = self.simulation_widget.to_local(touch.x, touch.y)

        if sim.bounds[0] < transformed_touch[0]-50 < sim.bounds[1]-90 and sim.bounds[2]-25 < transformed_touch[1]-50 < sim.bounds[3]-90:
            with self.simulation_widget.canvas:
                Image(source="../images/colony.png", pos=(transformed_touch[0] - 50, transformed_touch[1] - 50), size=(100, 100))
            self.simulation_widget.unbind(on_touch_down=self.place_colony)
            sim.add_colony(Colony(amount=100, size=(100, 100), coordinates=(transformed_touch[0] - 50, transformed_touch[1] - 50), color=(0, 0, 0, 1)))


if __name__ == "__main__":
    config
    GUI().run()
