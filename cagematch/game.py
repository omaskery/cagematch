"""this file implements the top level game object that pulls together the rest of the code into one game"""
from .ticker import Ticker
from .entities import EntityContainer, Player, Projectile, Enemy
import pygame


class Game(object):
    """this is the top level game object, the game is operated from here"""

    def __init__(self, resolution, fullscreen):
        """constructor that initialises the game"""
        # store parameters
        self._resolution = resolution
        self._fullscreen = fullscreen
        # flag for whether game is still running (see run())
        self._running = False

        # all game entities (players, enemies, ...)
        self._entities = EntityContainer()
        self._entities.add(Player(self._resolution, self._player_shoot))
        self._entities.add(Enemy((400, 100)))

        # configuration for the game's "tickers" (periodically recurring events)
        desired_fps = 60.0
        desired_lps = 100.0
        seconds_between_stats = 10.0
        # initialise the tickers
        self._render_ticker = Ticker.from_frequency(desired_fps)
        self._logic_ticker = Ticker.from_frequency(desired_lps)
        self._stats_ticker = Ticker.from_seconds(seconds_between_stats)

        # delta time between simulation steps
        self._dt = 1.0 / desired_fps

        # the colour the screen clears to before each frame is rendered
        self._clear_colour = 0, 0, 0
        # the position of the game camera
        self._camera_pos = 0, 0

        # initialise pygame and create the window
        pygame.init()
        flags = 0
        if self._fullscreen:
            flags = flags or pygame.FULLSCREEN
        self._screen = pygame.display.set_mode(self._resolution, flags)

    def __del__(self):
        """destructor that cleans up pygame when the game shuts down"""
        pygame.quit()

    def run(self):
        """method called to execute the game until it is exited"""
        self._running = True
        # infinitely run the game until some code sets the running flag to false
        while self._running:
            # handle any input events (keyboard, mouse, joystick, window...)
            self._handle_events()
            # while it's time to think, update the simulation (uses loop to 'catch up' if ever behind somehow)
            while self._logic_ticker.tick(self._run_simulation):
                pass
            # if it's time to render, draw a new frame, don't accumulate error on rendering
            # because we'd rather drop frames on a bad computer than have the simulation degrade
            self._render_ticker.tick(self._render_graphics, accumulate=False)
            # if it's time to print statistics, do that
            self._stats_ticker.tick(self._display_stats)

    def _handle_events(self):
        """handles all OS events"""
        # handle every event the OS wants us to look at
        for event in pygame.event.get():
            self._handle_event(event)

    def _handle_event(self, event):
        """handles a single OS event"""
        # if it's the quit event, set the running flag to false, exiting the game loop (see run() method above)
        if event.type == pygame.QUIT:
            self._running = False

    def _run_simulation(self):
        """updates the game's simulation/model"""
        self._entities.think(self._dt)

    def _render_graphics(self):
        """renders a new frame to draw to the screen"""
        self._screen.fill(self._clear_colour)
        # create a rectangle to describe the visible game window ("what the camera can see")
        bounds = pygame.Rect(self._camera_pos, self._resolution)
        self._entities.render(bounds, self._screen)
        pygame.display.flip()

    def _display_stats(self):
        """displays new game statistics to the console (and title bar)"""
        fps = self._render_ticker.ticks_per_second()
        lps = self._logic_ticker.ticks_per_second()
        stats_string = "fps={:.2f} lps={:.2f}".format(
            fps, lps
        )
        print("stats: {}".format(stats_string))
        pygame.display.set_caption("Cage Match ({})".format(stats_string))

    def _player_shoot(self, bullet_origin, death_callback):
        """callback passed to the Player to enable them to fire projectiles"""
        speed = 4
        projectile = Projectile(bullet_origin, (0, -speed))
        projectile.set_death_callback(death_callback)
        self._entities.add(projectile)

