import json


class API:

    def __init__(self):
        self.observerList = []

    def OpenAPIData(self):
        try:
            with open('Security/ApiData.json', "r") as self.apiDataJson:
                data = json.load(self.apiDataJson)
                return data
        except IOError:
            print("No file found Security/ApiData.json")
            raise IOError

    def AddObserver(self, weather):
        self.observerList.append(weather)
        weather.Update()

    def NotifyObservers(self):
        for o in self.observerList:
            o.Update()

    def CheckDataForChanges(self, original, new):
        equal = True
        if len(original) > 0 and len(original) == len(new):
            for i in range(0, len(original)):
                if new[i] != original[i]:
                    equal = False
        else:
            equal = False
        return equal
