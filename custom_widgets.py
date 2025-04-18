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
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout


# Modern and Minimalist
border_color = (55 / 255, 71 / 255, 79 / 255, 1)  # Charcoal Gray css -> #37474F
app_background = (236 / 255, 239 / 255, 241 / 255, 1)  # Light Gray css -> #ECEFF1
item_background = (96 / 255, 125 / 255, 139 / 255, 1)  # Steel Blue css -> #607D8B


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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, None)
        self.pos_hint = {"top": 1}
        self.spacing = 10
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


class CustomRecipeBackground(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.rect = Rectangle(
                source="images/recipes_background.png", size=self.size, pos=self.pos
            )
        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):  # Corrected method signature
        self.rect.size = self.size
        self.rect.pos = self.pos


class CustomRecipeBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        rr, gg, bb, aa = item_background
        aa = 0.8
        r, g, b, a = border_color

        # Add the actual box elements on top
        with self.canvas.before:
            Color(rr, gg, bb, aa)  # Background overlay (if needed)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])

            Color(r, g, b, a)  # Border
            self.border = Line(
                rounded_rectangle=(self.x, self.y, self.width, self.height, 20), width=2
            )

        # Ensure resizing updates elements correctly
        self.bind(pos=self.update_elements, size=self.update_elements)

    def update_elements(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos
        self.border.rounded_rectangle = (self.x, self.y, self.width, self.height, 20)


class CustomBudgetBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.rect = Rectangle(source="images/budget_background.png")
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos


class CustomGroceryLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.rect = Rectangle(source="images/grocery_background.jpeg")
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos


class CustomSettingsButton(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Define a scale factor for resizing
        scale_factor = (
            0.5  # Adjust this to make everything smaller (e.g., 0.5 = half size)
        )

        # Button
        self.button = Button(
            size_hint=(None, None),
            size=(200 * scale_factor, 100 * scale_factor),  # Resize button
            pos_hint={"y": 0.03, "right": 0.95},
        )

        # Remove the grey background of the button
        self.button.background_normal = ""  # Disable background image
        self.button.background_down = ""  # Disable pressed background
        self.button.background_color = (0, 0, 0, 0)  # Fully transparent

        self.add_widget(self.button)

        # Image (aligned with button and resized proportionally)
        self.image = Image(
            source="images/settings-normal.png",
            size_hint=(None, None),
            size=(200 * scale_factor, 100 * scale_factor),  # Resize image
            pos=self.button.pos,
        )
        self.add_widget(self.image)

        # Bind the image's position to the button's position
        self.button.bind(pos=self.update_image_position)

    def update_image_position(self, instance, value):
        self.image.pos = instance.pos


class CustomSettingsLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        spacer = Widget(size_hint=(1, 1))  # Takes up the remaining space
        self.add_widget(spacer)
        settings = CustomSettingsButton()
        self.add_widget(settings)


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
        parent_layout = BoxLayout(orientation="vertical")
        # Action bar stays at the top with a fixed height
        actions = CustomActionBar(
            size_hint=(1, None), height=80
        )  # Adjust height as needed
        budget_btn = CustomButton(text="Budget")
        budget_btn.bind(on_press=self.budget_page)
        recipe_btn = CustomButton(text="Recipes")
        recipe_btn.bind(on_press=self.recipe_page)
        grocery_btn = CustomButton(text="Grocery List")
        grocery_btn.bind(on_press=self.grocery_page)
        actions.add_widget(budget_btn)
        actions.add_widget(recipe_btn)
        actions.add_widget(grocery_btn)
        parent_layout.add_widget(actions)

        # Wrapper Layout: FloatLayout to allow pos_hint for CustomRecipeBox
        wrapper_layout = FloatLayout(size_hint=(1, 1))  # Takes remaining space
        recipe_bg = CustomRecipeBackground()
        recipe_box = CustomRecipeBox(
            size_hint=(0.8, 0.6), pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        wrapper_layout.add_widget(recipe_bg)
        wrapper_layout.add_widget(recipe_box)
        parent_layout.add_widget(wrapper_layout)

        # Settings Layout
        settings_layout = CustomSettingsButton()
        wrapper_layout.add_widget(settings_layout)

        self.add_widget(parent_layout)

    def recipe_page(self, instance):
        self.manager.current = "recipes"

    def budget_page(self, instance):
        self.manager.current = "budget"

    def grocery_page(self, instance):
        self.manager.current = "grocery"


class BudgetScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        parent_layout = BoxLayout(orientation="vertical")
        actions = CustomActionBar(size_hint=(1, None), height=80)
        budget_btn = CustomButton(text="Budget")
        budget_btn.bind(on_press=self.budget_page)
        recipe_btn = CustomButton(text="Recipes")
        recipe_btn.bind(on_press=self.recipe_page)
        grocery_btn = CustomButton(text="Grocery List")
        grocery_btn.bind(on_press=self.grocery_page)
        actions.add_widget(budget_btn)
        actions.add_widget(recipe_btn)
        actions.add_widget(grocery_btn)
        parent_layout.add_widget(actions)

        wrapper_layout = FloatLayout()
        budget_box = CustomBudgetBox(size_hint=(1, 1))
        wrapper_layout.add_widget(budget_box)
        parent_layout.add_widget(wrapper_layout)

        # Settings Layout
        settings_layout = CustomSettingsLayout(size_hint=(1, 0.2))
        wrapper_layout.add_widget(settings_layout)

        self.add_widget(parent_layout)

    def recipe_page(self, instance):
        self.manager.current = "recipes"

    def budget_page(self, instance):
        self.manager.current = "budget"

    def grocery_page(self, instance):
        self.manager.current = "grocery"


class GroceryScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        parent_layout = BoxLayout(orientation="vertical")
        actions = CustomActionBar(size_hint=(1, None), height=80)
        budget_btn = CustomButton(text="Budget")
        budget_btn.bind(on_press=self.budget_page)
        recipe_btn = CustomButton(text="Recipes")
        recipe_btn.bind(on_press=self.recipe_page)
        grocery_btn = CustomButton(text="Grocery List")
        grocery_btn.bind(on_press=self.grocery_page)
        actions.add_widget(budget_btn)
        actions.add_widget(recipe_btn)
        actions.add_widget(grocery_btn)
        parent_layout.add_widget(actions)

        wrapper_layout = FloatLayout()
        grocery_layout = CustomGroceryLayout(size_hint=(1, 1))
        wrapper_layout.add_widget(grocery_layout)
        parent_layout.add_widget(wrapper_layout)

        # Settings Layout
        settings_layout = CustomSettingsLayout(size_hint=(1, 0.18))
        wrapper_layout.add_widget(settings_layout)

        self.add_widget(parent_layout)

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
