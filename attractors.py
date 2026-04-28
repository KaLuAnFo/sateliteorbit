from ursina import *

DISPLAY_SCALE = 1_000_000


class Attractors:
    def __init__(self, mass, position, radius, texture=None):
        self.mass = mass
        self.position = Vec3(position)
        self.radius = radius

        self.texture = texture

        self.entity = Entity(
            model="sphere",
            position=self.position / DISPLAY_SCALE,
            scale=self.radius / DISPLAY_SCALE,
            texture=self.texture
        )

    def sync_entity(self):
        self.entity.position = self.position