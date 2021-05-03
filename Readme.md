# Smart Mirror
This Python Application will supply data from application to be displayed 
in an aesthetic manner on a screen. It would work very well behind a mirror
as it is a dark background with light text. 

## APIs used
1. TomTom - Used to predict how long a route will take to walk or drive
2. Spotify - Used to display the current song playing and the duration
3. Open Weather - Used to show the weather of the upcoming and current day
4. Google Calendar - Used to show the 3 most upcoming events in your calendar

## How to setup
To setup the application you need to do a couple of things to get the APIs working.

### Adding the security folders
You will need to add a the file "ApiData.json" to the security folder. This is where 
the api keys and extra data is stored. 

```
{
	"spotify": {
		"client_id": "x",
		"client_secret": "x",
		"username": "x",
		"redirect_uri": "http://localhost:8080/callback/"
	},

	"weather": {
		"location": "x",
		"api_key": "x"
	},

	"directions": {
		"api_key": "x",

		"home": {
			"lon": "x",
			"lat": "x"
		},
		
		"locations": [
			{
				"name": "x",
				"lon": "x",
				"lat": "x",
				"transport": "x"
			},
			
			{
				"name": "x",
				"lon": "x",
				"lat": "x",
				"transport": "x"
			}
		]
	}
}
```

1. Spotify
    1. client_id - The client_id setup for the API 
    1. client_secret - The client_secret setup for the API
    1. username - The username of your Spotify account
    1. redirect_uri - The redirect URI of the Spotify API, it is advised to use localhost:8080 for auto authentication
2. Weather
    2. location - Your current location based on City, find your city here: http://bulk.openweathermap.org/sample/
    2. api_key - The API key which can be setup here: https://openweathermap.org/api - a free one will do
3. Directions
    3. api_key - The api key of your TomTom api: https://developer.tomtom.com/
    3. home - The location of your home using longitudinal and latitudinal coordinates
    4. locations - An array of locations with: longitudinal and latitudinal coordinates, name and transportation you will 
    take to get there: car or pedestrian. 
 
### Google Calendar
To enable Google Calendar you will need to setup the api connection up in your Google API dashboard for Google Calendar. 
From here you need to download the credentials.json and place in the Security directory. 

When you run the application for the first time, it should redirect you to single sign on, you just need to allow the 
apps connection to Google Calendar. 

## Notes
If you only want certain APIs connected, leave the credentials out of the ApiData.json file, error handling of the 
application will deal with this and not show any connected APIs which don't have the correct data in the JSON file. 

## MIT License
MIT License

Copyright (c) 2021 Jack Dane

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
