import sys
class Stops:
    def __init__(self, d):
        self.stops = []
        self.d = d
        self.__load(d)
    def __load(self, d):
        from os import getcwd, listdir
        files = [x for x in listdir(d) if x.endswith(".txt")]
        for f in files:
            ff = open(d+f, "r")
            ff = ff.readlines()
            data = [d.split("\n")[0] for d in ff]
            self.stops += data
        


if __name__ == "__main__":
    stops = Stops()
    print(stops.stops)