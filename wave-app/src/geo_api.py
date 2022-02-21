import requests


def get_address(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    res = requests.get(url)
    address = res.json()
    return address["display_name"]


def get_location(city, state):
    url = f"https://nominatim.openstreetmap.org/search?city={city}&state={state}&country=Australia&format=json"
    res = requests.get(url)
    resJson = res.json()
    return (resJson.lat, resJson.lon)
