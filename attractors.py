from ursina import *

DISPLAY_SCALE = 1_000_000


class Attractors:
    def __init__(self, mass, position, radius, colour):
        self.mass = mass
        self.position = Vec3(position)
        self.radius = radius
        self.colour = colour

        self.entity = Entity(
            model="sphere",
            position=self.position / DISPLAY_SCALE,
            scale=self.radius / DISPLAY_SCALE,
            color=self.colour
        )

    def sync_entity(self):
        self.entity.position = self.position