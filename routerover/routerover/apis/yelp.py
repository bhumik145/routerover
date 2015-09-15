import rauth
import time
import json

CONSUMER_KEY = 'TY-IfNcSqwVY_mCQJWOqvg'
CONSUMER_SECRET = 'Bj7NVWXPyuazx_3foVQf1F79T3Y'
TOKEN_KEY = 'A4__i2Vn_PXNHItjHPiBqv0itYtIR8nO'
TOKEN_SECRET = 'muk8chRFxAYh00wE355pqsP9HF8'  


def get_results(params):

  #Obtain these from Yelp's manage access page
  consumer_key = CONSUMER_KEY
  consumer_secret = CONSUMER_SECRET
  token = TOKEN_KEY
  token_secret = TOKEN_SECRET
  
  session = rauth.OAuth1Session(
    consumer_key = consumer_key
    ,consumer_secret = consumer_secret
    ,access_token = token
    ,access_token_secret = token_secret)
    
  request = session.get("http://api.yelp.com/v2/search",params=params)
  
  #Transforms the JSON API response into a Python dictionary
  data = request.json()
  session.close()
  
  return parse_json(data)
    
def get_search_parameters(lat,long,term,radius=5000):
  #See the Yelp API for more details
  params = {}
  params["term"] = term
  params["ll"] = "{},{}".format(str(lat),str(long))
  params["radius_filter"] = radius
  params["limit"] = "10"

  return params

def parse_json(content):
  result = []
  if content.get("businesses"):
    businesses = content["businesses"]
    for business in businesses:
      bus_struct = {}
      bus_struct['name'] = str(business["name"])
      bus_struct['rating'] = str(business["rating"])
      bus_struct['latitude'] = str(business["location"]["coordinate"]["latitude"])
      bus_struct['longitude'] = str(business["location"]["coordinate"]["longitude"])
      result.append(bus_struct)
  return result 

