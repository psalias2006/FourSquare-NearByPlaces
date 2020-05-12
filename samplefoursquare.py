import FourPlacesLib.fourPlaces as fourNear
import os

inputDir    = 'my_input'
outputDir   = 'my_output'
#filename    = 'corfu_geo.json'
baseUrl     = 'https://api.foursquare.com/v2/venues/search'
clientID    = 'XXXXXXXXXXXXXXXXXXXXXX'
clientSecret= 'YYYYYYYYYYYYYYYYYYYYYY'
rad         = '500'

def getEveything(myFile):
    print (myFile)
    fourPlaces = fourNear.NearbyModel('myfirst', inputDir, outputDir, myFile, baseUrl, clientID, clientSecret, rad)
    fourPlaces.runEverything()
    return

def searchEverything(inDir, outDir):
    localPath   = os.getcwd()
    inputDir  = localPath + '/' + inDir + '/'
    outputDir = localPath + '/' + outDir + '/'
    files = os.listdir(inputDir)

    for f in files:
        getEveything(f)

    return

if __name__ == "__main__":
    searchEverything(inputDir, outputDir)

