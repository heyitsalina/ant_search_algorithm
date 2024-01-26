import ast
import numpy as np
from resources import config
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.screen import MDScreen
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.button import MDFloatingActionButtonSpeedDial
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDSwitch
from kivy.animation import Animation
from kivy.graphics import Rectangle, Color, Ellipse
from kivy.graphics.transformation import Matrix
from kivy.graphics import Line
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp
from resources.simulation import Simulation
from resources.food import Food
from resources.colony import Colony
from resources.pheromone import Pheromone


sim = Simulation()

class GUI(MDApp):
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
    on_window_resize():
        adjust the view when the size of the window is changed
    """
    
    title = "Ant Search Simulation"

    def build(self):
        Window.bind(mouse_pos=self.on_mouse_pos)
        Window.bind(size=self.on_window_resize)

        root = MDScreen()

        background = BoxLayout()
       
        sim.bounds = (
            0,
            720,
            -480,
            0 
        )

        with background.canvas:
            Color(0.64, 0.43, 0.25, 1)
            Rectangle(pos=(0, 0), size=(1920, 1080))

        simulation_widget = SimulationWidget()
        button_widget = ButtonWidget(simulation_widget)
        
        background.add_widget(simulation_widget)
        root.add_widget(background)
        root.add_widget(button_widget)

        Clock.schedule_interval(lambda dt: simulation_widget.update_world(dt), 0.1)

        return root

    def on_start(self):
        self.fps_monitor_start()

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

    def on_window_resize(self, *args):
        Clock.schedule_interval(lambda instance: self.root.children[1].children[0].adjust_view(instance), 0.2)


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
                max_x - min_x + 5,
                max_y - min_y + 5
            ), width=1)
            pos = (min_x, min_y)
            Image(source="../images/background.jpg", pos=pos, size=(max_x-min_x+5, max_y-min_y+5), allow_stretch = True, keep_ratio=False)

    def update_canvas(self):
        self.canvas.clear()
        self.draw_bounds()
        self.draw_pheromone()
        self.draw_food()
        self.draw_ants()
        self.draw_food_life_bar()      

    def update_world(self, dt):
        if self.is_running:
            sim.next_epoch()
            self.update_canvas()
    
    def draw_pheromone(self):
        with self.canvas:
            for colony in sim.colonies:
                if colony.show_pheromone:
                        pheromone_shape = colony.pheromone.pheromone_array[0].shape
                        scale = (sim.bounds[1]//pheromone_shape[1], -sim.bounds[2]//pheromone_shape[0])
                        for pheromone_array in (0, 1):
                            array_values = colony.pheromone.pheromone_array[pheromone_array]
                            alpha = array_values / (np.min(array_values)*1.7+1) if pheromone_array == 0 else array_values / (np.max(array_values)*1.7+1)
                            color = (0, 0, 0.7) if pheromone_array == 0 else (0.7, 0, 0)
                            for row in range(pheromone_shape[0]):
                                for col in range(pheromone_shape[1]):
                                    Color(*color, alpha[row][col])
                                    Rectangle(pos=(col*scale[0]+2.5, -row*(scale[1]) - scale[1]+2.5), size=(scale[0], scale[1]))

    def draw_food(self):
        with self.canvas:
            for food in sim.food:
                Image(source="../images/apple.png", pos=food.coordinates, size=(100, 100))

    def draw_ants(self):
        with self.canvas:
            for colony in sim.colonies:
                Image(source="../images/colony.png", pos=colony.coordinates, size=(100, 100))
                Color(*colony.color)
                for ant in colony.ants:
                    Ellipse(pos=ant.coordinates,
                            size=(5, 5)) 
    
    def draw_food_life_bar(self):
        with self.canvas:
            for food in sim.food:
                if food.show_life_bar:
                    Color(0.5, 0.5, 0.5, 1)
                    Rectangle(pos=(food.coordinates[0]+13, food.coordinates[1]+80-2), size=(74, 14))
                    Color(0, 1, 0.2, 1)
                    Rectangle(pos=(food.coordinates[0]+15, food.coordinates[1]+80), size=(70*food.amount_of_food/100, 10))

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
            ants_label = MDTextField(hint_text="Number of ants", text=str(len(colony.ants)))
            ant_settings_label = MDTextField(hint_text="Step size", text=str(colony.ants[0].step_size))
            carry_label = MDTextField(hint_text="Amount to carry", text=str(colony.ants[0].amount_to_carry))
            color_label = MDTextField(hint_text="Color", text=str(colony.color))
            show_pheromone_label = MDBoxLayout(orientation="horizontal", size_hint=(.75, .75))
            pheromone_grid_label = MDTextField(hint_text="Pheromone grid", text=str(colony.pheromone.pheromone_array[0].shape))
            pheromone_switch = PheromoneSwitch(active=colony.show_pheromone)
            show_pheromone_label.add_widget(pheromone_grid_label)
            show_pheromone_label.add_widget(pheromone_switch)

            self.dialog = MDDialog(
                title='Colony Settings',
                type="custom",
                content_cls=MDBoxLayout(ants_label,
                                        ant_settings_label,
                                        carry_label,
                                        color_label,
                                        show_pheromone_label,
                                        orientation="vertical",
                                        spacing="12dp",
                                        size_hint_y=None,
                                        height="350dp",
                                        width="100dp"),
                buttons=[
                    MDFlatButton(
                        text="Cancel",
                        on_release=lambda *args: self.dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="Apply Changes",
                        on_release=lambda *args: self.apply_ant_changes(colony, ants_label.text, ant_settings_label.text, carry_label.text, color_label.text, pheromone_grid_label.text, pheromone_switch.active)
                    ),
                ],
            )
            self.dialog.open()
    
    def show_food_popup(self, food):
        food_label = MDBoxLayout(orientation="horizontal", size_hint=(.75, .75))
        amount_label = MDTextField(hint_text="Amount of food", text=str(food.amount_of_food))
        life_bar_switch = PheromoneSwitch(active=food.show_life_bar)
        food_label.add_widget(amount_label)
        food_label.add_widget(life_bar_switch)

        self.dialog = MDDialog(
            title='Food Settings',
            type="custom",
            content_cls=MDBoxLayout(food_label,
                                    orientation="vertical",
                                    spacing="12dp",
                                    size_hint_y=None,
                                    height="100dp"),
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    on_release=lambda *args: self.dialog.dismiss()
                ),
                MDFlatButton(
                    text="Apply Changes",
                    on_release=lambda *args: self.apply_food_changes(food, amount_label.text, life_bar_switch.active)
                ),
                ],
        )
        self.dialog.open()
    
    def apply_ant_changes(self, colony, new_ant_count, new_step_size, new_amount_to_carry, new_color, new_pheromone_grid, new_pheromone_state):
        new_ant_count = int(new_ant_count)
        new_amount_to_carry = int(new_amount_to_carry)
        new_step_size = int(new_step_size)
        new_color = ast.literal_eval(new_color)
        new_pheromone_grid = ast.literal_eval(new_pheromone_grid)
        if new_ant_count >= 0:
            colony.amount = new_ant_count
            colony.ants = []
            colony.add_ants(step_size=new_step_size, amount_to_carry=new_amount_to_carry)
            colony.color = new_color
            colony.pheromone = Pheromone(grid_shape=new_pheromone_grid)
            colony.show_pheromone = new_pheromone_state
            self.dialog.dismiss()

    def apply_food_changes(self, food, new_food_amount, new_life_bar_state):
        new_food_amount = int(new_food_amount)
        if new_food_amount >= 0:
            food.amount_of_food = new_food_amount
            food.show_life_bar = new_life_bar_state
            self.dialog.dismiss()
    
    def adjust_view(self, instance):
        if self.scale == 1 and self.pos == ((self.width - sim.bounds[1])//2, (self.height - sim.bounds[2])//2):
            return False
        self.scale = 1
        self.pos = ((self.width - sim.bounds[1])//2, (self.height - sim.bounds[2])//2)


class PheromoneSwitch(MDSwitch):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon_active = "check"

    def on_active(self, instance_switch, active_value: bool) -> None:
        if self.theme_cls.material_style == "M3" and self.widget_style != "ios":
            size = (
                (
                    (dp(16), dp(16))
                    if not self.icon_inactive
                    else (dp(24), dp(24))
                )
                if not active_value
                else (dp(24), dp(24))
            )
            icon = "blank"
            color = (0, 0, 0, 0)

            if self.icon_active and active_value:
                icon = self.icon_active
                color = (
                    self.icon_active_color
                    if self.icon_active_color
                    else self.theme_cls.text_color
                )
            elif self.icon_inactive and not active_value:
                icon = self.icon_inactive
                color = (
                    self.icon_inactive_color
                    if self.icon_inactive_color
                    else self.theme_cls.text_color
                )

            if not self.active:
                Animation(size=size, t="out_quad", d=0.2).start(self.ids.thumb)
                Animation(color=color, t="out_quad", d=0.2).start(
                    self.ids.thumb.ids.icon
                )
            
            self.set_icon(self, icon)

        self._update_thumb_pos()


class FoodButton(MDFloatingActionButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = "food-apple-outline"
        self.theme_cls.material_style = "M3"
        self.icon_size = 70
        self.md_bg_color = (1, 0.6, .11, 1)


class ColonyButton(MDFloatingActionButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = "../images/ant_icon.png"
        self.theme_cls.material_style = "M3"
        self.icon_size = 70
        self.md_bg_color = (1, 0.6, .11, 1)


class SizeButton(MDFloatingActionButtonSpeedDial):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        self.icon = "resize"
        self.root_button_anim = True
        self.hint_animation = True
 
    def on_enter(self, instance_button) -> None:
        """Called when the mouse cursor is over a button from the stack."""
        if self.state == "open":
            for widget in self.children:
                if self.hint_animation:
                    Animation.cancel_all(widget)
                    for item in self.data.items():
                        if widget.text in item:
                            Animation(
                                _canvas_width=widget.width + dp(24),
                                _padding_right=self.right_pad_value
                                if self.right_pad
                                else 0,
                                d=self.opening_time,
                                t=self.opening_transition,
                            ).start(instance_button)
                            if (
                                instance_button.icon
                                == self.data[f"{widget.text}"]
                                or instance_button.icon
                                == self.data[f"{widget.text}"][0]
                            ):
                                Animation(
                                    opacity=1,
                                    d=self.opening_time,
                                    t=self.opening_transition,
                                ).start(widget)
                            else:
                                Animation(
                                    opacity=0, d=0.1, t=self.opening_transition
                                ).start(widget)
                    Animation.cancel_all(widget)
        self.close_stack()


class StartStopButton(MDFillRoundFlatButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = 'Start'
        self.font_size = 40
        self.padding = 30


class ClearCanvasButton(MDFillRoundFlatButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = 'Clear'
        self.font_size = 40
        self.padding = 30


class AdjustViewButton(MDFillRoundFlatButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text="Adjust\n view"
        self.font_size = 30
        self.padding = 20


class ButtonWidget(BoxLayout):
    """
    This class is the widget for all the buttons.
    ...
    
    Attributs
    ---------
    simulation_widget : SimulationWidget()
        instance of the SimulationWidget() to connect both widgets
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

        self.food_button = FoodButton()
        self.colony_button = ColonyButton()

        self.food_button.bind(on_press=self.on_food_button_press)
        self.colony_button.bind(on_press=self.on_colony_button_press)

        sizes = {"size-xxl": (2560, 1440), "size-xl": (1920, 1080), "size-l": (1080, 720), "size-m": (720, 480), "size-s": (480, 360)}

        size_button = SizeButton()

        size_button.data = {f"{size[1][0]}x{size[1][1]}": [size[0],
                                                     "on_press", lambda btn, size=size: self.change_border_size(size[1]),
                                                     "on_release", lambda instance: size_button.close_stack(),
                                                     "on_mouse_over", size_button.on_enter,
                                                     "text", size[1]] for size in sizes.items()}

        food_colony_layout = BoxLayout(orientation='horizontal', spacing=10, padding=0)
        food_colony_layout.add_widget(self.food_button)
        food_colony_layout.add_widget(self.colony_button)

        self.start_stop_button = StartStopButton(on_press=self.simulation_widget.toggle_simulation)

        clear_canvas_button = ClearCanvasButton(on_press=self.on_clear_button_press)

        adjust_view_button = AdjustViewButton(on_press=lambda instance: simulation_widget.adjust_view(instance))

        buttons_layout = BoxLayout(orientation='horizontal', spacing=100, padding=0, size_hint_y=None)
        buttons_layout.add_widget(food_colony_layout)
        buttons_layout.add_widget(adjust_view_button)
        buttons_layout.add_widget(clear_canvas_button)
        buttons_layout.add_widget(self.start_stop_button)
        buttons_layout.add_widget(size_button)

        self.add_widget(buttons_layout)

        self.food_button_pressed = False
        self.colony_button_pressed = False

    def change_border_size(self, new_border_size):
        sim.bounds = (
            0,
            new_border_size[0],
            - new_border_size[1],
            0 
        )

        self.simulation_widget.clear_canvas(0)
        self.simulation_widget.draw_bounds()
        self.simulation_widget.adjust_view(0)

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
            sim.add_food(Food(size=(100, 100), coordinates=(transformed_touch[0] - 50, transformed_touch[1] - 50), amount_of_food=100))

    def place_colony(self, instance, touch):
        transformed_touch = self.simulation_widget.to_local(touch.x, touch.y)

        if sim.bounds[0] < transformed_touch[0]-50 < sim.bounds[1]-90 and sim.bounds[2]-25 < transformed_touch[1]-50 < sim.bounds[3]-90:
            with self.simulation_widget.canvas:
                Image(source="../images/colony.png", pos=(transformed_touch[0] - 50, transformed_touch[1] - 50), size=(100, 100))
            self.simulation_widget.unbind(on_touch_down=self.place_colony)
            n_row, n_col = int(sim.bounds[3]-sim.bounds[2])//40, int(sim.bounds[1]-sim.bounds[0])//40
            sim.add_colony(Colony(grid_pheromone_shape=(n_row, n_col), amount=100, size=(100, 100),
                                  coordinates=(transformed_touch[0] - 50, transformed_touch[1] - 50), color=(0, 0, 0, 1)))


if __name__ == "__main__":
    config
    GUI().run()
