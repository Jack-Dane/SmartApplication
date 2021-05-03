from Models.ModelAPI import API
import requests
import threading
import sys
import datetime


class WeatherApi(API):

    def __init__(self):
        super(WeatherApi, self).__init__()

        self.data = self.OpenAPIData()

        try:
            self.data = self.data["weather"]
            self.location = self.data["location"]
            self.apiKey = self.data["api_key"]
        except KeyError as keyException:
            print("KeyError - Weather API: Variables not defined in the api data json")
            raise keyException

        self.url = "http://api.openweathermap.org/data/2.5/forecast?q=" + self.location + "&appid=" + self.apiKey + "&units=metric"
        self.days = []
        # set time and temp into different days
        self.setDays()

    def setDays(self):
        try:
            weatherRequest = requests.get(self.url)
            weatherRequest.raise_for_status()
        except Exception as exception:
            print(exception)
            raise exception

        weatherRequest = weatherRequest.json()

        days = []
        # placing the weather data into days that can be read by the display
        for val in weatherRequest.get("list"):
            weatherDate = datetime.datetime.strptime(val["dt_txt"], "%Y-%m-%d %H:%M:%S").date()
            temp = val["main"]["temp"]
            imgIcon = val["weather"][0]["icon"]

            if len(days) == 0:
                low = val["main"]["temp_min"]
                high = val["main"]["temp_max"]
                day = self.Today(weatherDate, float(temp), imgIcon, high, low)
                days.append(day)
            elif weatherDate != days[len(days) - 1].day:
                day = self.Day(weatherDate, float(temp), imgIcon)
                days.append(day)
            else:
                if len(self.days) != 0:
                    days[len(days) - 1].addDay(temp, imgIcon)

        # Check to see if the new weather data is the same as previous weather data
        equal = self.CheckDataForChanges(self.days, days)

        # if weather data has changed update the display else do nothing
        if not equal:
            self.days = days
            self.NotifyObservers()

        threading.Timer(1, self.setDays).start()

    def GetToday(self):
        return self.days[0]

    def GetDays(self):
        return self.days

    class Day:

        def __init__(self, day, temp, imgIconId):
            self.days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            self.temp = temp
            self.day = day
            self.imgIconId = imgIconId

        def addDay(self, temp, imgIconId):
            if temp > self.temp:
                self.temp = temp
                self.imgIconId = imgIconId

        def DayOfWeek(self):
            return self.days[self.day.weekday()]

        def GetTemp(self):
            return str(round(self.temp))

        def GetIcon(self):
            return "http://openweathermap.org/img/wn/" + self.imgIconId + "@2x.png"

        def __eq__(self, other):
            if isinstance(other, self.__class__):
                return self.temp == other.temp and self.day == other.day and self.imgIconId == other.imgIconId
            return False

    class Today(Day):

        def __init__(self, day, temp, imgIconId, high, low):
            self.high = high
            self.low = low
            super().__init__(day, temp, imgIconId)

        def GetHigh(self):
            return str(round(self.high))

        def GetLow(self):
            return str(round(self.low))
