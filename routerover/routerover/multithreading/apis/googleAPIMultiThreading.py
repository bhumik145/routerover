import requests
import json
import threading
from myLogger import roverLogOnBothConsoleAndFile


apiKey = 'AIzaSyAV0lyucR8lT6C_8uM_OpWFWX_mat-K_No'
urlMain = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
googleLock = threading.Lock()

#https://maps.googleapis.com/maps/api/place/nearbysearch/json?&location=37.2977695,-121.893945&radius=5000&keyword=gas+station&key=AIzaSyAV0lyucR8lT6C_8uM_OpWFWX_mat-K_No


def getGooglePlaces(lattitude, longitude, radius, searchString, googlePlaces, googleThreadCount):
    roverLogOnBothConsoleAndFile.info("Google thread " + str(googleThreadCount) + " started execution")
    payload = getURLPayloadForGoogleAPICall(lattitude, longitude, radius, searchString)
    response = requests.get(urlMain, params=payload)
    parseGoogleResponseJSONAndUpdateGooglePlaces(response.text, googlePlaces)
    roverLogOnBothConsoleAndFile.info("Google thread " + str(googleThreadCount) + " finished execution")

def parseGoogleResponseJSONAndUpdateGooglePlaces(responseText, googlePlaces):
    jsonDict = json.loads(responseText)
    resultList = []
    if len(jsonDict['results']) > 0:
        for result in jsonDict['results']:
            resultTuple = (str(result['geometry']['location']['lat']),
                str(result['geometry']['location']['lng']),
                str(result['name']))
            resultList.append(resultTuple)
        googleLock.acquire()
        try:
            googlePlaces += resultList
        finally:
            googleLock.release()

def getURLPayloadForGoogleAPICall(lattitude, longitude, radius, searchString):
    payload = {}
    payload['location'] = str(lattitude) + ',' + str(longitude)
    payload['radius'] =  str(radius)
    payload['keyword'] = str(searchString)
    payload['key'] = apiKey
    return payload
