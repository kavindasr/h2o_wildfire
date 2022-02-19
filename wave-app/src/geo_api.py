from http.client import responses
import requests
from concurrent.futures import ThreadPoolExecutor

def get_address(url):
    # url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    res = requests.get(url)
    address = res.json()
    return address["display_name"]

def get_res(list_of_urls):
    with ThreadPoolExecutor(max_workers=10) as pool:
        response_list = list(pool.map(get_address,list_of_urls))
        return response_list