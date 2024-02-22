from kivy.config import Config

"""
The configs required for the correct display of the gui are collected here.
As these settings must be made before further kivy imports, they are stored here and imported into the gui.
"""

Config.set('graphics', 'window_state', 'maximized')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')