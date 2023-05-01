from collections import deque
from typing import Optional, Dict, Callable, Deque

import pyglet
import arcade
from arcade import Window, View
from arcade.color import BLACK
from arcade.gui import UIManager, UIAnchorLayout, UILabel, UIBoxLayout
from arcade.types import Color

from huntgame.utils import CallTemplate, DeferredCall

from loguru import logger


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


class StackWindow(arcade.Window):

    def __init__(
        self,
        base_view_spec: Optional[CallTemplate] = None,
        defer_seconds: float = 0.1,
        **kwargs  # Should actually mirror the constructor here.
    ):
        """
        A window with a stack for views.

        :param view_spec: How to build the base view, if any.
        :param defer_seconds: How long to wait for the window to initialize
        :param kwargs: Any other args the Window can take
        """
        super().__init__(**kwargs)

        self._base_view: Optional[View] = None
        self._view_stack: Deque[View] = deque()
        if base_view_spec:
            self._pending_deferred_call: Optional[DeferredCall] =\
                base_view_spec if isinstance(base_view_spec, DeferredCall) else DeferredCall(*base_view_spec)

            pyglet.clock.schedule_once(self._handle_deferred_view, defer_seconds)
            logger.debug(
                'Scheduled: {}s until deferred view creation of {}', defer_seconds, self._pending_deferred_call)
        else:
            logger.debug('No view scheduled.')

    def _handle_deferred_view(self, elapsed: float = None) -> None:
        if self._pending_deferred_call:
            logger.debug(
                '{} elapsed, processing scheduled view call {} ',
                elapsed, self._pending_deferred_call)

            self.base_view = self._pending_deferred_call()
            self.show_view(self._base_view)
            self._pending_deferred_call = None
        else:
            logger.debug('{} elapsed, skipping initialization due to lack of call', elapsed)

    @property
    def base_view(self) -> Optional[HelperView]:
        return self._base_view

    @base_view.setter
    def base_view(self, view: HelperView):
        self._base_view = view


ChoiceDefs = Dict[str, Callable]


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

