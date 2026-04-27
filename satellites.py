from ursina import *

DISPLAY_SCALE = 1_000_000
G = 6.67430e-11


class Satellites:
    def __init__(self, position, velocity, radius, colour, primary):
        self.position = Vec3(position)
        self.velocity = Vec3(velocity)
        self.acceleration = Vec3(0, 0, 0)

        self.radius = radius
        self.colour = colour
        self.primary = primary

        self.entity = Entity(
            model="sphere",
            position=self.position / DISPLAY_SCALE,
            scale=self.radius / DISPLAY_SCALE,
            color=self.colour
        )

    def calculate_acceleration(self, attractors):
        total_acceleration = Vec3(0, 0, 0)

        for attractor in attractors:
            r_vec = attractor.position - self.position
            r = r_vec.length()

            if r == 0:
                continue

            acceleration = G * attractor.mass * r_vec / r**3
            total_acceleration += acceleration

        self.acceleration = total_acceleration

    def update_physics(self, dt):
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt

    def sync_entity(self):
        self.entity.position = self.position / DISPLAY_SCALE

    def update(self, dt, attractors):
        self.calculate_acceleration(attractors)
        self.update_physics(dt)
        self.sync_entity()