"""code pertaining to the playable entity in the game"""
from .entity import Entity, EntityContainer
import random
import pygame


class EnemyController(EntityContainer):
    """manages a collection of enemies' behaviour"""

    def __init__(self, resolution, starting_speed, max_speed, shoot_method, advance_speed=2):
        """constructor"""
        super().__init__()
        # decide the initial direction of enemies
        self._current_direction = random.choice([Enemy.RIGHT, Enemy.LEFT])
        # store  parameters
        self._current_speed = starting_speed
        self._max_speed = max_speed
        self._advance_speed = advance_speed
        self._shoot_method = shoot_method
        # number of bullets in the air from enemies
        self._bullets_flying = 0
        self._max_flying_bullets = 1
        # figure out the bounds of where enemies can move
        space_ratio = 0.05
        bound_x, bound_y = resolution[0] * space_ratio, resolution[1] * space_ratio
        bound_w = resolution[0] * (1.0 - 2.0 * space_ratio)
        bound_h = resolution[1] * (1.0 - 2.0 * space_ratio)
        self._bounds = pygame.Rect(bound_x, bound_y, bound_w, bound_h)

    def populate(self, rows, columns, x_spacing, y_spacing):
        """generate a collection of enemies given a number and spacing between them"""
        width = columns * x_spacing
        start_x = self._bounds.centerx - width / 2
        start_y = self._bounds.top
        for y in range(rows):
            for x in range(columns):
                spawn_x = start_x + x_spacing * x
                spawn_y = start_y + y_spacing * y
                enemy = Enemy((spawn_x, spawn_y))
                self.add(enemy)

    def add(self, entity):
        """override 'add entity to container' behaviour to set their movement/speed to match all enemies"""
        super().add(entity)
        entity.set_movement(self._current_direction, self._current_speed)
        entity.set_death_callback(self._enemy_died)

    def think(self, dt):
        """simulation event"""
        # update all contained entities
        super().think(dt)
        if len(self._entities) > 0:
            self._check_for_direction_change()
            self._attempt_shooting()

    def _check_for_direction_change(self):
        """checks to see if enemies need to change direction"""
        # decide whether the enemies need to change direction
        turn_around = False
        if self._current_direction == Enemy.LEFT:
            left_most = self._find_leftmost()
            if left_most < self._bounds.left:
                turn_around = True
        elif self._current_direction == Enemy.RIGHT:
            right_most = self._find_rightmost()
            if right_most > self._bounds.right:
                turn_around = True
        else:
            print("invalid direction: {}".format(self._current_direction))
        # if so, change direction
        if turn_around:
            self._change_direction()

    def _attempt_shooting(self):
        """checks to see if any enemies should fire at the player"""
        if self._bullets_flying < self._max_flying_bullets:
            if random.random() <= 0.005:
                firing = random.choice(self._entities)
                bullet_origin = firing._rect.midbottom
                self._bullets_flying += 1
                self._shoot_method(bullet_origin, self._bullet_died)

    def _bullet_died(self, bullet):
        """callback called when a bullet from an enemy dies"""
        _ = bullet
        self._bullets_flying -= 1

    def _find_leftmost(self):
        """identifies which enemy is the furthest left, and returns the x position of their leading edge"""
        leftmost = None
        for entity in self._entities:
            if leftmost is None or entity.leading_edge < leftmost.leading_edge:
                leftmost = entity
        if leftmost is None:
            return None
        else:
            return leftmost.leading_edge

    def _find_rightmost(self):
        """identifies which enemy is furthest right, and returns the x position of their leading edge"""
        rightmost = None
        for entity in self._entities:
            if rightmost is None or entity.leading_edge > rightmost.leading_edge:
                rightmost = entity
        if rightmost is None:
            return None
        else:
            return rightmost.leading_edge

    def _change_direction(self):
        """changes the direction of all enemies, increases their speed and advances them down the screen"""
        if self._current_direction == Enemy.LEFT:
            self._current_direction = Enemy.RIGHT
        else:
            self._current_direction = Enemy.LEFT
        if self._current_speed < self._max_speed:
            self._current_speed += 0.1
        for enemy in self._entities:
            enemy.set_movement(self._current_direction, self._current_speed)
            enemy.advance(self._advance_speed)

    def _enemy_died(self, enemy):
        """callback when an enemy dies, used to make the last enemy speed up"""
        _ = enemy
        if len(self._entities) == 2:
            print("last enemy!")
            self._current_speed *= 2
            self._entities[0].set_movement(self._current_direction, self._current_speed)


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

        # default direction & speed
        self._direction = Enemy.LEFT
        self._speed = Enemy.DEFAULT_SPEED

        # figure out spawn position
        size = 64, 64
        # store a floating point x position as well as rect, so we can manually implement
        # smoother movement slower than 1 pixel per simulation update
        self._real_xpos = float(pos[0])
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
        self._real_xpos += dx
        self._rect.x = int(self._real_xpos)

