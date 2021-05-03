import threading
import spotipy
import spotipy.util as util
from Models.ModelAPI import API


class SpotifyApi(API):
    def __init__(self):
        super(SpotifyApi, self).__init__()

        self.data = self.OpenAPIData()

        self.data = self.data["spotify"]
        try:
            self.client_id = self.data["client_id"]
            self.client_sec = self.data["client_secret"]
            scope = "user-read-currently-playing"
            self.username = self.data["username"]
            self.redirectURI = self.data["redirect_uri"]
        except KeyError as keyException:
            print("KeyError - Spotify API: Variables not defined in the api data json")
            raise keyException

        self.token = util.prompt_for_user_token(self.username, scope, client_id=self.client_id,
                                                client_secret=self.client_sec,
                                                redirect_uri=self.redirectURI)
        self.currentTrack = False
        self.GetCurrentTrack()

    def GetCurrentTrack(self):
        sp = spotipy.client.Spotify(auth=self.token)
        result = sp.current_user_playing_track()
        if result:
            self.currentTrack = self.Track(result)
            if self.currentTrack.isPlaying:
                self.NotifyObservers()

        threading.Timer(1, self.GetCurrentTrack).start()

    class Track:
        def __init__(self, track):
            self.name = track["item"]["name"]
            self.artist = track["item"]["artists"][0]["name"]
            self.img = track["item"]["album"]["images"][0]["url"]
            self.endAngle = (track["progress_ms"] / track["item"]["duration_ms"]) * 360
            self.isPlaying = track["is_playing"]
