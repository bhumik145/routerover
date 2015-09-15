#!/usr/bin/python

from django.http import JsonResponse
import json
from apis import yelp, mygasfeed,eventfulapi, meetup, googleAPIMultiThreading

from sets import Set
from threading import Thread
from myLogger import roverLogOnBothConsoleAndFile

def demo(request):
    print request
    return JsonResponse({'foo':'bar'})

#the maximum allowed radius 50000 meters

def mapper(request):

    jsonBlob = json.loads(request.body)
    #retrieve all the parameters from request body
    points = parsePoints(jsonBlob['points'])

    source = (float(jsonBlob['source']['latitude']) , float(jsonBlob['source']['longitude']))
    destination = (float(jsonBlob['destination']['latitude']) , float(jsonBlob['destination']['longitude']))
    searchStringSeperatedByPlus = generatePlusSignSeperatedSearchString(jsonBlob['searchkeys'])
    searchRadius = float(jsonBlob['radius'])
    apiSelection = getAPISelectionFromRequestJson(jsonBlob['apis'])
    numberOfPointsToUseForSearch = 100 # +2 for source and destination

    points.append(source)
    points.append(destination)

    points = pickXPoints(points, numberOfPointsToUseForSearch)
    placesToShowOnRoute = getPlacesToShowOnRoute(points, searchStringSeperatedByPlus,
                                                 searchRadius, apiSelection)

    response = JsonResponse(placesToShowOnRoute, safe=False)
    response['Access-Control-Allow-Origin'] = '*'

    return response

def getAPISelectionFromRequestJson(apiSectionOfRequest):
    apiSelection = {}
    apiSelection['google'] = str(apiSectionOfRequest['google'])
    apiSelection['yelp'] = str(apiSectionOfRequest['yelp'])
    apiSelection['gas'] = str(apiSectionOfRequest['gas'])
    apiSelection['meetup'] = str(apiSectionOfRequest['meetup'])
    apiSelection['eventful'] = str(apiSectionOfRequest['eventful'])
    return apiSelection

def pickXPoints(points, numberOfPointsToUseForSearch):
    if(len(points) > numberOfPointsToUseForSearch):
        totalNumberOfPoints = len(points)
        jump = totalNumberOfPoints / numberOfPointsToUseForSearch
        jump = int(jump)
        reducedNumberOfPointsList = []

        index = 0
        while index < totalNumberOfPoints:
            reducedNumberOfPointsList.append(points[index])
            index = index + jump
        return reducedNumberOfPointsList
    else:
        return points

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

def getPlacesToShowOnRoute(points, searchStringSeperatedByPlus, searchRadius, apiSelection):
    resultObjectsDict = generateEmptyResultObjectsDict(apiSelection)
    resultDict = {}

    for point in points:
        initiateAllThreads(resultObjectsDict, point, searchStringSeperatedByPlus,
                           searchRadius, apiSelection)
    joinAllThreads(resultObjectsDict)
    prepareFinalResultDict(resultObjectsDict)
    return prepareFinalResultDict(resultObjectsDict)

def generateEmptyResultObjectsDict(apiSelection):
    resultObjectsDict = {}
    for key, value in apiSelection.iteritems():
        if value == 'true':
            resultObjectsDict[key] = emptyResultDict()
    return resultObjectsDict

def emptyResultDict():
    emptyDict = {}
    emptyDict['threads'] = []
    emptyDict['places'] = []
    emptyDict['threadCount'] = 0
    return emptyDict

def initiateAllThreads(resultObjectsDict, point, searchStringSeperatedByPlus, searchRadius, apiSelection):
    if(apiSelection['google'] == 'true'):
        resultObjectsDict['google']['threadCount'] +=  1
        thread = Thread(target = googleAPIMultiThreading.getGooglePlaces,
                        args = (point[0], point[1], searchRadius,
                        searchStringSeperatedByPlus, resultObjectsDict['google']['places'],
                        resultObjectsDict['google']['threadCount']))
        resultObjectsDict['google']['threads'].append(thread)
        thread.start()
    if(apiSelection['yelp'] == 'true'):
        resultObjectsDict['yelp']['threadCount'] +=  1
        thread = Thread(target = yelp.getYelpPlaces, args = (point[0], point[1],
                        searchStringSeperatedByPlus, searchRadius, resultObjectsDict['yelp']['places'],
                        resultObjectsDict['yelp']['threadCount']))
        resultObjectsDict['yelp']['threads'].append(thread)
        thread.start()
    '''
    if(apiSelection['gas'] == 'true'):
        gasPlace = mygasfeed.get_gas(point[0], point[1], int(searchRadius)/1000) if searchRadius else mygasfeed.get_gas(point[0], point[1])
        gasPlaces += (gasPlace)
    if(apiSelection['eventful'] == 'true'):
        eventfulPlace = eventfulapi.get_events(point[0], point[1], searchRadius) if searchRadius else eventfulapi.get_events(point[0], point[1])
        eventfulPlaces += (eventfulPlace)
    '''
    if(apiSelection['meetup'] == 'true'):
        resultObjectsDict['meetup']['threadCount'] +=  1
        thread = Thread(target = meetup.getYelpPlaces, args = (point[0], point[1],
                        searchStringSeperatedByPlus, searchRadius, resultObjectsDict['yelp']['places'],
                        resultObjectsDict['yelp']['threadCount']))
        resultObjectsDict['yelp']['threads'].append(thread)
        thread.start()


        meetupPlace = meetup.get_meetups(point[0], point[1], searchRadius) if searchRadius else meetup.get_meetups(point[0], point[1])
        meetupPlaces += (meetupPlace)

def joinAllThreads(resultObjectsDict):
    for key in resultObjectsDict:
        currentThread = 0
        for thread in resultObjectsDict[key]['threads']:
            currentThread += 1
            thread.join()
            roverLogOnBothConsoleAndFile.info("Joined " + key + " thread: " + str(currentThread))

def prepareFinalResultDict(resultObjectsDict):
    resultDict = {}
    for key in resultObjectsDict:
        resultDict[key] = list(set(resultObjectsDict[key]['places']))
    return resultDict

'''
resultTuple = {"latitude":str(jsonDict['results'][i]['geometry']['location']['lat']),
    "longitude":str(jsonDict['results'][i]['geometry']['location']['lng']),
    "name":str(jsonDict['results'][i]['name'])}
'''
