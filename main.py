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
TIME_SCALE =100

earth = Attractors(
    mass=EARTH_MASS,
    position=(0, 0, 0),
    radius=EARTH_RADIUS,
    texture="data/2k_earth_daymap.jpg"
)
satellite_list = []
attractors = [earth]
button_dict = {}
te = Text(
    position=window.top,
    max_lines=3,
    color=color.white,
    origin=(-0.5, 0.5),
    scale=0.5,
    text="",
    parent=camera.ui,
    enabled=False

)

def button_clicked(name):
    selected_object = satellite_list[satellite_list.index(name)]
    te.text = (
            selected_object.name + '\n' +
            selected_object.tle_line_1 + '\n' +
            selected_object.tle_line_2
    )
    #selected_object.entity.scale*=2
    te.enabled= True

    print('geklickt:', name)
    print(selected_object.tle_line_1)





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
    button_dict[satellite.name] = Func(button_clicked, satellite)

#UI

b1 = ButtonList(button_dict,button_height=1,width=0.3, popup=0,clear_selected_on_enable=True)
b1.position = window.top_left
b1.enabled = False
def input(key):
    if key == 'space':
        b1.enabled = not b1.enabled

b1.on_click= button_clicked


def search_and_highlight(name):
    pass



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