import json
from geocoding import Geocoding
from weather import Weather
 
class Main:
    @staticmethod
    def run():
        geocodee = 1
        weather = 1
        reversee = 1
        queries = []
        results = []  # List to store results in order
        result = None  # Initialize result outside the if block

        try:
            while True:
                detail = input().strip()
                if detail == "NO MORE QUERIES":
                    break
                queries.append(detail)

            reverse = input()

            if queries:
                # Parse the first line
                target_detail = queries[0].split()
                target_type, location_info = target_detail[1], " ".join(target_detail[2:])

                if target_type == "NOMINATIM":
                    geocode_result = Geocoding.geocode_location(location_info)
                    if not geocode_result:
                        print("FAILED")
                        print("Location not found")
                        return  # Stop execution if geocoding fails
                elif target_type == "FILE":
                    file_path = location_info
                    try:
                        with open(file_path, "r") as file:
                            data = json.load(file)
                            location = data[0]["display_name"]
                        geocode_result = Geocoding.geocode_location(location)
                        geocodee = None
                    except FileNotFoundError:
                        print("FAILED")
                        print(file_path)
                        print("MISSING")
                        return
                    except json.JSONDecodeError:
                        print("FAILED")
                        print(file_path)
                        print("FORMAT")
                        return

                # Parse the second line
                weather_detail = queries[1].split()
                weather_type, weather_info = weather_detail[1], " ".join(weather_detail[2:])

                if weather_type == "NWS":
                    result = Weather.build_search_url(geocode_result['lat'], geocode_result['lon'])
                elif weather_type == "FILE":
                    file_path = weather_info
                    try:
                        with open(file_path, "r") as file:
                            result = json.load(file)
                    except FileNotFoundError:
                        print("FAILED")
                        print(file_path)
                        print("MISSING")
                        return
                    except json.JSONDecodeError:
                        print("FAILED")
                        print(file_path)
                        print("FORMAT")
                        return
                    weather = None

            # Process queries
            temp_result = None
            humidity_result = None
            wind_result = None
            precipitation_result = None
            feels_result = None

            for detail in queries[2:]:
                words = detail.split()

                if len(words) >= 2:
                    limit, length = words[-1], words[-2]

                    if "TEMPERATURE AIR" in detail:
                        scale = words[-3]
                        temp_result = Weather.extreme_temp(result, int(length), limit, scale)
                        results.append(("Temperature", temp_result))
                    elif "HUMIDITY" in detail:
                        humidity_result = Weather.extreme_humidity(result, int(length), limit)
                        results.append(("Humidity", humidity_result))
                    elif "WIND" in detail:
                        wind_result = Weather.extreme_wind(result, int(length), limit)
                        results.append(("Wind", wind_result))
                    elif "PRECIPITATION" in detail:
                        precipitation_result = Weather.extreme_precipitation(result, int(length), limit)
                        results.append(("Precipitation", precipitation_result))
                    elif "TEMPERATURE FEELS" in detail:
                        scale = words[-3]
                        feels_result = Weather.temp_feels(result, int(length), limit, scale)
                        results.append(("Temperature Feels", feels_result))

            # Prints reverse geocode either from API or from file
            if reverse.startswith("REVERSE NOMINATIM"):
                Geocoding.reverse_geocode(geocode_result['lat'], geocode_result['lon'])
            elif reverse.startswith("REVERSE FILE"):
                file_path = reverse.split(" ")[-1]  # Extracting the file path from the input
                with open(file_path, "r") as file:
                    reverse_geocode_data = json.load(file)
                    print(reverse_geocode_data['display_name'])
                reversee = None

            # Print results after both functions are called
            for query_type, result in results:
                if result is not None:
                    value, unit = result
                    if query_type == "Wind":
                        print(f'{value} {unit:.4f} mph')
                    elif query_type == "Humidity" or query_type == "Precipitation":
                        print(f'{value} {unit:.4f} %')
                    else:
                        print(f'{value} {unit:.4f}')

            if geocodee is not None:
                print("**Forward geocoding data from OpenStreetMap")
            if reversee is not None:
                print("**Reverse geocoding data from OpenStreetMap")
            if weather is not None:
                print("**Real-time weather data from the National Weather Service, United States Department of Commerce")

        except KeyboardInterrupt:
            print("Execution interrupted.")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == '__main__':
    Main.run()
    