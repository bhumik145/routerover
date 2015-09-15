import rauth
import time
import json
import threading
from myLogger import roverLogOnBothConsoleAndFile

CONSUMER_KEY = 'TY-IfNcSqwVY_mCQJWOqvg'
CONSUMER_SECRET = 'Bj7NVWXPyuazx_3foVQf1F79T3Y'
TOKEN_KEY = 'A4__i2Vn_PXNHItjHPiBqv0itYtIR8nO'
TOKEN_SECRET = 'muk8chRFxAYh00wE355pqsP9HF8'

yelpLock = threading.Lock()

def getYelpPlaces(lattitude, longitude, searchString, radius, yelpPlaces, yelpThreadCount):
    roverLogOnBothConsoleAndFile.info("Yelp thread: " + str(yelpThreadCount) + " stated execution")
    payload = getURLPayloadForYelpAPICall(lattitude, longitude, searchString, radius)
    consumer_key = CONSUMER_KEY
    consumer_secret = CONSUMER_SECRET
    token = TOKEN_KEY
    token_secret = TOKEN_SECRET
    session = rauth.OAuth1Session(
      consumer_key = consumer_key
      ,consumer_secret = consumer_secret
      ,access_token = token
      ,access_token_secret = token_secret)
    request = session.get("http://api.yelp.com/v2/search",params=payload)
    #Transforms the JSON API response into a Python dictionary
    data = request.json()
    session.close()
    parseYelpResponseJSONAndUpdateYelpPlaces(data, yelpPlaces)
    roverLogOnBothConsoleAndFile.info("Yelp thread: " + str(yelpThreadCount) + " finished execution")


def getURLPayloadForYelpAPICall(lat, long, term, radius):
  #See the Yelp API for more details
  params = {}
  params["term"] = term
  params["ll"] = "{},{}".format(str(lat),str(long))
  params["radius_filter"] = radius
  params["limit"] = "10"
  return params

def parseYelpResponseJSONAndUpdateYelpPlaces(content, yelpPlaces):
    resultList = []
    if content.get("businesses"):
        businesses = content["businesses"]
        for business in businesses:
            resultTuple = (str(business["location"]["coordinate"]["latitude"]),
                           str(business["location"]["coordinate"]["longitude"]),
                           str(business["name"]), str(business["rating"]))
            resultList.append(resultTuple)
        yelpLock.acquire()
        try:
            yelpPlaces += resultList
        finally:
            yelpLock.release()
