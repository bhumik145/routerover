import cookielib
import socket
import urllib
import urllib2

url = 'http://10.254.187.198:8000/mapper/'
http_header = {
                "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.46 Safari/535.11",
                "Accept" : "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,text/png,*/*;q=0.5",
                "Accept-Language" : "en-us,en;q=0.5",
                "Accept-Charset" : "ISO-8859-1",
                "Content-type": "application/x-www-form-urlencoded",
                "Host" : "http://10.254.187.198:8000/",
                "Referer" : "http://10.254.187.198:8000/mapper//"
                }

params = {
  'source': {
    'lat' : 100,
    'long' : 200
  },
  'city_from' : [169, 190, 34],
  'radius_from' : 0,
  'city_to' : 263,
  'radius_to' : 0,
  'date' : 'date',
  'day' : 5,
  'month' : 03,
  'year' : 2012,
  'tolerance' : 0
}

#data = '{"glossary":{"title": "example glossary","GlossDiv":{"title": "S","GlossList":{"GlossEntry":{"ID": "SGML","SortAs": "SGML","GlossTerm": "Standard Generalized Markup Language","Acronym": "SGML","GlossDef":{"para": "A meta-markup language, used to create markup languages such as DocBook.","GlossSeeAlso": ["GML", "XML"]},"GlossSee": "markup"}}}}}'
data = {'id': 2, 'name': 'hussain'}
 # setup socket connection timeout
timeout = 15
socket.setdefaulttimeout(timeout)

# setup cookie handler
cookie_jar = cookielib.LWPCookieJar()
cookie = urllib2.HTTPCookieProcessor(cookie_jar)

# setup proxy handler, in case some-day you need to use a proxy server
proxy = {} # example: {"http" : "www.blah.com:8080"}

# create an urllib2 opener()
#opener = urllib2.build_opener(proxy, cookie) # with proxy
opener = urllib2.build_opener(cookie) # we are not going to use proxy now

# create your HTTP request
#req = urllib2.Request(url, urllib.urlencode(params), http_header)
req = urllib2.Request(url, data, http_header)
# submit your request
res = opener.open(req)
html = res.read()

# save retrieved HTML to file
open("tmp.html", "w").write(html)
print html
