"""code pertaining to the playable entity in the game"""
from .entity import Entity, EntityContainer
import random
import pygame


class EnemyController(EntityContainer):

    def __init__(self, resolution, starting_speed, max_speed, advance_speed=1):
        super().__init__()
        self._current_direction = random.choice([Enemy.RIGHT, Enemy.LEFT])
        self._current_speed = starting_speed
        self._max_speed = max_speed
        self._advance_speed = advance_speed
        space_ratio = 0.05
        self._left_boundary = resolution[0] * space_ratio
        self._right_boundary = resolution[0] * (1.0 - space_ratio)

    def add(self, entity):
        super().add(entity)
        entity.set_movement(self._current_direction, self._current_speed)

    def think(self, *args):
        super().think(args)
        turn_around = False
        if self._current_direction == Enemy.LEFT:
            left_most = self._find_leftmost()
            if left_most < self._left_boundary:
                turn_around = True
        elif self._current_direction == Enemy.RIGHT:
            right_most = self._find_rightmost()
            if right_most > self._right_boundary:
                turn_around = True
        else:
            print("invalid direction: {}".format(self._current_direction))
        if turn_around:
            self._change_direction()

    def _find_leftmost(self):
        leftmost = None
        for entity in self._entities:
            if leftmost is None or entity.leading_edge < leftmost.x_position:
                leftmost = entity
        if leftmost is None:
            return None
        else:
            return leftmost.leading_edge

    def _find_rightmost(self):
        rightmost = None
        for entity in self._entities:
            if rightmost is None or entity.leading_edge > rightmost.x_position:
                rightmost = entity
        if rightmost is None:
            return None
        else:
            return rightmost.leading_edge

    def _change_direction(self):
        if self._current_direction == Enemy.LEFT:
            self._current_direction = Enemy.RIGHT
        else:
            self._current_direction = Enemy.LEFT
        if self._current_speed < self._max_speed:
            self._current_speed += 1
        for enemy in self._entities:
            enemy.set_movement(self._current_direction, self._current_speed)
            enemy.advance(self._advance_speed)


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

    @property
    def leading_edge(self):
        """returns the x position of the leading edge of the enemy"""
        if self._direction == Enemy.LEFT:
            return self._rect.x
        else:
            return self._rect.x + self._rect.w

    def advance(self, amount):
        """advances the enemy down the screen by an amount"""
        self._rect.move_ip(0, amount)

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
