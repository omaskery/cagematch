"""code pertaining to the playable entity in the game"""
from .entity import Entity
import pygame


class Enemy(Entity):
    """this object represents the enemy entities in the game"""

    # represent directions of movement, enemies in this game just slide left and right
    # something external will tell them which direction to go
    LEFT = 0
    RIGHT = 1
    # the default movement speed
    DEFAULT_SPEED = 1

    def __init__(self, pos):
        """constructor"""
        super().__init__()

        self._direction = Enemy.LEFT
        self._speed = Enemy.DEFAULT_SPEED

        # figure out spawn position
        size = 32, 32
        self._rect = pygame.Rect(pos, size)

    def set_movement(self, direction, speed):
        """set properties of the enemies movement (direction & speed)"""
        self._direction = direction
        self._speed = speed

    def render(self, bounds, dest):
        """render event"""
        pygame.draw.rect(dest, (0, 255, 0), self._rect)

    def think(self, dt):
        """simulation event"""
        dx = 0
        # if we should be going left, set delta x to left
        if self._direction == Enemy.LEFT:
            dx -= self._speed
        # otherwise right
        elif self._direction == Enemy.RIGHT:
            dx += self._speed
        # move
        self._rect.move_ip(dx, 0)
