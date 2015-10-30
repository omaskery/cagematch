"""code pertaining to projectiles in the game"""

from ..spritesheet import AnimatedSpriteSheet, Animation
from .entity import Entity
import pygame


class Projectile(Entity):
    """an entity that is a projectile"""

    def __init__(self, pos, velocity, appearance, sprite):
        """constructor"""
        super().__init__()
        size = 10, 10
        # set up sprite and animation
        self._sprite = AnimatedSpriteSheet(sprite, size)
        self._sprite.add_animation("test", Animation([
            0, 1
        ], 3))
        self._sprite.set_animation("test")
        # create a rectangle to represent ourselves
        self._rect = pygame.Rect(pos, size)
        # centre the rectangle on the spawn position
        self._rect.center = pos
        # remember our velocity
        self._vel = velocity
        # store some appearance information
        self._appearance = appearance

    def think(self, dt):
        """simulation event"""
        # just move based on our velocity
        self._rect.move_ip(self._vel)

    def render(self, bounds, dest):
        """render event"""
        # if we leave the visible screen, flag ourselves as dead
        if not bounds.colliderect(self._rect):
            self.die()
        # otherwise draw ourself
        else:
            self._sprite.draw(dest, self._rect.x, self._rect.y)
            # pygame.draw.rect(dest, self._appearance, self._rect)
