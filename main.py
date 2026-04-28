from ursina import *
import json
from time import perf_counter
from trackedSatellites import TrackedSatellites
from attractors import Attractors
from datetime import datetime, timezone, timedelta

app = Ursina()

DISPLAY_SCALE_METERS = 1_000_000
EARTH_MASS = 5.972e24
EARTH_RADIUS = 6.371e6
CACHE_FILE = Path("data/tle_cache_old_api.json")
last_frame_time = perf_counter()
simulation_time = datetime.now(timezone.utc)
TIME_SCALE =10

earth = Attractors(
    mass=EARTH_MASS,
    position=(0, 0, 0),
    radius=EARTH_RADIUS,
    colour=color.blue
)
satellite_list = []
attractors = [earth]


def load_cached_satellites():
    with open(CACHE_FILE, "r",encoding="utf-8") as file:
        data=json.load(file)

    return data["satellites"]



for data in load_cached_satellites():
    satellite = TrackedSatellites (
        name = data["name"],
        tle_line_1=data["line1"],
        tle_line_2=data["line2"],
        colour=color.red,
        radius =0.05
    )
    satellite_list.append(satellite)


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