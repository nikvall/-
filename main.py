import sys
from io import BytesIO
import requests
from PIL import Image


toponym_to_find = " ".join(sys.argv[1:])


geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    pass

json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
toponym_size = toponym['boundedBy']['Envelope']
toponym_coodrinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

delta_longi = str(float(toponym_size['upperCorner'].split()[0]) - float(toponym_size['lowerCorner'].split()[0]))
delta_latti = str(float(toponym_size['upperCorner'].split()[1]) - float(toponym_size['lowerCorner'].split()[1]))

map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join([delta_longi, delta_latti]),
    "l": "map"
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()