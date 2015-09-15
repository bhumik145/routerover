import requests
import json
from sets import Set
apiKey = 'AIzaSyAV0lyucR8lT6C_8uM_OpWFWX_mat-K_No'
urlMain = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'


#https://maps.googleapis.com/maps/api/place/nearbysearch/json?&location=37.2977695,-121.893945&radius=5000&keyword=gas+station&key=AIzaSyAV0lyucR8lT6C_8uM_OpWFWX_mat-K_No

#rankby=distance and radius cannot be used at the same time

def getNearByPlaces(lattitude, longitude, radius, searchString):
    url = appendURLParameter(urlMain , 'location' , str(lattitude) + ',' + str(longitude))
    url = appendURLParameter(url , 'radius' , str(radius))
    url = appendURLParameter(url, 'keyword' , searchString)
    url = appendURLParameter(url , 'key', apiKey)
    response = requests.get(url)
    jsonDict = json.loads(response.text)
    i = 0
    resultList = []
    if len(jsonDict['results']) == 0:
        return resultList

    for result in jsonDict['results']:
        #print jsonDict['results'][i]['name'], jsonDict['results'][i]['geometry']['location']['lat'], jsonDict['results'][i]['geometry']['location']['lng']
        resultTuple = {"latitude":str(jsonDict['results'][i]['geometry']['location']['lat']),
            "longitude":str(jsonDict['results'][i]['geometry']['location']['lng']),
            "name":str(jsonDict['results'][i]['name'])}
        resultList.append(resultTuple)
        i = i + 1
    return resultList
def appendURLParameter(url, paramName, paramValue):
    return url + '&' + str(paramName) + '=' + str(paramValue)


latitude = '-33.8670522'
longitude = '151.1957362'
getNearByPlaces(latitude, longitude, 500, 'cruise')
