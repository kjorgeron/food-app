from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.actionbar import ActionBar, ActionView
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.graphics import Color, Rectangle, Line
from custom_widgets import SignOnScreen, RecipeScreen, FoodApp

# Cool and Calming
border_color = (0 / 255, 77 / 255, 64 / 255, 1)  # Deep Teal
app_background = (224 / 255, 242 / 255, 241 / 255, 1)  # Soft Mint
item_background = (128 / 255, 222 / 255, 234 / 255, 0.8)  # Sky Blue








FoodApp().run()
