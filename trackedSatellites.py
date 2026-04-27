from ursina import *
from skyfield.api import EarthSatellite, load

EARTH_RADIUS = 6.371e6/1_000_000
DISPLAY_SCALE_KM = 1_000

class TrackedSatellites:
    def __init__(self,name,tle_line_1,tle_line_2, colour,radius):
        self.name = name
        self.tle_line_1 = tle_line_1
        self.tle_line_2 = tle_line_2
        self.colour = colour
        self.radius = radius
        self.timescale = load.timescale()
        self.skyfield_satellite = EarthSatellite(
            self.tle_line_1,
            self.tle_line_2,
            self.name,
            self.timescale
        )
        self.entity = Entity(model="sphere",
                             color=color.red,
                             scale=self.radius
                             )

    def update(self, simulation_time):
        t = self.timescale.from_datetime(simulation_time)
        geocentric = self.skyfield_satellite.at(t)

        x , y , z = geocentric.position.km

        self.entity.position = Vec3(
            x/DISPLAY_SCALE_KM ,
            y/DISPLAY_SCALE_KM ,
            z/DISPLAY_SCALE_KM
        )