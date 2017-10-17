#!/usr/bin/python
import sys
import csv
import googlemaps
import datetime
import pickle

gmaps = googlemaps.Client(key='AIzaSyBtgQ_VO_AiRkBbAaUBbklMRXlpL0kclKs')

def getDistance(fromGPS, toGPS):
    if fromGPS == toGPS:
        return None

    route = gmaps.distance_matrix(
        {"lat": stations[x]["latitude"], "lng": stations[x]["longitude"]},
        {"lat": stations[y]["latitude"], "lng": stations[y]["longitude"]},
        language="cs-CZ", mode="driving")

    return {
        "timestamp": datetime.datetime.now().strftime("%Y%m%d%H%m%S"),
        "duration": route["rows"][0]["elements"][0]["duration"]["value"],
        "distance": route["rows"][0]["elements"][0]["distance"]["value"]
    }

def main(argv):
    stations = {}
    with open("CNG.csv") as csvfile:
        i = 0
        reader = csv.DictReader(csvfile)
        for row in reader:
            i += 1
            stations[i] = {
                "longitude": row["Longitude"],
                "latitude": row["Latitude"],
                "note": row["Name"],
            }


        inputFile = open("distmatrix.pkl", "rb")
        stationsFromFile = pickle.load(inputFile)
        DistMatrixFromFile = pickle.load(inputFile)
        inputFile.close()


        if len(stations) <> len(stationsFromFile):
            print "Different number of stations (in CSV", len(stations),", in data", len(stationsFromFile),")! Need to combine."

            for x in stations:
                found = False
                print x
                for y in stationsFromFile:
                    if stations[x]["latitude"] == stationsFromFile[y]["latitude"] and stations[x]["longitude"] == stationsFromFile[y]["longitude"]:
                        print "Match, breaking yhe cycle..."
                        found = True
                        break

                if found is False:
                    index = len(stationsFromFile) + 1
                    stationsFromFile[index] = {"latitude": stations[x]["latitude"], "longitude": stations[x]["longitude"], "note": stations[x]["note"]}

                    DistMatrixFromFile.append([{"distance": 0, "duration": 0,"timestamp": None}] * index)

                    for n in range(index):
                        for g in range(len(DistMatrixFromFile[n]), index):
                            DistMatrixFromFile[n].append([{"distance": 0, "duration": 0,"timestamp": None}])

        #print len(stationsFromFile)
        print "xxxxx"
        for x in DistMatrixFromFile:
            print len(x)
        quit()

        DistMatrix = [[{"distance": 0} for x in range(i)] for y in range(i)]

        for x in range(i):
            if x == 0:
                continue
            for y in range(i):
                if y == 0:
                    continue
                if x == y:
                    continue


        print DistMatrix

        output = open("distmatrix.pkl", "wb")
        pickle.dump(stations, output)
        pickle.dump(DistMatrix, output)
        output.close()
    return None

if __name__ == "__main__":
    main(sys.argv[1:])
