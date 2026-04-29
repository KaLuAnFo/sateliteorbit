from ursina import *

DISPLAY_SCALE = 1_000_000


class Attractors:
    def __init__(self, mass, position, radius):
        self.mass = mass
        self.position = Vec3(position)
        self.radius = radius

        self.texture = texture

        self.entity = Entity(
            model="sphere",
            position=self.position / DISPLAY_SCALE,
            scale=self.radius / DISPLAY_SCALE,
            texture="data/world.topo.bathy.200401.3x21600x10800.jpg",
            rotation_y =270,
            #rotation_z =180
        )

    def sync_entity(self):
        self.entity.position = self.position