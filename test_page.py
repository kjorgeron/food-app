class CustomLoginBoxLayout(BoxLayout):
    def __init__(self, border, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint = (0.5, 0.2)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.spacing = 10
        self.padding = [20, 20, 20, 20]  # Add consistent padding to ensure widgets stay within borders
        
        # Username Input
        username_input = TextInput(hint_text="Enter your username", size_hint=(1, None), height=40)
        
        # Password Input
        password_input = TextInput(hint_text="Enter your password", size_hint=(1, None), height=40)
        
        # Button
        button = CustomButton(
            text="Sign In",
            size_hint=(1, None),
            height=40,
            border_color=border,
            item_background=(1, 1, 1, 1),  # Example background color
        )
        
        # Add widgets to layout
        self.add_widget(username_input)
        self.add_widget(password_input)
        self.add_widget(button)

        # Border Color
        r, g, b, a = border
        with self.canvas.before:
            Color(r, g, b, a)  # Border color
            self.border_line = Line(width=2)

        # Bind size and position updates to redraw border dynamically
        self.bind(size=self._update_border, pos=self._update_border)

    def _update_border(self, *args):
        # Update the border dimensions to match the layout
        self.border_line.rectangle = (self.x, self.y, self.width, self.height)