from urllib2 import Request, urlopen, URLError
import json

def get_meetups(lat, lon, radius=5000):
	key = 'cf7a2c744205f2f7533d653c4e7a'
	url = 'https://api.meetup.com/2/open_events?'+'lat='+str(lat)+'&lon='+str(lon)+'&radius='+str(radius)+'&key='+key+''
	print url
	rqst = Request('https://api.meetup.com/2/open_events?'
		+'lat='+str(lat)
		+'&lon='+str(lon)  
		+'&radius='+str(radius)
		+'&key='+key+'')
	response = urlopen(rqst)
	string = response.read()
	json_obj = json.loads(string)
	return json_parse(json_obj)

def json_parse(obj):
	result = []
	meetups = obj["results"]
	cnt = 0
	for meetup in meetups:
		print meetup
		cnt+=1
		if cnt > 10:
			break
		dict = {}
		dict["name"] = meetup["name"]
		if meetup.get("venue"):
			dict["latitude"] = meetup["venue"]["lat"]
			dict["longitude"] = meetup["venue"]["lon"]
		elif meetup.get("group"):
			dict["latitude"] = meetup["group"]["group_lat"]
			dict["longitude"] = meetup["group"]["group_lon"]
		else:
			continue
		dict["timestamp"] = meetup["time"]
		result.append(dict)
	return result