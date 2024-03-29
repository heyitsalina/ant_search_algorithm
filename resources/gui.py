import ast
import json
import webbrowser
import numpy as np
from resources import config
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.screen import MDScreen
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivymd.uix.button import MDIconButton
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.button import MDFloatingActionButtonSpeedDial
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDSwitch
from kivy.animation import Animation
from kivy.graphics import Rectangle, Color, Ellipse
from kivy.graphics.transformation import Matrix
from kivy.graphics import Line
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.metrics import dp
from resources.simulation import Simulation
from resources.food import Food
from resources.colony import Colony
from resources.obstacle import Obstacle
from resources.pheromone import Pheromone


sim = Simulation()

class GUI(MDApp):
    """
    This class is used to create a graphical user interface (GUI) for the simulation.

    Methods:
    build():
        initialize kivy window
    on_start():
        show fps monitor
    on_mouse_pos():
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
        """
        Initialize the GUI window and set up widgets and event bindings.

        Returns
        root : MDScreen
            The root widget of the application screen.
        """
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
            Rectangle(pos=(0, 0), size=(Window.size[0], Window.size[1]))
        background.sound = True
        background.study = False

        simulation_widget = SimulationWidget()
        button_widget = ButtonWidget(simulation_widget)
        
        background.add_widget(simulation_widget)
        background.add_widget(InfoButton())
        background.add_widget(SettingsButton())
        root.add_widget(background)
        root.add_widget(button_widget)

        Clock.schedule_interval(lambda dt: simulation_widget.update_world(dt), 0.1)

        return root

    def on_start(self):
        """
        Show the fps monitor when the application starts.
        """
        self.fps_monitor_start()

    def on_mouse_pos(self, *args):
        """
        Notice if the cursor is over the buttons.
        """
        pos = args[1]
        buttons = self.root.children[0].children
        for button in buttons:
            if button.collide_point(*pos):
                Clock.schedule_once(self.mouse_enter_css, 0)
            else:
                Clock.schedule_once(self.mouse_leave_css, 0)

    def mouse_leave_css(self, *args):
        """
        Change cursor back to arrow.
        """
        Window.set_system_cursor('arrow')

    def mouse_enter_css(self, *args):
        """
        Change cursor to hand icon.
        """
        Window.set_system_cursor('hand')

    def on_window_resize(self, *args):
        """
        Adjust the view when the size of the window is changed.
        """
        Clock.schedule_interval(lambda instance: self.root.children[1].children[2].adjust_view(instance), 0.2)


class SettingsButton(MDIconButton):
    """
    Class representing the settings button.

    Attributes:
        icon (str): The icon name representing the settings button.
        pos_hint (dict): The position hint of the settings button.
        theme_text_color (str): The theme text color of the settings button.
        text_color (tuple): The text color of the settings button.
        icon_size (int): The size of the icon in the settings button.
    --------

    Methods:
    on_press():
        Handle the press event of the settings button.
    apply_changes():
        Apply changes based on the selected settings.
    load_settings():
        Load settings from a JSON file.
    show_error_dialog():
        Display an error dialog.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the settings button.
        """
        super().__init__(*args, **kwargs)
        self.icon = "cog-outline"
        self.pos_hint = {"right": 1, "top": 0.98}
        self.theme_text_color = "Custom"
        self.text_color = (0, 0, 0, 1)
        self.icon_size = 60
    
    def on_press(self, *args):
        """
        Handle the press event of the settings button.
        """
        settings_content = MDBoxLayout(orientation="vertical", spacing="12dp", size_hint_y=None, height="160dp")
        sound_layout = MDBoxLayout(orientation="horizontal", size_hint=(0.7, .5))
        sound_layout.add_widget(MDLabel(text="Sound"))
        sound_switch = CustomSwitch(active=self.parent.sound, pos_hint={"center_x": 1.5, "center_y": 0.4})
        sound_layout.add_widget(sound_switch)
        study_layout = MDBoxLayout(orientation="horizontal", size_hint=(0.7, .5))
        study_label = MDLabel(text="New study")
        study_layout.add_widget(study_label)
        study_switch = CustomSwitch(active=self.parent.study, pos_hint={"center_x": 1.5, "center_y": 0.4})
        study_layout.add_widget(study_switch)
        load_layout = MDBoxLayout(orientation="horizontal", size_hint=(0.7, .5))
        load_label = MDLabel(text="Load data")
        load_layout.add_widget(load_label)
        load_switch = CustomSwitch(active=False, pos_hint={"center_x": 1.5, "center_y": 0.4})
        load_layout.add_widget(load_switch)

        settings_content.add_widget(sound_layout)
        settings_content.add_widget(study_layout)
        settings_content.add_widget(load_layout)

        self.dialog = MDDialog(
            title="Settings",
            type="custom",
            size_hint=[0.2, None],
            content_cls=settings_content,
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    on_release=lambda *args: self.dialog.dismiss()
                ),
                MDFlatButton(
                    text="Apply Changes",
                    on_release=lambda *args: self.apply_changes(sound_switch.active, study_switch.active, load_switch.active)
                ),
            ],
        )
        self.dialog.open()

    def apply_changes(self, new_sound_status, new_study_status, new_load_status):
        """
        Apply changes based on the selected settings.

        Args:
        new_sound_status : bool
            The new status of the sound setting.
        new_study_status : bool
            The new status of the study setting.
        new_load_status : bool
            The new status of the load data setting.
        """
        self.parent.sound = new_sound_status
        self.parent.study = new_study_status
        if new_load_status:
            self.load_settings()
        self.dialog.dismiss()

    def load_settings(self):
        """
        Load settings from a JSON file.
        """
        try:
            with open('statistics/statistics.json', 'r') as json_file:
                data = json.load(json_file)

            sim.bounds = data["simulation"][0]["boundaries"]

            sim.colonies = []
            for colony_data in data["colonies"]:
                colony = Colony(
                                grid_pheromone_shape=colony_data['pheromone grid'],
                                amount=colony_data["amount"],
                                coordinates=colony_data["coordinates"],
                                color=colony_data["color"],
                                size=(100, 100)
                                )
                colony.ants = []
                colony.add_ants(colony_data["amount to carry"], colony_data["step size"], colony_data["search radius"], colony_data["pheromone influence"])
                colony.pheromone.reducing_factor = colony_data["pheromone reduction"]
                sim.colonies.append(colony)

            sim.food = []
            for food_data in data["food"]:
                food = Food(
                            amount_of_food=food_data["start amount"],
                            coordinates=food_data["coordinates"],
                            size=(100, 100)
                            )
                sim.food.append(food)
            
            sim.obstacles = []
            for obstacle_data in data["obstacles"]:
                obstacle = Obstacle(coordinates=obstacle_data["coordinates"], 
                                    size=obstacle_data["size"]
                                    )
                sim.add_obstacle(obstacle)
            
            self.parent.children[2].update_canvas()
            self.parent.children[2].adjust_view()
        except Exception as e:
            self.show_error_dialog(f"Error: {str(e)}" + "\n\n" + "Could not load settings. Try to restart the program.")
    
    def show_error_dialog(self, error_message):
        """
        Display an error dialog.

        Args:
        error_message : str
            The error message to be displayed.
        """
        sound = SoundLoader.load("../sounds/error.mp3")
        if sound:
            sound.play()
        error_layout = MDBoxLayout(orientation="vertical", spacing="12dp", size_hint_y=None)
        error_layout.add_widget(MDLabel(text=error_message))

        error_dialog = MDDialog(
            title="[color=ff0000]Error[/color]",
            type="custom",
            content_cls=error_layout,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args: error_dialog.dismiss()
                ),
            ],
        )
        error_dialog.open()


class InfoButton(MDIconButton):
    """
    Class representing the information button.

    Attributes:
        icon : str
            The icon name representing the settings button.
        pos_hint : dict
            The position hint of the settings button.
        theme_text_color : str
            The theme text color of the settings button.
        text_color : tuple
            The text color of the settings button.
        icon_size : int
            The size of the icon in the settings button.
    --------

    Methods:
    on_press(*args):
        Handle the press event of the information button.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the information button.
        """
        super().__init__(*args, **kwargs)
        self.icon = "information-outline"
        self.pos_hint = {"top": 0.98}
        self.theme_text_color = "Custom"
        self.text_color = (0, 0, 0, 1)
        self.icon_size = 60
    
    def on_press(self, *args):
        """
        Handle the press event of the information button.
        """
        webbrowser.open("https://github.com/heyitsalina/ant_search_algorithm/blob/main/images/basic_features.gif")


class ResizableDraggablePicture(Scatter):
    """
    Class is responsible for being able to zoom into the canvas. 

    Methods:
    on_touch_down(touch):
        Handle the touch down event.
    """
    def on_touch_down(self, touch):
        """
        Handle the touch down event.

        Args:
        touch : MotionEvent
            The touch event.
        """
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
    ----------

    Attributes:
    is_running : bool
        indicates whether the simulation is running
    size : tuple
        size of the simulation canvas
    pos : tuple
        position of the canvas
    dialog : MDDialog()
        a dialog window that shows settings about an object when it's double clicked
    -------

    Methods:
    update_world():
        calculate the next epoch and update canvas
    update_canvas():
        update the canvas
    draw_pheromone():
        draw the pheromone grid
    draw_food():
        draw the Food objects
    draw_ants():
        draw the Colony objects and their ants
    draw_food_life_bar():
        draw a life bar of the Food object above them
    toggle_simulation():
        change whether the simulation is running or not
    draw_bounds():
        draw the bounds of the simulation area on the canvas
    clear_canvas():
        clear the canvas
    on_touch_down():
        notice double clicks
    show_colony_dialog():
        show a dialog to change the colony settings
    show_food_dialog():
        show a dialog to change the food settings
    show_obstacle_dialog():
        show a dialog to change the obstacle settings
    apply_ant_changes():
        apply changes made in the ant dialog to the ants
    apply_food_changes():
        apply changes made in the food dialog to the food objects
    show_error_dialog():
        show the error dialog
    adjust_view():
        change the view back to the original
    delete_object():
        delete the passed object
    """

    def __init__(self, **kwargs):
        """
        Initialize the SimulationWidget.
        """
        super(SimulationWidget, self).__init__(**kwargs)
        self.is_running = False
        self.update_canvas()
        Clock.schedule_interval(lambda instance: self.adjust_view(instance), 0.1)

    def draw_bounds(self):
        """
        Draw the bounds of the simulation area on the canvas.
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
            Image(source="../images/background.png", pos=(min_x, min_y), size=(max_x-min_x+5, max_y-min_y+5), allow_stretch=True, keep_ratio=False)

    def update_canvas(self):
        """
        Update the canvas.
        """
        self.canvas.clear()
        self.draw_bounds()
        self.draw_obstacles()
        self.draw_pheromone()
        self.draw_food()
        self.draw_ants()
        self.draw_food_life_bar()      

    def update_world(self, dt):
        """
        Calculate the next epoch and update canvas.

        Args:
        dt : float
            Time interval.
        """
        if self.is_running:
            sim.next_epoch()
            self.update_canvas()
    
    def draw_pheromone(self):
        """
        Draw the pheromone grid.
        """
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
        """
        Draw the food objects.
        """
        with self.canvas:
            for food in sim.food:
                if food.amount_of_food > 0:
                    Image(source="../images/apple.png", pos=food.coordinates, size=(100, 100))

    def draw_ants(self):
        """
        Draw the Colony objects and their ants.
        """
        with self.canvas:
            for colony in sim.colonies:
                Image(source="../images/colony.png", pos=colony.coordinates, size=(100, 100))
                MDLabel(text=str(colony.food_counter), pos=(colony.coordinates[0]+35, colony.coordinates[1]+40), size=(50, 20))
                for ant in colony.ants:
                    Color(*colony.color)
                    Ellipse(pos=ant.coordinates, size=(5, 5))
                    if ant.pheromone_status == 1:
                        Color(1, 0, 0, 1)
                        Ellipse(pos=(ant.coordinates[0]+1.5, ant.coordinates[1]+1.5), size=(2, 2))
    
    def draw_food_life_bar(self):
        """
        Draw a life bar of the Food object above them.
        """
        with self.canvas:
            for food in sim.food:
                if food.show_life_bar:
                    if food.amount_of_food > 0:
                        Color(0.5, 0.5, 0.5, 1)
                        Rectangle(pos=(food.coordinates[0]+13, food.coordinates[1]+80-2), size=(74, 14))
                        Color(0, 1, 0.2, 1)
                        Rectangle(pos=(food.coordinates[0]+15, food.coordinates[1]+80), size=(70*food.amount_of_food/food.start_amount, 10))

    def draw_obstacles(self):
        """
        Draw the obstacles.
        """
        with self.canvas:
            for obstacle in sim.obstacles:
                Image(source="../images/obstacle.png", pos=obstacle.coordinates, size=obstacle.size)

    def toggle_simulation(self, instance):
        """
        Change whether the simulation is running or not.

        Args:
        instance : Object
            The instance triggering the method.
        """
        self.is_running = not self.is_running
        instance.text = 'Stop' if self.is_running else 'Start'

        if self.parent.study:
            if not self.is_running:
                sim.create_statistic()
                self.parent.study = False
            
    def clear_canvas(self, *args):
        """
        Clear the canvas.
        """
        sim.food = []
        sim.colonies = []
        sim.obstacles = []
        self.update_canvas()

    def on_touch_down(self, touch):
        """
        Notice double clicks.

        Args:
        touch : MotionEvent
            The touch event.
        -------

        Returns:
        bool
            Whether the event was consumed.
        """
        if not self.is_running and touch.is_double_tap:
            transformed_touch = self.to_local(*touch.pos)
            for colony in sim.colonies:
                colony_x, colony_y = colony.coordinates
                if colony_x < transformed_touch[0] < colony_x + 100 and \
                   colony_y < transformed_touch[1] < colony_y + 100:
                    self.show_colony_dialog(colony)
                    return True

            for food in sim.food:
                food_x, food_y = food.coordinates
                if food_x < transformed_touch[0] < food_x + 100 and \
                   food_y < transformed_touch[1] < food_y + 100:
                    self.show_food_dialog(food)
                    return True
            
            for obstacle in sim.obstacles:
                obstacle_x, obstacle_y = obstacle.coordinates
                if obstacle_x  < transformed_touch[0] < obstacle_x + 50 and \
                    obstacle_y < transformed_touch[1] < obstacle_y + 50:
                    self.show_obstacle_dialog(obstacle)
                    return True
                
        return super(SimulationWidget, self).on_touch_down(touch)

    def show_colony_dialog(self, colony):
            """
            Show a dialog to change the colony settings.

            Args:
            colony : Colony
                The colony object to be edited.
            """
            ants_label = MDTextField(hint_text="Number of ants", text=str(len(colony.ants)))
            ant_settings_label = MDTextField(hint_text="Step size", text=str(colony.ants[0].step_size))
            carry_label = MDTextField(hint_text="Amount to carry", text=str(colony.ants[0].amount_to_carry))
            color_label = MDTextField(hint_text="Color", text=str(colony.color))
            show_pheromone_label = MDBoxLayout(orientation="horizontal", size_hint=(1.1, .9))
            pheromone_grid_label = MDTextField(hint_text="Pheromone grid", text=str(colony.pheromone.pheromone_array[0].shape))
            search_radius_label = MDTextField(hint_text="Search radius of the ants", text=str(colony.ants[0].search_radius))
            pheromone_influence_label = MDTextField(hint_text="Pheromone influence", text=str(colony.ants[0].pheromone_influence))
            reducing_factor_label = MDTextField(hint_text="Pheromone reduction factor", text=str(colony.pheromone.reducing_factor))
            switch_label = MDBoxLayout(orientation="horizontal", spacing="30dp")
            pheromone_switch = CustomSwitch(active=colony.show_pheromone)
            pheromone_text = MDLabel(text="Show Pheromone Grid", pos_hint={"center_x": 1.5, "center_y": .5})
            switch_label.add_widget(pheromone_switch)
            switch_label.add_widget(pheromone_text)

            show_pheromone_label.add_widget(pheromone_grid_label)
            show_pheromone_label.add_widget(switch_label)

            self.dialog = MDDialog(
                title='Colony Settings',
                type="custom",
                size_hint=[0.35, None],
                content_cls=MDBoxLayout(ants_label,
                                        ant_settings_label,
                                        carry_label,
                                        color_label,
                                        search_radius_label,
                                        pheromone_influence_label,
                                        reducing_factor_label,
                                        show_pheromone_label,
                                        orientation="vertical",
                                        size_hint_y=None,
                                        height="500dp"),
                buttons=[
                    MDFlatButton(
                        text="Cancel",
                        on_release=lambda *args: self.dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="Delete",
                        on_release=lambda *args: self.delete_object(colony),
                    ),
                    MDFlatButton(
                        text="Apply Changes",
                        on_release=lambda *args: self.apply_ant_changes(colony, ants_label.text, ant_settings_label.text, carry_label.text, color_label.text, search_radius_label.text, pheromone_influence_label.text, reducing_factor_label.text, pheromone_grid_label.text, pheromone_switch.active)
                    ),
                ],
            )
            self.dialog.open()
    
    def show_food_dialog(self, food):
        """
        Show a dialog to change the food settings.

        Args:
        food : Food
            The food object to be edited.
        """
        food_label = MDBoxLayout(orientation="vertical", spacing="12dp")

        food_amount_label = MDBoxLayout(orientation="horizontal", size_hint=(1, .9), spacing="30dp")
        amount_label = MDTextField(hint_text="Amount of food", text=str(food.amount_of_food))
        switch_label = MDBoxLayout(orientation="horizontal", spacing="30dp")
        life_bar_switch = CustomSwitch(active=food.show_life_bar)
        life_bar_text = MDLabel(text="Show Life Bar", pos_hint={"center_x": 1.5, "center_y": 0.6})
        switch_label.add_widget(life_bar_switch)
        switch_label.add_widget(life_bar_text)

        food_amount_label.add_widget(amount_label)
        food_amount_label.add_widget(switch_label)


        move_random_layout = MDBoxLayout(orientation="horizontal", size_hint=(1, .9), spacing="30dp")

        switch_move_label = MDBoxLayout(orientation="horizontal", spacing="30dp")
        move_random_label = MDTextField(hint_text="Move after number of epochs", text=str(food.move_after_number_of_epochs))

        move_random_switch = CustomSwitch(active=food.move_randomly)
        move_random_text = MDLabel(text="Move randomly", pos_hint={"center_x": 1.5, "center_y": 0.6})

        switch_move_label.add_widget(move_random_switch)
        switch_move_label.add_widget(move_random_text)

        move_random_layout.add_widget(move_random_label)
        move_random_layout.add_widget(switch_move_label)

        food_label.add_widget(food_amount_label)
        food_label.add_widget(move_random_layout)

        self.dialog = MDDialog(
            title='Food Settings',
            type="custom",
            size_hint=[0.35, None],
            content_cls=MDBoxLayout(food_label,
                                    orientation="vertical",
                                    size_hint_y=None,
                                    height="120dp"),
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    on_release=lambda *args: self.dialog.dismiss()
                ),
                MDFlatButton(
                        text="Delete",
                        on_release=lambda *args: self.delete_object(food),
                    ),
                MDFlatButton(
                    text="Apply Changes",
                    on_release=lambda *args: self.apply_food_changes(food, amount_label.text, life_bar_switch.active, move_random_label.text, move_random_switch.active)
                ),
                ],
        )
        self.dialog.open()
    
    def show_obstacle_dialog(self, obstacle):
        """
        Show a dialog to change the obstacle settings.

        Args:
        obstacle : Obstacle
            The obstacle object for which settings are being managed.
        """
        self.dialog = MDDialog(
            title='Obstacle Settings',
            type="custom",
            size_hint=[0.35, None],
            content_cls=MDBoxLayout(),
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    on_release=lambda *args: self.dialog.dismiss()
                ),
                MDFlatButton(
                        text="Delete",
                        on_release=lambda *args: self.delete_object(obstacle),
                    ),
                ],
        )
        self.dialog.open()

    def apply_ant_changes(self, colony, new_ant_count, new_step_size, new_amount_to_carry, new_color, new_search_radius, new_pheromone_influence, new_reducing_factor, new_pheromone_grid, new_pheromone_state):
        """
        Apply changes made in the dialog window to ant settings.

        Args:
        colony : Colony
            The colony object whose ant settings are being modified.
        new_ant_count : str
            The new number of ants in the colony.
        new_step_size : str
            The new step size for the ants.
        new_amount_to_carry : str
            The new amount of food each ant can carry.
        new_color : str
            The new color of the colony.
        new_search_radius : str
            The new search radius for the ants.
        new_pheromone_influence : str
            The new pheromone influence for the ants.
        new_reducing_factor : str
            The new pheromone reduction factor.
        new_pheromone_grid : str
            The new shape of the pheromone grid.
        new_pheromone_state : bool
            The new state indicating whether to show the pheromone grid.
        """
        try:
            new_ant_count = int(new_ant_count)
            new_amount_to_carry = int(new_amount_to_carry)
            new_step_size = int(new_step_size)
            new_color = ast.literal_eval(new_color)
            new_search_radius = int(new_search_radius)
            new_pheromone_influence = float(new_pheromone_influence)
            new_reducing_factor = float(new_reducing_factor)
            new_pheromone_grid = ast.literal_eval(new_pheromone_grid)
            
            if new_ant_count < 0:
                self.show_error_dialog("Number of ants has to be non-negative.")
                return
            if new_step_size < 0: 
                self.show_error_dialog("Step size has to be non-negative.")
                return
            if new_amount_to_carry < 0:
                self.show_error_dialog("Amount to carry has to be non-negative.")
                return
            if new_pheromone_influence < 0:
                self.show_error_dialog("Number of pheromone influence has to be non-negative.")
                return
            if new_reducing_factor < 0:
                self.show_error_dialog("Pheromone reduction factor has to be non-negative.")
                return

            colony.amount = new_ant_count
            colony.ants = []
            colony.add_ants(step_size=new_step_size, amount_to_carry=new_amount_to_carry, search_radius=new_search_radius, pheromone_influence=new_pheromone_influence)
            colony.color = new_color
            colony.pheromone = Pheromone(grid_shape=new_pheromone_grid, reducing_factor=new_reducing_factor)
            colony.show_pheromone = new_pheromone_state
            self.dialog.dismiss()

        except ValueError:
            self.show_error_dialog("Please enter valid integer values.")

        except Exception as e:
            self.show_error_dialog(f"Error: {str(e)}")

    def apply_food_changes(self, food, new_food_amount, new_life_bar_state, new_move_random_epoch, new_move_randomly_state):
        """
        Apply changes made in the dialog window to food settings.

        Args:
        food : Food
            The food object whose settings are being modified.
        new_food_amount : str
            The new amount of food.
        new_life_bar_state : bool
            The new state indicating whether to show the life bar for the food.
        new_move_random_epoch : str
            The new number of epochs after which the food moves randomly.
        new_move_randomly_state : bool
            The new state indicating whether the food moves randomly.
        """
        try:
            new_food_amount = int(new_food_amount)
            new_move_random_epoch = int(new_move_random_epoch)
            if new_food_amount < 0:
                self.show_error_dialog("Please enter a valid integer for food amount.\nThe amount of food must be >= 0.")
                return
            food.amount_of_food = new_food_amount
            food.start_amount = new_food_amount
            food.show_life_bar = new_life_bar_state
            food.move_after_number_of_epochs = new_move_random_epoch
            food.move_randomly = new_move_randomly_state
            self.dialog.dismiss()

        except ValueError:
                self.show_error_dialog("Please enter a valid integer for food amount.")

    def show_error_dialog(self, error_message):
        """
        Display an error dialog window with the provided error message.

        Args:
        error_message : str
            The error message to be displayed in the dialog window.
        """
        sound = SoundLoader.load("../sounds/error.mp3")
        if sound:
            sound.play()
        error_layout = MDBoxLayout(orientation="vertical", spacing="12dp", size_hint_y=None)
        error_layout.add_widget(MDLabel(text=error_message))

        error_dialog = MDDialog(
            title="[color=ff0000]Error[/color]",
            type="custom",
            content_cls=error_layout,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args: error_dialog.dismiss()
                ),
            ],
        )
        error_dialog.open()

    def adjust_view(self, *args):
        """
        Adjust the view of the simulation widget.
        """
        if self.scale == 1 and self.pos == ((self.width - sim.bounds[1])//2 + 95, (self.height - sim.bounds[2])//2):
            return False
        self.scale = 1
        self.pos = ((self.width - sim.bounds[1])//2 + 95, (self.height - sim.bounds[2])//2)

    def delete_object(self, object):
        """
        Delete the specified object from the simulation.

        Args:
        object : Food, Colony, or Obstacle
            The object to be deleted from the simulation.
        """
        if isinstance(object, Food):
            sim.food.remove(object)
        elif isinstance(object, Colony):
            sim.colonies.remove(object)
        elif isinstance(object, Obstacle):
            sim.obstacles.remove(object)
        self.dialog.dismiss()
        self.update_canvas()


class CustomSwitch(MDSwitch):
    """
    Custom switch widget that extends the functionality of MDSwitch.

    Attributes:
        icon_active (str): The icon to be displayed when the switch is active.
    --------

    Methods:
        on_active(instance_switch, active_value):
            Callback invoked when the switch is toggled.
    """
    def __init__(self, **kwargs):
        """
        Initialize the CustomSwitch widget.
        """
        super().__init__(**kwargs)
        self.icon_active = "check"

    def on_active(self, instance_switch, active_value):
        """
        Callback invoked when the switch is toggled.

        Args:
            instance_switch (CustomSwitch): The instance of the CustomSwitch widget.
            active_value (bool): The new state of the switch (True for active, False for inactive).
        """
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
            icon = "check"
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

            try:
                Animation(size=size, t="out_quad", d=0.2).start(self.ids.thumb)
                Animation(color=color, t="out_quad", d=0.2).start(
                    self.ids.thumb.ids.icon
                )
            except Exception:
                pass
            
            self.set_icon(self, icon)

        self._update_thumb_pos()


class FoodButton(MDFloatingActionButton):
    """
    Class representing the food button.

    Attributes:
        icon (str):
            The icon name representing the food button.
        theme_cls.material_style (str):
            The material style of the button.
        icon_size (int):
            The size of the icon in the food button.
        md_bg_color (tuple):
            The background color of the button.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the food button.
        """
        super().__init__(*args, **kwargs)
        self.icon = "food-apple-outline"
        self.theme_cls.material_style = "M3"
        self.icon_size = 70
        self.md_bg_color = (1, 0.6, .11, 1)


class ColonyButton(MDFloatingActionButton):
    """
    Class representing the colony button.

    Attributes:
        icon (str):
            The icon representing the colony button.
        theme_cls.material_style (str):
            The material style of the button.
        icon_size (int):
            The size of the icon in the colony button.
        md_bg_color (tuple):
            The background color of the button.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the colony button.
        """
        super().__init__(*args, **kwargs)
        self.icon = "../images/ant_icon.png"
        self.theme_cls.material_style = "M3"
        self.icon_size = 70
        self.md_bg_color = (1, 0.6, .11, 1)


class SizeButton(MDFloatingActionButtonSpeedDial):
    """
    Class representing the size button.

    Attributes:
        theme_cls.theme_style (str):
            The theme style of the button.
        theme_cls.primary_palette (str):
            The primary color palette of the button.
        icon (str):
            The icon representing the size button.
        label_text_color (str):
            The text color of the button label.
        label_bg_color (str):
            The background color of the button label.
        label_radius (int):
            The radius of the button label.
        root_button_anim (bool):
            Flag indicating whether root button animation is enabled.
    --------

    Methods:
        on_enter(instance_button):
            Called when the mouse cursor is over a button from the stack.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the size button.
        """
        super().__init__(*args, **kwargs)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        self.icon = "resize"
        self.label_text_color = "black"
        self.label_bg_color = "orange"
        self.label_radius = 12
        self.root_button_anim = True
 
    def on_enter(self, instance_button):
        """
        Called when the mouse cursor is over a button from the stack.
        """
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
    """
    Class representing the start/stop button.

    Attributes:
        text (str):
            The text displayed on the button.
        font_size (int):
            The font size of the button text.
        padding (int):
            The padding of the button.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the start/stop button.
        """
        super().__init__(*args, **kwargs)
        self.text = 'Start'
        self.font_size = 40
        self.padding = 30


class ClearCanvasButton(MDFillRoundFlatButton):
    """
    Class representing the clear canvas button.

    Attributes:
        text (str):
            The text displayed on the button.
        font_size (int):
            The font size of the button text.
        padding (int):
            The padding of the button.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the clear canvas button.
        """
        super().__init__(*args, **kwargs)
        self.text = 'Clear'
        self.font_size = 40
        self.padding = 30


class AdjustViewButton(MDFillRoundFlatButton):
    """
    Class representing the adjust view button.

    Attributes:
        text (str):
            The text displayed on the button.
        font_size (int):
            The font size of the button text.
        padding (int):
            The padding of the button.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the adjust view button.
        """
        super().__init__(*args, **kwargs)
        self.text = "Adjust\n view"
        self.font_size = 30
        self.padding = 20


class Obstacles_Button(MDFloatingActionButton):
    """
    Class representing the obstacles button.

    Attributes:
        icon (str):
            The icon displayed on the button.
        theme_cls (str):
            The material style of the button.
        icon_size (int):
            The size of the icon.
        md_bg_color (tuple):
            The background color of the button.
    """
    
    def __init__(self, *args, **kwargs):
        """
        Initialize the obstacles button.
        """
        super().__init__(*args, **kwargs)
        self.icon = "square-outline"
        self.theme_cls.material_style = "M3"
        self.icon_size = 70
        self.md_bg_color = (1, 0.6, .11, 1)


class ButtonWidget(BoxLayout):
    """
    This class is the widget for all the buttons.
    
    Attributes:
        simulation_widget (SimulationWidget):
            An instance of the SimulationWidget to connect both widgets.
        food_button (FoodButton):
            The food button.
        colony_button (ColonyButton):
            The colony button.
        start_stop_button (Button):
            The start/stop button.
        obstacles_button (Obstacles_Button):
            The obstacles button.
        food_button_pressed (bool):
            Indicates whether the food button is pressed.
        colony_button_pressed (bool):
            Indicates whether the colony button is pressed.
    --------
    
    Methods:
        __init__(simulation_widget, **kwargs):
            Initialize the ButtonWidget.
        change_border_size(new_border_size):
            Change the size of the simulation border.
        on_food_button_press(instance):
            Executed after pressing the food button.
        on_obstacles_button_press(instance):
            Executed after pressing the obstacle button.
        on_colony_button_press(instance):
            Executed after pressing the colony button.
        on_clear_button_press(instance):
            Clear the canvas and stop the simulation.
        place_food(instance, touch):
            Place the food on the canvas.
        place_colony(instance, touch):
            Place the colony on the canvas.
        place_obstacle(instance, touch):
            Place an obstacle on the canvas.
        play_button_sound(*args):
            Play sound if a button is pressed.
        play_place_sound(*args):
            Play sound when a new object is placed on the canvas.
    """
    
    def __init__(self, simulation_widget, **kwargs):
        """
        Initialize the ButtonWidget.

        Args:
            simulation_widget (SimulationWidget): An instance of the SimulationWidget.
        """
        super(ButtonWidget, self).__init__(**kwargs)
        self.simulation_widget = simulation_widget

        self.food_button = FoodButton(on_press=self.play_button_sound, on_release=self.on_food_button_press)
        self.colony_button = ColonyButton(on_press=self.play_button_sound, on_release=self.on_colony_button_press)
        self.obstacles_button = Obstacles_Button(on_press=self.play_button_sound, on_release=self.on_obstacles_button_press)

        sizes = {"size-xxl": (2560, 1440), "size-xl": (1920, 1080), "size-l": (1080, 720), "size-m": (720, 480), "size-s": (480, 360)}

        size_button = SizeButton()

        size_button.data = {f"  {size[1][0]}x{size[1][1]}   ": [size[0],
                                                     "on_press", lambda btn, size=size: self.change_border_size(size[1]),
                                                     "on_release", lambda instance: size_button.close_stack(),
                                                     "on_mouse_over", size_button.on_enter,] for size in sizes.items()}

        food_colony_layout = BoxLayout(orientation='horizontal', spacing=10, padding=0)
        food_colony_layout.add_widget(self.food_button)
        food_colony_layout.add_widget(self.colony_button)
        food_colony_layout.add_widget(self.obstacles_button)

        self.start_stop_button = StartStopButton(on_press=self.play_button_sound, on_release=self.simulation_widget.toggle_simulation)

        clear_canvas_button = ClearCanvasButton(on_release=self.on_clear_button_press)

        adjust_view_button = AdjustViewButton(on_press=self.play_button_sound, on_release=lambda instance: simulation_widget.adjust_view(instance))

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
        """
        Change the size of the simulation border.

        Args:
            new_border_size (tuple): The new size of the simulation border.
        """
        if self.simulation_widget.is_running:
            self.start_stop_button.trigger_action(0)
            
        sim.bounds = (
            0,
            new_border_size[0],
            - new_border_size[1],
            0 
        )

        self.simulation_widget.clear_canvas()
        self.simulation_widget.draw_bounds()
        self.simulation_widget.adjust_view()

    def on_food_button_press(self, instance):
        """
        Executed after pressing the food button.

        Args:
            instance: The instance of the food button.
        """
        if not self.simulation_widget.is_running:
            self.simulation_widget.bind(on_touch_down=self.place_food)
       
    def on_colony_button_press(self, instance):
        """
        Executed after pressing the colony button.

        Args:
            instance: The instance of the colony button.
        """
        if not self.simulation_widget.is_running:
            self.simulation_widget.bind(on_touch_down=self.place_colony)       
    
    def on_obstacles_button_press(self, instance):
        """
        Executed after pressing the obstacle button.

        Args:
            instance: The instance of the obstacle button.
        """
        if not self.simulation_widget.is_running:
            self.simulation_widget.bind(on_touch_down=self.place_obstacle)

    def on_clear_button_press(self, instance):
        """
        Clear the canvas and stop the simulation.

        Args:
            instance: The instance of the clear button.
        """
        if self.simulation_widget.is_running:
            self.start_stop_button.trigger_action(0)
        else:
            self.play_button_sound()
        self.simulation_widget.clear_canvas(instance)
        
    def place_food(self, instance, touch):
        """
        Place the food on the canvas.

        Args:
            instance: The instance of the button widget.
            touch: The touch event.
        """
        transformed_touch = self.simulation_widget.to_local(touch.x, touch.y)
        
        if sim.bounds[0] < transformed_touch[0]-50 < sim.bounds[1]-90 and sim.bounds[2]-25 < transformed_touch[1]-50 < sim.bounds[3]-90:
            self.play_place_sound()
            with self.simulation_widget.canvas:
                Image(source="../images/apple.png", pos=(transformed_touch[0] - 50, transformed_touch[1] - 50), size=(100, 100))
            self.simulation_widget.unbind(on_touch_down=self.place_food)
            sim.add_food(Food(size=(100, 100), coordinates=(transformed_touch[0] - 50, transformed_touch[1] - 50), amount_of_food=100))

    def place_colony(self, instance, touch):
        """
        Place the colony on the canvas.

        Args:
            instance: The instance of the button widget.
            touch: The touch event.
        """
        transformed_touch = self.simulation_widget.to_local(touch.x, touch.y)

        if sim.bounds[0] < transformed_touch[0]-50 < sim.bounds[1]-90 and sim.bounds[2]-25 < transformed_touch[1]-50 < sim.bounds[3]-90:
            self.play_place_sound()
            with self.simulation_widget.canvas:
                Image(source="../images/colony.png", pos=(transformed_touch[0] - 50, transformed_touch[1] - 50), size=(100, 100))
            self.simulation_widget.unbind(on_touch_down=self.place_colony)
            n_row, n_col = int(sim.bounds[3]-sim.bounds[2])//40, int(sim.bounds[1]-sim.bounds[0])//40
            sim.add_colony(Colony(grid_pheromone_shape=(n_row, n_col), amount=100, size=(100, 100),
                                  coordinates=(transformed_touch[0] - 50, transformed_touch[1] - 50), color=(0, 0, 0, 1)))

    def place_obstacle(self, instance, touch):
        """
        Place an obstacle on the canvas based on the touch position.

        Args:
        instance : instance
            The instance of the widget.
        touch : instance
            The touch event that triggered the placement of the obstacle.
        """
        transformed_touch = self.simulation_widget.to_local(touch.x, touch.y)

        if sim.bounds[0] < transformed_touch[0]-50 < sim.bounds[1]-90 and sim.bounds[2]-25 < transformed_touch[1]-50 < sim.bounds[3]-90:
            self.play_place_sound()
            with self.simulation_widget.canvas:
                Image(source="../images/obstacle.png", pos=(transformed_touch[0] - 25, transformed_touch[1] - 25), size=(50, 50))
            self.simulation_widget.unbind(on_touch_down=self.place_obstacle)
            sim.add_obstacle(Obstacle(coordinates=(transformed_touch[0] - 25, transformed_touch[1] - 25), size=(50, 50)))

    def play_button_sound(self, *args):
        """
        Play a sound when a button is clicked.
        """
        if self.parent.children[1].sound:
            sound = SoundLoader.load("../sounds/click.mp3")
            if sound:
                sound.play()

    def play_place_sound(self, *args):
        """
        Play a sound when an object is placed on the canvas.
        """
        if self.parent.children[1].sound:
            sound = SoundLoader.load("../sounds/place.mp3")
            if sound:
                sound.play()


if __name__ == "__main__":
    config
    GUI().run()
