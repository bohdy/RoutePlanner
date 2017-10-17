#!/usr/bin/python
import sys
import csv
import googlemaps
import datetime
import pickle

def main(argv):
    stations = {}
    """
    stations[0] = {
        "longitude": 14.455251,
        "latitude": 50.119387,
        "note": "START"
    }
    """
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
            if i > 5:
                break

        print "Total stations: ", i

        DistMatrix = [[{"distance": 0} for x in range(i)] for y in range(i)]
        for x in range(i):
            DistMatrix[x][x] = None
        """
        stations[len(stations)] = {
            "longitude": 18.265545,
            "latitude": 49.826365,
            "note": "KONEC",
        }
        """

        gmaps = googlemaps.Client(key='AIzaSyBtgQ_VO_AiRkBbAaUBbklMRXlpL0kclKs')
        """
        places = []
        for x in range(i):

            if x < 15:
                places.append({"lat": stations[x+1]["latitude"], "lng": stations[x+1]["longitude"]})

        matrixG = gmaps.distance_matrix(places, places, language="cs-CZ", mode="driving")
        print matrixG
        """

        for x in range(i):
            if x == 0:
                continue
            for y in range(i):
                if y == 0:
                    continue
                if x == y:
                    continue

                print "Duration for", x, " to", y
                if DistMatrix[x][y]["distance"] == 0:
                    route = gmaps.distance_matrix(
                        {"lat": stations[x]["latitude"], "lng": stations[x]["longitude"]},
                        {"lat": stations[y]["latitude"], "lng": stations[y]["longitude"]},
                        language="cs-CZ", mode="driving")
                    DistMatrix[x][y]["duration"] = route["rows"][0]["elements"][0]["duration"]["value"]
                    DistMatrix[x][y]["distance"] = route["rows"][0]["elements"][0]["distance"]["value"]
                    DistMatrix[x][y]["timestamp"] = datetime.datetime.now().strftime("%Y%m%d%H%m%S")
                print "From ", x, " to ", y, " is distance ", DistMatrix[x][y]

        print DistMatrix

        output = open("distmatrix.pkl", "wb")
        pickle.dump(stations, output)
        pickle.dump(DistMatrix, output)
        output.close()
    return None

if __name__ == "__main__":
    main(sys.argv[1:])
