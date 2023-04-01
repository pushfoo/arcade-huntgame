from collections import deque
from typing import Deque

import arcade
from arcade import View

from huntgame.views import ChoiceScreen


class GameWindow(arcade.Window):
    """
    Base game window...

    self.link helper?
        returns a callable...

    """
    def __init__(self, width: int = 800, height: int = 600):
        super().__init__(width, height, "Game")
        self.game_state = None
        self.view_stack: Deque[View] = deque()

        # make this take styles?
        self.default_view = ChoiceScreen(
            "Main Menu",
            {
                "New game": lambda event: print(event),
                "Exit": lambda event: arcade.exit()
            }
        )
        self.show_view(self.default_view)


def main():
    # window = arcade.Window(800, 600, title="Hunt Game")
    # start_view = ChoiceScreen("You enter the cave...")
    # window.show_view(start_view)
    window = GameWindow()
    arcade.run()


if __name__ == "__main__":
    main()
