import pytest
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.button import Button
from resources.gui import GUI, SimulationWidget, ButtonWidget

@pytest.fixture
def app():
    # Initialize the Kivy application
    app = GUI()
    return app

def test_app_builds_without_errors(app):
    # Test that the application builds without errors
    app.initialize_kivy()
    app.build()

def test_simulation_widget_generate():
    # Test the generate method in SimulationWidget
    widget = SimulationWidget()
    widget.generate()
    assert widget.array is not None
    assert widget.points is not None

def test_simulation_widget_toggle_simulation():
    # Test the toggle_simulation method in SimulationWidget
    widget = SimulationWidget()
    initial_state = widget.is_running
    widget.toggle_simulation(Button(text='Start'))
    assert widget.is_running != initial_state

def test_button_widget_change_window_size():
    # Test the change_window_size method in ButtonWidget
    widget = ButtonWidget(SimulationWidget())
    initial_size = Window.size
    widget.change_window_size((800, 600))

    # Schedule a function to check the assertion after a short delay
    def check(dt):
        assert Window.size != initial_size
        
    Clock.schedule_once(lambda dt:check, 0.1)

    # Run the Kivy main loop for a short duration to allow events to be processed
    Clock.tick()

def test_clock_schedule_interval():
    # Test the Clock.schedule_interval with a lambda function
    widget = SimulationWidget()
    Clock.schedule_interval(lambda dt: widget.update_world(dt), 0.1)


if __name__ == "__main__":
    pytest.main()
