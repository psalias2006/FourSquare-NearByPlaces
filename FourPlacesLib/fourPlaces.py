import json, requests
import pandas as pd

class NearbyModel:

    def __init__(self, name, inputDir, outputDir, filename, baseUrl, clientID, clientSecret, radius):
        self.name           = name
        self.inputDir       = inputDir
        self.outputDir      = outputDir
        self.filename       = filename
        self.baseUrl        = baseUrl
        self.clientID       = clientID
        self.clientSecret   = clientSecret
        self.radius         = radius


    def parseGeoJson(self, geoJson):
        filepath = self.inputDir + '/' + geoJson

        with open(filepath) as f:
            data    = json.load(f)

        places  = data['features'][0]['geometry']['coordinates'][0]
        return places


    def getPlaces(self, clientID, clientSecret, baseUrl, lat, lon, rad):
        url   =   baseUrl

        param = dict(
                client_id       = clientID,
                client_secret   = clientSecret,
                ll              = lat + ',' + lon,
                radius          = rad,
                v               = '20180101',
                limit           = 1000)

        resp = requests.get(url=url, params=param)
        data = json.loads(resp.text)

        return data


    def getPandas(self, placeJson):
        rsp         = []
        venueList   = (placeJson['response']['venues'])

        for item in venueList:
            try:
                venueID        = item['id']
                venueCatShort  = item['categories'][0]['shortName']
                venueName      = item['name']
                venueLat       = item['location']['lat']
                venueLon       = item['location']['lng']

                rsp.append({'venueID'      : venueID,
                            'venueCatShort': venueCatShort,
                            'venueName'    : venueName,
                            'venueLat'     : venueLat,
                            'venueLon'     : venueLon})
            except: pass
        dfItem      = pd.DataFrame.from_records(rsp)

        return dfItem


    
    def requestNearBy(self, placesList):
        clientID        = self.clientID
        clientSecret    = self.clientSecret
        rad             = self.radius
        baseUrl         = self.baseUrl
        pandasList      = []

        for place in placesList:
            lon = str(place[0])
            lat = str(place[1])

            placeJson   = self.getPlaces(clientID, clientSecret, baseUrl, lat, lon, rad)
            placePandas = self.getPandas(placeJson)
            
            pandasList.append(placePandas)

        return pandasList


    def mergePandas(self, pandasList):
        bigPanda    = pd.concat(pandasList)
        uniquePanda = bigPanda.drop_duplicates()

        return uniquePanda

    
    def pandasToCsv(self, placesDf):
        filename    = self.filename
        outputDir   = self.outputDir
        final       = outputDir + '/' + filename.split('.')[0] + '.csv'

        df_places = placesDf[['venueID', 'venueCatShort', 'venueLat', 'venueLon', 'venueName']]
        df_places.to_csv(final, index=False)
        return


    def runEverything(self):
        placeLst    = self.parseGeoJson(self.filename)
        pandasLst   = self.requestNearBy(placeLst)
        pandasBig   = self.mergePandas(pandasLst)
        
        self.pandasToCsv(pandasBig)
        return


def main():
    print("goooo")
    return

if __name__ == '__main__':
    main()

