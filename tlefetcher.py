import requests
from trackedSatellites import TrackedSatellites
from ursina import *

base_URL = "https://tle.ivanstanojevic.me/api/tle/"

def get_info(tracking_number):
    url = base_URL + str(tracking_number)
    headers = {
        "User-Agent": "sateliteorbit"
    }
    try:
        response = requests.get(url, headers= headers,timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print("API Fehler:",response.status_code)
            print(response.text)
            return None
    except requests.exceptions.RequestException as error:
        print("Request Error:",error)
        return None




def create_Satellites(tracking_number):

    data = get_info(tracking_number)
    if data is None:
        print("Keine Daten erhalten")
        return None
    if "line1" not in data or "line2" not in data or "name" not in data:
        return None
    if data["line1"] is None or data["line2"] is None:
        return None

    print(data)
    try:
        trackedSatellite = TrackedSatellites(
            name=data["name"],
            tle_line_1=data["line1"],
            tle_line_2=data["line2"],
            colour=color.red,
            radius=0.1

        )
        return trackedSatellite
    except Exception as error:
        print(error)
        return None
