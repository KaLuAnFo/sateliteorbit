import json
from pathlib import Path
from datetime import datetime, timezone

import requests


BASE_URL = "https://tle.ivanstanojevic.me/api/tle"

CACHE_DIR = Path("data")
CACHE_FILE = CACHE_DIR / "tle_cache_old_api.json"

SEARCH_GROUPS = [
    "ISS",
    "STARLINK",
    "ONEWEB",
    "GPS",
    "GALILEO",
    "BEIDOU",
    "GLONASS",
    "NOAA",
    "GOES",
    "METEOR",
    "IRIDIUM",
    "INTELSAT",
    "SES",
    "HUBBLE",
    "LANDSAT",
    "TERRA",
    "AQUA",
    "SENTINEL",
    "COSMOS",
    "CUBESAT",
    "AMATEUR",
    "WEATHER",
    "COMMUNICATION",
]


def fetch_search(search_term):
    params = {
        "search": search_term,
    }

    headers = {
        "User-Agent": "satellite-orbit-project/1.0"
    }

    response = requests.get(
        BASE_URL,
        params=params,
        headers=headers,
        timeout=20
    )

    response.raise_for_status()
    return response.json()


def extract_satellites(api_response):
    """
    Die API kann je nach Endpoint unterschiedlich antworten.
    Diese Funktion versucht mehrere mögliche Formate abzufangen.
    """

    if api_response is None:
        return []

    if isinstance(api_response, list):
        return api_response

    if isinstance(api_response, dict):
        if "member" in api_response:
            return api_response["member"]

        if "satellites" in api_response:
            return api_response["satellites"]

        if "data" in api_response:
            return api_response["data"]

        if "name" in api_response and "line1" in api_response and "line2" in api_response:
            return [api_response]

    return []


def is_valid_tle_satellite(satellite):
    return (
        satellite is not None
        and satellite.get("name") is not None
        and satellite.get("line1") is not None
        and satellite.get("line2") is not None
    )


def normalize_satellite(satellite, search_group):
    norad_id = (
        satellite.get("satelliteId")
        or satellite.get("satellite_id")
        or satellite.get("norad_cat_id")
        or satellite.get("noradId")
        or satellite.get("id")
    )

    return {
        "name": satellite.get("name"),
        "norad_id": norad_id,
        "line1": satellite.get("line1"),
        "line2": satellite.get("line2"),
        "source_group": search_group,
        "groups": [search_group],
        "raw": satellite,
    }


def fetch_all_groups():
    satellites_by_key = {}
    errors = []

    for search_group in SEARCH_GROUPS:
        print(f"Lade Suchgruppe: {search_group}")

        try:
            response_json = fetch_search(search_group)
            satellites = extract_satellites(response_json)

            print(f"  gefunden: {len(satellites)}")

            for satellite in satellites:
                if not is_valid_tle_satellite(satellite):
                    continue

                normalized = normalize_satellite(satellite, search_group)

                key = normalized["norad_id"]

                if key is None:
                    key = normalized["name"]

                key = str(key)

                if key not in satellites_by_key:
                    satellites_by_key[key] = normalized
                else:
                    existing = satellites_by_key[key]

                    if search_group not in existing["groups"]:
                        existing["groups"].append(search_group)

        except Exception as error:
            print(f"  Fehler bei {search_group}: {error}")

            errors.append({
                "group": search_group,
                "error": str(error)
            })

    return {
        "saved_at": datetime.now(timezone.utc).isoformat(),
        "source": "tle.ivanstanojevic.me",
        "base_url": BASE_URL,
        "search_groups": SEARCH_GROUPS,
        "count": len(satellites_by_key),
        "errors": errors,
        "satellites": list(satellites_by_key.values()),
    }


def save_cache(data):
    CACHE_DIR.mkdir(exist_ok=True)

    with open(CACHE_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    print()
    print(f"Gespeichert in: {CACHE_FILE}")
    print(f"Satelliten insgesamt: {data['count']}")
    print(f"Fehlerhafte Suchgruppen: {len(data['errors'])}")


def main():
    data = fetch_all_groups()
    save_cache(data)


if __name__ == "__main__":
    main()