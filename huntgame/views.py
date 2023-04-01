from typing import Optional, Dict, Callable, Any

import arcade
from arcade import Window
from arcade.color import BLACK
from arcade.gui import UIManager, UIWidget, UIAnchorLayout, UILabel, UIBoxLayout
from arcade.types import Color


ChoiceDefs = Dict[str, Callable[[UIWidget, Any], None]]


class HelperView(arcade.View):
    """
    A helper view which contains utility implementations for a game.

    UI elements should access the game state stored on ``self.window``.
    """
    def __init__(
        self,
        window: Optional[Window] = None,
        bg_color: Color = BLACK
    ):
        super().__init__(window=window)
        self._bg_color = bg_color
        self.ui: UIManager = UIManager()

    def fullscreen(self):
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_show_view(self):
        self.fullscreen()
        self.window.background_color = self._bg_color
        self.ui.enable()

    def on_hide_view(self):
        self.ui.disable()

    def on_draw(self):
        self.clear()
        self.ui.draw()


# class MenuScreen(ChoiceScreen):
#     def __init__(self):
#         super().__init__("", {
#             "New Game": lambda a:
#         })


class ChoiceScreen(HelperView):

    def __init__(
        self,
        text: str,
        choices: ChoiceDefs,
        title: str = "",
        window: Optional[Window] = None,
        bg_color: Color = BLACK,
        setup: bool = True
    ):
        super().__init__(window=window, bg_color=bg_color)
        self.center_widget: Optional[UIAnchorLayout] = None
        self.title: Optional[UILabel] = None
        self.text: Optional[UILabel] = None
        self.buttons: Optional[UIBoxLayout] = None
        self.vertical: Optional[UIBoxLayout] = None
        self.anchor_widget: Optional[UIAnchorLayout] = None

        self._title_text: str = title
        self._full_text: str = text
        self._choices: ChoiceDefs = choices
        self._initialized: bool = False

        if setup:
            self.setup()

    @property
    def text_finished(self) -> bool:
        return self.text.text == self._full_text

    def setup(
        self,
        text: Optional[str] = None,
        choices: Optional[ChoiceDefs] = None,
        title: Optional[str] = None,
    ):
        choices = choices if choices is not None else self._choices
        text = text if text is not None else self._full_text
        title = title if title is not None else self._title_text

        if self._initialized:
            self.anchor_widget.clear()

        self.text = UILabel(text=text, width=200, multiline=True)
        self.buttons = UIBoxLayout(space_between=20, vertical=False)

        for choice_text, on_click in choices.items():
            button = arcade.gui.UIFlatButton(text=choice_text, width=100)
            button.on_click = on_click
            self.buttons.add(button)

        self.vertical = UIBoxLayout(space_between=20, children=[self.text, self.buttons])
        self.anchor_widget = UIAnchorLayout(children=[self.vertical], anchor_x="center_x", anchor_y="center_y")
        self.ui.add(self.anchor_widget)

        self._initialized = True


