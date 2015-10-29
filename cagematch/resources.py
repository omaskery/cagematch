"""this file manages the retrieving of content resources like images from disk"""


import zipfile
import pygame
import io


class Resources(object):
    def __init__(self, asset_pack_path):
        self._path = asset_pack_path
        self._handle = zipfile.ZipFile(self._path)

    def get(self, resource_name):
        return self._handle.open(resource_name)

    def get_image(self, resource_name):
        resource_stream = self.get(resource_name)
        stream = io.BytesIO(resource_stream.read())
        return pygame.image.load(stream, resource_name)
