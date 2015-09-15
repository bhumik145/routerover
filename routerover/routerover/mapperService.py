from django.http import JsonResponse
import json
from apis import yelp, mygasfeed,eventfulapi, meetup
from sets import Set
from apis import googleAPI
from tempthread import runMainThread, getResultDict


def demo(request):
    print request
    return JsonResponse({'foo':'bar'})

#the maximum allowed radius 50000 meters
#join keywords by plus sign whenever there is a space

def mapper(request):

    jsonBlob = json.loads(request.body)
    #retrieve all the parameters from request body
    points = parsePoints(jsonBlob['points'])

    source = (float(jsonBlob['source']['latitude']) , float(jsonBlob['source']['longitude']))
    destination = (float(jsonBlob['destination']['latitude']) , float(jsonBlob['destination']['longitude']))

    points.append(source)
    points.append(destination)

    searchStringSeperatedByPlus = generatePlusSignSeperatedSearchString(jsonBlob['searchkeys'])
    searchRadius = float(jsonBlob['radius'])
    #Reduce the number of points before sending
    #Add source and destination in the points list before-hand
    placesToShowOnRoute = getPlacesToShowOnRoute(points, searchStringSeperatedByPlus, searchRadius,
        jsonBlob['apis']['yelp']=="true",
        jsonBlob['apis']['gas']=="true",
        jsonBlob['apis']['eventful']=="true",
        jsonBlob['apis']['meetup']=="true",
        jsonBlob['apis']['google']=="true")
#    resultArray = []
#    for place in placesToShowOnRoute:
#        resultArray.append(place)
    response = JsonResponse(placesToShowOnRoute, safe=False)
    response['Access-Control-Allow-Origin'] = '*'
    return response

def generatePlusSignSeperatedSearchString(stringWithWhitespaces):
    searchStringSeperatedByPlus = ''
    stringArray = stringWithWhitespaces.split()
    for string in stringArray:
        if len(searchStringSeperatedByPlus) == 0:
            searchStringSeperatedByPlus = string
        else:
            searchStringSeperatedByPlus = searchStringSeperatedByPlus + '+' + string
    return searchStringSeperatedByPlus

def parsePoints(pointsArrayInStringFormat):
    points = []
    i = 0
    for point in pointsArrayInStringFormat:
        latLongTuple = (float(pointsArrayInStringFormat[i]['latitude']) , float(pointsArrayInStringFormat[i]['longitude']))
        points.append(latLongTuple)
        i = i + 1
    return points

def getPlacesToShowOnRoute(points, searchStringSeperatedByPlus, searchRadius, yelpFlag, gasFlag, eventfulFlag, meetupFlag, googleFlag):
    #runMainThread(points, radius, term, yelpFlag, gasFlag, eventfulFlag, meetupFlag, googleFlag)
    runMainThread(points, searchRadius, searchStringSeperatedByPlus, yelpFlag, gasFlag, eventfulFlag, meetupFlag, googleFlag)
    return getResultDict()
