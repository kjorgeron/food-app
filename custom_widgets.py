from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.actionbar import ActionBar, ActionView
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle, Line, Ellipse, RoundedRectangle

border_color = (55 / 255, 71 / 255, 79 / 255, 1)  # Charcoal Gray
app_background = (236 / 255, 239 / 255, 241 / 255, 1)  # Light Gray
item_background = (96 / 255, 125 / 255, 139 / 255, 1)  # Steel Blue


class CustomLoginBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.custom_border = border_color
        self.custom_background = item_background
        pos = {"center_x": 0.5, "center_y": 0.5}
        size = (1, None)
        self.orientation = "vertical"
        self.size_hint = (0.5, 0.5)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.spacing = 10
        self.padding = [30, 0, 30, 0]
        anchor1 = AnchorLayout()
        anchor1.anchor_x = "center"
        anchor1.anchor_y = "top"
        anchor2 = AnchorLayout()
        anchor2.anchor_x = "center"
        anchor2.anchor_y = "center"
        anchor3 = AnchorLayout()
        anchor3.anchor_x = "center"
        anchor3.anchor_y = "bottom"
        self.username_input = TextInput(
            hint_text="Enter your username", size_hint=(size), height=40
        )
        self.username_input.pos_hint = pos
        self.password_input = TextInput(
            hint_text="Enter your password", size_hint=(size), height=40
        )
        self.password_input.pos_hint = pos
        self.button = CustomButton(
            text="Sign In",
            size_hint=(size),
            height=40,
        )
        self.username_input.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.password_input.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.button.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.button.bind(on_press=self.validate_login)
        anchor1.add_widget(self.username_input)
        anchor2.add_widget(self.password_input)
        anchor3.add_widget(self.button)
        self.add_widget(BoxLayout())
        self.add_widget(BoxLayout())
        self.add_widget(anchor1)
        self.add_widget(anchor2)
        self.add_widget(anchor3)
        self.add_widget(BoxLayout())
        self.add_widget(BoxLayout())
        # self.add_widget(BoxLayout(size_hint=(size), height=100))  # Empty space below

        r, g, b, a = self.custom_border
        rr, gg, bb, aa = self.custom_background
        with self.canvas.before:
            Color(rr, gg, bb, aa)  # Red background
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])

            Color(r, g, b, a)  # Black border
            self.border = Line(
                rounded_rectangle=(self.x, self.y, self.width, self.height, 20), width=2
            )

        # Bind resizing method
        self.bind(pos=self.on_size, size=self.on_size)

    def on_size(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.border.rounded_rectangle = (self.x, self.y, self.width, self.height, 20)

    def validate_login(self, instance):
        # Traverse the hierarchy to find the ScreenManager
        screen_manager = None
        current_parent = self.parent
        while current_parent:  # Traverse up the parent tree
            if hasattr(current_parent, "manager"):
                screen_manager = current_parent.manager
                break
            current_parent = current_parent.parent

        # Validate login logic
        if screen_manager:
            if self.username_input.text == "" and self.password_input.text == "":
                screen_manager.current = "recipes"
            else:
                screen_manager.current = "sign_on"
        else:
            print("Error: ScreenManager is not available.")


class CustomLoginForm(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print(self.parent)
        self.size_hint = (1, 1)
        self.custom_border = border_color
        layout = CustomLoginBoxLayout()
        self.add_widget(layout)


class CustomButton(Button):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)

        # Set button properties
        self.text = text
        self.background_color = item_background  # Button background
        r, g, b, a = border_color
        # Add border using canvas.before
        with self.canvas.before:
            Color(r, g, b, a)  # Red border color (RGBA)
            self.border_line = Line(
                width=2
            )  # Create the Line object with no rectangle yet

            # Bind size and position updates to redraw the border dynamically
            self.bind(size=self._update_border, pos=self._update_border)

    def _update_border(self, *args):
        # Update the border dimensions to match the button
        self.border_line.rectangle = (self.x, self.y, self.width, self.height)


class CustomActionBar(BoxLayout):
    def __init__(self, orientation, space, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, None)
        self.pos_hint = {"top": 1}
        self.orientation = orientation
        self.spacing = space
        self.padding = (10, 10)


class CustomLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        r, g, b, a = item_background
        with self.canvas.before:
            Color(r, g, b, a)
            self.rect = Rectangle()
        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos


class SignOnScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        with self.canvas.before:
            self.rect = Rectangle(source="images/login_background.png")
        self.bind(pos=self.update_rect, size=self.update_rect)
        layout = BoxLayout()
        layout.orientation = "vertical"
        login = CustomLoginForm()
        layout.add_widget(login)
        self.add_widget(layout)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos


class RecipeScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(
            Label(text="You are at the Recipe Screen", font_size=32, color=(0, 0, 0, 1))
        )
        with self.canvas.before:
            self.rect = Rectangle(source="images/recipes_background.png")
        self.bind(pos=self.update_rect, size=self.update_rect)
        actions = CustomActionBar(orientation="horizontal", space=10)
        budget_btn = CustomButton(text="Budget")
        budget_btn.bind(on_press=self.budget_page)
        recipe_btn = CustomButton(text="Recipes")
        recipe_btn.bind(on_press=self.recipe_page)
        grocery_btn = CustomButton(text="Grocery List")
        grocery_btn.bind(on_press=self.grocery_page)
        actions.add_widget(budget_btn)
        actions.add_widget(recipe_btn)
        actions.add_widget(grocery_btn)
        self.add_widget(actions)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def recipe_page(self, instance):
        self.manager.current = "recipes"

    def budget_page(self, instance):
        self.manager.current = "budget"

    def grocery_page(self, instance):
        self.manager.current = "grocery"


class BudgetScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(
            Label(text="You are at the Budget Screen", font_size=32, color=(0, 0, 0, 1))
        )
        with self.canvas.before:
            self.rect = Rectangle(source="images/budget_background1.png")
        self.bind(pos=self.update_rect, size=self.update_rect)
        actions = CustomActionBar(orientation="horizontal", space=10)
        budget_btn = CustomButton(text="Budget")
        budget_btn.bind(on_press=self.budget_page)
        recipe_btn = CustomButton(text="Recipes")
        recipe_btn.bind(on_press=self.recipe_page)
        grocery_btn = CustomButton(text="Grocery List")
        grocery_btn.bind(on_press=self.grocery_page)
        actions.add_widget(budget_btn)
        actions.add_widget(recipe_btn)
        actions.add_widget(grocery_btn)
        self.add_widget(actions)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def recipe_page(self, instance):
        self.manager.current = "recipes"

    def budget_page(self, instance):
        self.manager.current = "budget"

    def grocery_page(self, instance):
        self.manager.current = "grocery"


class GroceryScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(
            Label(
                text="You are at the Grocery Screen", font_size=32, color=(0, 0, 0, 1)
            )
        )
        with self.canvas.before:
            self.rect = Rectangle(source="images/grocery_background.jpeg")
        self.bind(pos=self.update_rect, size=self.update_rect)
        actions = CustomActionBar(orientation="horizontal", space=10)
        budget_btn = CustomButton(text="Budget")
        budget_btn.bind(on_press=self.budget_page)
        recipe_btn = CustomButton(text="Recipes")
        recipe_btn.bind(on_press=self.recipe_page)
        grocery_btn = CustomButton(text="Grocery List")
        grocery_btn.bind(on_press=self.grocery_page)
        actions.add_widget(budget_btn)
        actions.add_widget(recipe_btn)
        actions.add_widget(grocery_btn)
        self.add_widget(actions)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def recipe_page(self, instance):
        self.manager.current = "recipes"

    def budget_page(self, instance):
        self.manager.current = "budget"

    def grocery_page(self, instance):
        self.manager.current = "grocery"


class FoodApp(App):
    title = "Food App"

    def build(self):
        sm = ScreenManager()
        sign_on = SignOnScreen(name="sign_on")
        recipe_page = RecipeScreen(name="recipes")
        budget_page = BudgetScreen(name="budget")
        grocery_page = GroceryScreen(name="grocery")
        sm.add_widget(sign_on)
        sm.add_widget(recipe_page)
        sm.add_widget(budget_page)
        sm.add_widget(grocery_page)
        sm.current = "sign_on"
        return sm
