from Models.ModelAPI import API
import threading
import requests


class LocationApi(API):

    def __init__(self):
        super(LocationApi, self).__init__()

        self.locations = []

        self.data = self.OpenAPIData()

        try:
            self.data = self.data["directions"]
            self.home = self.Home(self.data["home"]["lon"], self.data["home"]["lat"])
            self.api_key = self.data["api_key"]
        except KeyError as keyException:
            print("KeyError - Location API: Variables not defined in the api data json")
            raise keyException

        self.GetLocations(self.api_key)

    def GetLocations(self, api_key):
        locations = []

        for place in self.data.get("locations"):
            locations.append(self.Location(place.get("name"), place.get("lon"), place.get("lat"), place.get("transport")))

        for location in locations:
            location.CalculateTime(self.home, api_key)

        same = True
        if len(self.locations) > 0:
            for i in range(0, len(locations)):
                if not (self.locations[i] == locations[i]):
                    same = False
                    break
        else:
            same = False

        if not same:
            self.locations = locations
            self.NotifyObservers()

        threading.Timer(60, self.GetLocations, [api_key]).start()

    class Home:
        def __init__(self, lon, lat):
            self.lon = str(lon)
            self.lat = str(lat)

    class Location(Home):
        def __init__(self, name, lon, lat, travel):
            self.name = name
            self.travel = travel
            self.time = ""
            self.traffic = ""

            if self.travel == "car":
                self.source = "Icons/car.jpg"
            elif self.travel == "pedestrian":
                self.source = "Icons/walk.png"
            super().__init__(lon, lat)

        def CalculateTime(self, home, api_key):
            query = "https://api.tomtom.com/routing/1/calculateRoute/"
            query += home.lat + "," + home.lon + ":"
            query += self.lat + "," + self.lon + "/json?"
            query += "key=" + api_key
            query += "&travelMode=" + self.travel

            try:
                response = requests.get(query)
                response.raise_for_status()
            except Exception as exception:
                print(exception)
                raise exception

            data = response.json()

            self.time = str(round(data["routes"][0]["summary"]["travelTimeInSeconds"] / 60))
            self.traffic = str(round(data["routes"][0]["summary"]["trafficDelayInSeconds"] / 60))

        def GetTime(self):
            return self.time + "mins"

        def GetTraffic(self):
            return "Delay: " + self.traffic + "mins"

        def __eq__(self, other):
            if isinstance(other, self.__class__):
                return self.name == other.name and self.time == other.time and self.travel == other.travel
            return False
