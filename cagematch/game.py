"""this file implements the top level game object that pulls together the rest of the code into one game"""
from .ticker import Ticker
from .entities import EntityContainer, Player, Projectile, Enemy, EnemyController
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

        # difficulty variables
        self._starting_speed = 1
        self._max_speed = 8
        self._advance_rate = 2
        self._rows = 4
        self._columns = 6
        self._xspacing = 96
        self._yspacing = self._xspacing

        # all game entities (players, enemies, ...)
        self._entities = EntityContainer()
        # player bullets
        self._player_bullets = EntityContainer(die_on_empty=False)
        # enemy bullets
        self._enemy_bullets = EntityContainer(die_on_empty=False)
        # all enemies
        self._start_level()
        # add player to game
        self._player = Player(self._resolution, self._player_shoot)
        self._entities.add(self._player)
        # add enemy container to game
        self._entities.add(self._enemies)
        # add bullet container to game
        self._entities.add(self._player_bullets)
        self._entities.add(self._enemy_bullets)

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

    def _start_level(self):
        """sets up a level of the game"""
        self._enemies = EnemyController(
            self._resolution,
            self._starting_speed,
            self._max_speed,
            self._enemy_shoot,
            advance_speed=self._advance_rate
        )
        self._enemies.populate(self._rows, self._columns, self._xspacing, self._yspacing)
        self._enemies.set_death_callback(self._next_level)
        self._starting_speed += 0.5
        self._entities.add(self._enemies)

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
        # update all entities
        self._entities.think(self._dt)
        # see if any player bullets hit any enemies
        self._player_bullets.check_collisions(
            self._enemies,
            Game._enemy_shot_by_bullet
        )
        # see if any enemy bullets hit the player
        self._enemy_bullets.check_collision_single(
            self._player,
            Game._player_shot_by_bullet
        )

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
        speed = 7
        projectile = Projectile(bullet_origin, (0, -speed), (255, 255, 0))
        projectile.set_death_callback(death_callback)
        self._player_bullets.add(projectile)

    def _enemy_shoot(self, bullet_origin, death_callback):
        """callback passed to the Player to enable them to fire projectiles"""
        speed = 3
        projectile = Projectile(bullet_origin, (0, speed), (255, 255, 255))
        projectile.set_death_callback(death_callback)
        self._enemy_bullets.add(projectile)

    def _next_level(self, enemy_controller):
        """callback called when all enemies are dead"""
        _ = enemy_controller
        print("next level")
        self._start_level()

    @staticmethod
    def _enemy_shot_by_bullet(bullet, enemy):
        """callback for an enemy being shot by a bullet"""
        bullet.die()
        enemy.die()

    @staticmethod
    def _player_shot_by_bullet(bullet, player):
        """callback for an enemy being shot by a bullet"""
        bullet.die()
        print("player died!")
        # TODO: handle player death
