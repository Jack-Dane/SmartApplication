import os
import pickle
from Models.ModelAPI import API
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
import threading
import dateutil.parser


class GoogleCalendarApi(API):
    def __init__(self):
        super(GoogleCalendarApi, self).__init__()

        self.SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        creds = None
        self.events = []

        if os.path.exists("Security/token.pickle"):
            with open("Security/token.pickle", "rb") as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "Security/credentials.json", self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open("Security/token.pickle", "wb") as token:
                pickle.dump(creds, token)

        self.service = build("calendar", "v3", credentials=creds)
        self.setEvents(3)

    def setEvents(self, n):
        now = datetime.datetime.utcnow().isoformat() + "Z"
        events_result = self.service.events().list(calendarId="primary", timeMin=now,
                                                   maxResults=n, singleEvents=True,
                                                   orderBy="startTime").execute()
        events = events_result.get("items", [])

        equal = self.CheckDataForChanges(self.events, events)

        if not equal:
            self.events = []
            for event in events:
                self.events.append(self.Event(event))
            self.NotifyObservers()

        threading.Timer(5, self.setEvents, [3]).start()

    def returnEvents(self):
        return self.events

    class Event:
        def __init__(self, event):
            self.start = dateutil.parser.parse(event["start"]["dateTime"])
            self.end = dateutil.parser.parse(event["end"]["dateTime"])
            self.title = event["summary"]
            self.date = dateutil.parser.parse(event["start"]["dateTime"])

        def GetDesc(self):
            start = datetime.datetime.strftime(self.start, "%H:%M")
            end = datetime.datetime.strftime(self.end, "%H:%M")
            return str(self.title) + " " + str(start) + "-" + str(end)

        def GetDate(self):
            month = datetime.datetime.strftime(self.date, "%b")
            day = datetime.datetime.strftime(self.date, "%d")
            return day + "\n" + month

        def __eq__(self, other):
            if isinstance(other, self.__class__):
                return self.start == other.start and self.end == other.end and self.title == other.title and self.date == other.date
            return False
