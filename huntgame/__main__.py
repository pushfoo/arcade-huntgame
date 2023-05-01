import arcade

from huntgame.utils import DeferredCall
from huntgame.views import ChoiceScreen, StackWindow


def main():

    window = StackWindow(
        width=800, height=600, title="Game",
        base_view_spec=DeferredCall(
            ChoiceScreen,
            "Main Menu",
            choices={
                "New game": lambda event: print(event),
                "Exit": lambda event: arcade.exit()
            })
    )

    arcade.run()


if __name__ == "__main__":
    main()
