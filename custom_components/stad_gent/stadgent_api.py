"""API client for StadGent"""
from .const import PARKINGS_URI
from requests import get


class StadGentAPI:
    def getParkings(self):
        headers = {"Accept-Encoding": "gzip", "origin": "https://stad.gent"}

        try:
            response = get(url=PARKINGS_URI, headers=headers)

            if response.status_code != 200:
                raise StadGentAPIError()

            jsonResult = response.json()

            return jsonResult["records"]
        except:
            raise StadGentAPIError()


class StadGentAPIError(Exception):
    pass