from ursina import *
from skyfield.api import EarthSatellite, load, wgs84

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

        subpoint = wgs84.subpoint(geocentric)

        lat_deg = subpoint.latitude.degrees
        lon_deg = subpoint.longitude.degrees
        alt_km = subpoint.elevation.km

        if not all(math.isfinite(value) for value in [lat_deg, lon_deg, alt_km]):
            self.entity.enabled = False
            return

        self.entity.enabled = True

        lat = math.radians(lat_deg)
        lon = math.radians(-lon_deg)

        earth_radius_km = 6371
        r = (earth_radius_km + alt_km) / DISPLAY_SCALE_KM / 2

        x = r * math.cos(lat) * math.sin(lon)
        y = r * math.sin(lat)
        z = r * math.cos(lat) * math.cos(lon)

        self.entity.position = Vec3(x, y, z)