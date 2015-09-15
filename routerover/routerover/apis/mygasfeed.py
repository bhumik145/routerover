from rest_framework.response import Response
from django.http.response import HttpResponse
from urllib2 import Request, urlopen, URLError
import json

def get_gas(lat, lon, radius=5):
    key = 'zglauv3q06'
    rqst = Request('http://api.mygasfeed.com/stations/radius/'
    		+str(lat)+'/'
    		+str(lon)+'/'
    		+str(radius)+'/'
    		+'reg'+'/'
    		+'Distance'+'/'
    		+key+'.json')
        
    response = urlopen(rqst)
    string = response.read()
    json_obj = json.loads(string)
    return json_parse(json_obj)

def json_parse(obj):
	result = []
	cnt = 0
	stations = obj["stations"]
	for station in stations:
		cnt += 1
		if cnt > 10:
			break
		dict = {}
		dict['name'] = station["station"]
		dict['latitude'] = station['lat']
		dict['longitude'] = station['lng']
		dict['reg_price'] = station['reg_price']
		result.append(dict)
	return result


