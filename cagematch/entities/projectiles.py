"""code pertaining to projectiles in the game"""

from .entity import Entity
import pygame


class Projectile(Entity):
    """an entity that is a projectile"""

    def __init__(self, pos, velocity, appearance):
        """constructor"""
        super().__init__()
        size = 10, 10
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
            pygame.draw.rect(dest, self._appearance, self._rect)
