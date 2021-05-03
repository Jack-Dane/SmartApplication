from kivy.clock import Clock
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from Models.WeatherAPI import WeatherApi
from Models.GoogleCalendarApi import GoogleCalendarApi
from Models.LocationApi import LocationApi
from Models.SpotifyApi import SpotifyApi
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from datetime import datetime


class LeftSideDisplay(StackLayout):
    def __init__(self, **kwargs):
        super(LeftSideDisplay, self).__init__(**kwargs)
        # TRY, EXCEPT, PASS to allow the app to continue to allow for modular design

        try:
            self.add_widget(WeatherDisplay())
        except Exception as e:
            print(e)

        try:
            self.add_widget(CalendarDisplay())
        except Exception as e:
            print(e)

        try:
            self.add_widget(TravelDisplay())
        except Exception as e:
            print(e)

        try:
            self.add_widget(SpotifyDisplay())
        except Exception as e:
            print(e)


class CalendarDisplay(StackLayout):
    def __init__(self, **kwargs):
        super(CalendarDisplay, self).__init__(**kwargs)
        self.calendar = GoogleCalendarApi()
        self.calendar.AddObserver(self)

    def Update(self, *args):
        self.clear_widgets()
        self.count = 0
        self.events = self.calendar.returnEvents()

        try:
            for event in self.events:
                calEvent = CalendarEvent()
                calEvent.calendarEventDesc.text = event.GetDesc()
                calEvent.calendarEventDate.text = event.GetDate()
                self.add_widget(calEvent)
                self.count += 1

            self.height = self.count * CalendarEvent().height
        except IndexError:
            return


class CalendarEvent(StackLayout):
    def __init__(self, **kwargs):
        super(CalendarEvent, self).__init__(**kwargs)


class TimeDisplay(BoxLayout):
    def __init__(self, **kwargs):
        super(TimeDisplay, self).__init__(**kwargs)

        Clock.schedule_interval(self.Update, 1)  # update time every second

    def Update(self, *args):
        self.time.text = datetime.now().strftime("%H:%M")
        self.date.text = datetime.now().strftime("%A %dth %B %Y")


class WeatherDisplay(BoxLayout):
    location = StringProperty("")

    def __init__(self, **kwargs):
        super(WeatherDisplay, self).__init__(**kwargs)
        self.weather = WeatherApi()
        self.weather.AddObserver(self)
        self.height = 0

    def Update(self, *args):
        self.height = 200
        self.clear_widgets()
        self.weatherdays = self.weather.GetDays()
        weatherToday = WeatherToday()

        try:
            weatherToday.weatherTodayHigh.text = self.weatherdays[0].GetHigh()
            weatherToday.weatherTodayLow.text = self.weatherdays[0].GetLow()
            weatherToday.weatherTodayIcon.source = self.weatherdays[0].GetIcon()
            weatherToday.weatherTodayLocation.text = self.weather.location[:self.weather.location.index(",")]

            self.add_widget(weatherToday)

            weatherWeek = WeatherWeek()

            for i in range(1, 5):
                wDay = WeatherWeekDay()
                wDay.weatherTemp.text = self.weatherdays[i].GetTemp()
                wDay.weatherIcon.source = self.weatherdays[i].GetIcon()
                wDay.weatherDay.text = self.weatherdays[i].DayOfWeek()
                weatherWeek.add_widget(wDay)

            self.add_widget(weatherWeek)
        except IndexError:
            return


class WeatherWeek(BoxLayout):
    def __init__(self, **kwargs):
        super(WeatherWeek, self).__init__(**kwargs)


class WeatherToday(BoxLayout):
    def __init__(self, **kwargs):
        super(WeatherToday, self).__init__(**kwargs)


class WeatherWeekDay(StackLayout):
    def __init__(self, **kwargs):
        super(WeatherWeekDay, self).__init__(**kwargs)


class TravelDisplay(StackLayout):
    def __init__(self, **kwargs):
        super(TravelDisplay, self).__init__(**kwargs)

        self.loc = LocationApi()
        self.loc.AddObserver(self)

    def Update(self, *args):
        self.clear_widgets()
        self.locations = self.loc.locations
        self.height = len(self.locations) * TravelPoint().height

        for location in self.locations:
            travel = TravelPoint()
            travel.location.text = location.name
            travel.time.text = location.GetTime()
            if location.traffic != "0":
                travel.traffic.text = location.GetTraffic()
            travel.icon.source = location.source

            self.add_widget(travel)


class TravelPoint(StackLayout):
    def __init__(self, **kwargs):
        super(TravelPoint, self).__init__(**kwargs)


class SpotifyDisplay(BoxLayout):
    angleEnd = NumericProperty()

    def __init__(self, **kwargs):
        super(SpotifyDisplay, self).__init__(**kwargs)
        self.spotify = SpotifyApi()
        self.spotify.AddObserver(self)

    def Update(self, *args):
        track = self.spotify.currentTrack
        if track:
            self.angleEnd = track.endAngle
            self.trackName.text = track.name
            self.trackArtist.text = track.artist


class ApiScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(ApiScreen, self).__init__(**kwargs)

        self.add_widget(TimeDisplay())
        self.add_widget(LeftSideDisplay())


class MainApp(App):
    def build(self):
        return ApiScreen()


if __name__ == "__main__":
    MainApp().run()
