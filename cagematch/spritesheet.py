"""this file provides an implementation of a sprite sheet for rendering animations, etc"""


import datetime
import pygame


class SpriteSheet(object):
    """object for holding a sprite sheet, a collection of sprites stored in one source image"""

    def __init__(self, image, sprite_size):
        """constructor"""
        # store parameters
        self._image = image
        self._sprite_size = sprite_size

        # ensure the image is the correct size
        if self._image.get_width() % sprite_size[0] != 0:
            raise Exception("sprite sheet width is not a multiple of its sprite width ({} % {} != 0)".format(
                self._image.get_width(), sprite_size[0]
            ))
        if self._image.get_height() % sprite_size[1] != 0:
            raise Exception("sprite sheet height is not a multiple of its sprite height ({} % {} != 0)".format(
                self._image.get_height(), sprite_size[1]
            ))

        # work out how many rows and columns of sprites fit in this spritesheet
        self._columns = self._image.get_width() / sprite_size[0]
        self._rows = self._image.get_height() / sprite_size[1]

    def draw(self, surface, sprite_id, x, y):
        """method for drawing a particular sprite to a position on the target surface"""
        # figure out where in the sprite sheet the specified sprite is
        src_x = int(sprite_id % self._columns) * self._sprite_size[0]
        src_y = int(sprite_id / self._columns) * self._sprite_size[1]
        # create a rect for the position to read the sprite from
        area = pygame.Rect(src_x, src_y, self._sprite_size[0], self._sprite_size[1])
        # create a rect for the destination to draw to
        dest = pygame.Rect(x, y, self._sprite_size[0], self._sprite_size[1])
        # draw the sprite onto the target surface
        surface.blit(self._image, dest, area)


class Animation(object):
    """keeps a list of frames and manages which frame should be visible"""
    def __init__(self, frame_ids, fps, loops=True):
        """constructor"""
        self._frames = frame_ids
        self._fps = fps
        self._period = datetime.timedelta(seconds=1.0/self._fps)
        self._next_frame = datetime.datetime.now() + self._period
        self._loops = loops
        self._current_frame = 0

    def reset(self):
        """reset the animation to the beginning"""
        self._current_frame = 0
        self._next_frame = datetime.datetime.now() + self._period

    def is_done(self):
        """see if this animation has finished, which is only possible if it doesn't loop"""
        result = False
        if not self._loops:
            result = self._current_frame == (len(self._frames) - 1)
        return result

    def current_sprite_id(self):
        """tells the animation to figure out what sprite ID should be showing currently"""
        while datetime.datetime.now() > self._next_frame:
            self._next_frame += self._period
            self._current_frame += 1
            if self._current_frame >= len(self._frames):
                if self._loops:
                    self._current_frame = 0
                else:
                    self._current_frame -= 1
        return self._frames[self._current_frame]


class AnimatedSpriteSheet(object):
    """combines an animation and sprite sheet to draw the right sprites at the right times"""
    def __init__(self, image, sprite_size):
        """constructor"""
        self._sheet = SpriteSheet(image, sprite_size)
        self._current = Animation([0], 1)
        self._animations = {}

    def add_animation(self, name, animation):
        """add an animation to this animated sprite sheet"""
        self._animations[name] = animation

    def set_animation(self, name):
        """set the current animation using the name given when added"""
        selected = self._animations[name]
        if self._current is not selected:
            self._current = selected
            self._current.reset()

    def current_sprite_id(self):
        """the current sprite ID that should be displayed"""
        return self._current.current_sprite_id()

    def draw(self, surface, x, y):
        """draw the sprite ID indicated by the animation from the spritesheet at the desired position"""
        self._sheet.draw(surface, self.current_sprite_id(), x, y)

