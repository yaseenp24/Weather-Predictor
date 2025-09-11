


import json
import urllib.parse
import urllib.request
import time

class Geocoding:
    BASE_URL_REVERSE = "https://nominatim.openstreetmap.org/reverse"
    BASE_URL_NOMINATIM = 'https://nominatim.openstreetmap.org/search'

    @staticmethod
    def get_result(url: str) -> dict:
        response = None

        try:
            headers = {'User-Agent': 'yaseenp@uci.edu'}
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            if response.getcode() != 200:
                print("FAILED!")
                print(f"{response.getcode()} {url}")
                print("NOT 200")
                return {}

            json_text = response.read().decode(encoding='utf-8')
            return json.loads(json_text)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print("FAILED!")
                print(f"{e.code} {url}")
                print("NOT 200")
            else:
                print("FAILED!")
                print(f"{e.code} {url}")
                print("NOT 200")
            return {}
        except urllib.error.URLError as e:
            print("FAILED!")
            print(f"{url}")
            print("NETWORK")
            return {}
        except Exception as e:
            print("FAILED!")
            print(f"{url}")
            print("FORMAT")
            return {}
        finally:
            if response is not None:
                response.close()

    @staticmethod
    def geocode_location(location: str) -> dict:
        query_parameters = {
            'q': location,
            'format': 'json',
            'limit': 1
        }

        url = f'{Geocoding.BASE_URL_NOMINATIM}?{urllib.parse.urlencode(query_parameters)}'
        result = Geocoding.get_result(url)

        if result:
            result = result[0]  # Return the first result as a dictionary
        else:
            print("Error: Location unknown")
            return {}

        boundingbox = result['boundingbox']
        print("TARGET ", end='')
        print(f'{boundingbox[1]}/N ', end='')
        print(f'{abs(float(boundingbox[3]))}/W')
        return result

    @staticmethod
    def reverse_geocode(lat: float, lon: float):
        query_parameters = {
            'lat': lat,
            'lon': lon,
            'format': 'json',
        }

        url = f'{Geocoding.BASE_URL_REVERSE}?{urllib.parse.urlencode(query_parameters)}'
        result = Geocoding.get_result(url)

        display_name = result['display_name']
        print(f'{display_name}', end='')
        print()
        return result
 