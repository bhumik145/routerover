import collections

ResultObject = collections.namedtuple('ResultObject', 'places threads threadCount')
googleResultObject = ResultObject(places = [], threads = [], threadCount = 0)

print googleResultObject

googleResultObject.places.append('abc')
print googleResultObject

googleResultObject.threadCount += 1

print googleResultObject
