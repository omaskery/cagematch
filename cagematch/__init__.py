"""the cagematch module implements the 'Cage Match' game"""
from .game import Game


def main():
    """entry point for the cagematch game"""
    # the resolution of the game window
    resolution = 1024, 768
    fullscreen = False

    # create a game object and call it's run method to run the game
    Game(resolution, fullscreen).run()

