"""code pertaining to the playable entity in the game"""
from .entity import Entity
import pygame


class Player(Entity):
    """this object represents the player entity in the game"""

    def __init__(self, resolution):
        """constructor"""
        super().__init__()
        size = 32, 32
        start_x = (resolution[0] - size[0]) / 2
        start_y = resolution[1] - 2 * size[1]
        start_pos = start_x, start_y
        self._rect = pygame.Rect(start_pos, size)
        self._player_bounds = pygame.Rect(size[0], start_y, resolution[0] - size[0] * 2, size[1])

    def render(self, bounds, dest):
        """render event"""
        pygame.draw.rect(dest, (255, 0, 0), self._rect)

    def think(self, dt):
        """simulation event"""
        max_speed = 3
        dx = Player._horizontal_movement(max_speed)
        self._rect.move_ip(dx, 0)
        self._rect.clamp_ip(self._player_bounds)

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
