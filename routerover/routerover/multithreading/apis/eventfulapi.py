import eventful

def get_events(lat, lon, radius=5):
	coordinates = str(lat)+','+str(lon)
	api = eventful.API('L5TN3BsjGj9xFbtb')
	events = api.call('/events/search', 
		location=(coordinates), 
		within=radius)
	return json_parse(events)
	

def json_parse(response):
	result = []
	if response.get("events"):
		if response["events"].get("event"):
			events = response["events"]["event"]
			for event in events:
				eventDic = {}
				eventDic["name"] = event["title"]
				eventDic["latitude"] = event["latitude"]
				eventDic["longitude"] = event["longitude"]
				result.append(eventDic)
	return result

