from ursina import *
from time import perf_counter
from attractors import Attractors
from tlefetcher import create_Satellites
from datetime import datetime, timezone, timedelta

app = Ursina()

G = 6.67430e-11
DISPLAY_SCALE_METERS = 1_000_000
EARTH_MASS = 5.972e24
EARTH_RADIUS = 6.371e6

last_frame_time = perf_counter()
simulation_time = datetime.now(timezone.utc)
TIME_SCALE =1000

earth = Attractors(
    mass=EARTH_MASS,
    position=(0, 0, 0),
    radius=EARTH_RADIUS,
    colour=color.blue
)
iss =create_Satellites(25544)
attractors = [earth]
satellite_list = []
if iss is not None:
    satellite_list.append(iss)

print (earth.radius/DISPLAY_SCALE_METERS)


def update():
    global simulation_time, last_frame_time

    current_time = perf_counter()
    dt = current_time - last_frame_time
    last_frame_time = current_time
    simulation_time+=timedelta(seconds=dt*TIME_SCALE)

    for satellite in satellite_list:
        if satellite is not None:
            satellite.update(simulation_time)

    earth.sync_entity()


EditorCamera()

app.run()