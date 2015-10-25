"""code pertaining to the playable entity in the game"""
from .entity import Entity
import datetime
import pygame


class Player(Entity):
    """this object represents the player entity in the game"""

    # single bullet means only one bullet exists at a time
    SINGLE_BULLET = 0
    # fire rate means you can fire bullets up to a fixed rate
    FIRE_RATE = 1

    def __init__(self, resolution, shoot_method):
        """constructor"""
        super().__init__()

        # store parameters
        self._shoot_method = shoot_method

        # figure out spawn position
        size = 64, 64
        start_x = (resolution[0] - size[0]) / 2
        start_y = resolution[1] - 2 * size[1]
        start_pos = start_x, start_y
        self._rect = pygame.Rect(start_pos, size)

        # derive where we can move
        self._player_bounds = pygame.Rect(size[0], start_y, resolution[0] - size[0] * 2, size[1])

        # setup fields for controlling shooting
        self._shooting_type = Player.SINGLE_BULLET
        # rate based shooting
        self._fire_rate = 5.0
        self._fire_period = datetime.timedelta(seconds=1.0/self._fire_rate)
        self._can_fire_after = datetime.datetime.now()
        # single bullet allowed shooting
        self._bullet_exists = False

    def render(self, bounds, dest):
        """render event"""
        pygame.draw.rect(dest, (255, 0, 0), self._rect)

    def think(self, dt):
        """simulation event"""
        max_speed = 3
        # see if we need to move around
        dx = Player._horizontal_movement(max_speed)
        self._rect.move_ip(dx, 0)
        # ensure we don't wander off the screen
        self._rect.clamp_ip(self._player_bounds)
        # see if we should fire bullets
        if self._can_shoot() and Player._should_shoot():
            bullet_origin = self._rect.midtop
            # record the fact the bullet exists
            self._bullet_exists = True
            # request that a bullet is shot, and that we're told when it dies
            self._shoot_method(bullet_origin, self._bullet_died)
            # set when we can next shoot
            self._can_fire_after = datetime.datetime.now() + self._fire_period

    def _bullet_died(self, bullet):
        """callback is fired when a fired bullet is deleted from game"""
        _ = bullet
        # record the fact we have no bullets 'in the air' (if we're in SINGLE_BULLET mode)
        self._bullet_exists = False

    def _can_shoot(self):
        """determines whether we can actually fire yet"""
        if self._shooting_type == Player.FIRE_RATE:
            # if we're firing up to a rate, see if enough time has passed since last shot
            now = datetime.datetime.now()
            return now >= self._can_fire_after
        elif self._shooting_type == Player.SINGLE_BULLET:
            # if we can only fire once, see if our bullet still exists
            return not self._bullet_exists
        else:
            print("invalid shoot method: {}".format(self._shoot_method))

    @staticmethod
    def _should_shoot():
        """determines whether the input for 'shoot' has been given"""
        result = False

        # is shoot key pressed?
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            result = True

        # TODO: controller support here

        return result

    @staticmethod
    def _horizontal_movement(max_speed):
        """returns how fast to move horizontally up to max speed in either direction"""
        result = 0

        # keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            result -= max_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            result += max_speed

        # TODO: add controller support here?

        # clamp the output to the max speed
        result = max(min(max_speed, result), -max_speed)

        return result
