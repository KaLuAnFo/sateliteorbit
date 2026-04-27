
from ursina import *
from attractors import Attractors
from satellites import Satellites

app = Ursina()

G = 6.67430e-11

EARTH_MASS = 5.972e24
EARTH_RADIUS = 6.371e6

SATELLITE_ALTITUDE = 400_000
SATELLITE_ORBIT_RADIUS = EARTH_RADIUS + SATELLITE_ALTITUDE

SATELLITE_ORBIT_VELOCITY = math.sqrt(
    G * EARTH_MASS / SATELLITE_ORBIT_RADIUS
)

earth = Attractors(
    mass=EARTH_MASS,
    position=(0, 0, 0),
    radius=EARTH_RADIUS,
    colour=color.blue
)

satellite = Satellites(
    position=(SATELLITE_ORBIT_RADIUS, 0, 0),
    velocity=(0, 0, SATELLITE_ORBIT_VELOCITY),
    radius=200_000,
    colour=color.red,
    primary=earth
)

attractors = [earth]
satellite_list = [satellite]

TIME_SCALE = 10


def update():
    dt = 1 * TIME_SCALE

    for satellite in satellite_list:
        satellite.update(dt, attractors)

    earth.sync_entity()


EditorCamera()

app.run()