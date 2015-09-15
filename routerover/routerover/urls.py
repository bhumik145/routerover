from django.conf.urls import patterns, include, url
from . import mapperService
from . import multithreading
import sys
sys.path.append("/Users/bthakkar/projects/routerove/routerover/routerover/multithreading")

from multithreading import mapperServiceMultiThreading

urlpatterns = patterns('',
    #url(r'^Data/Orders/$', Orders.as_view(), name='Orders'),
    url(r'^demo/$', mapperService.demo, name = 'demo'),
    #url(r'^mapper/$', mapperService.mapper, name = 'mapper'),
    url(r'^mapper/$', mapperServiceMultiThreading.mapper, name = 'mapper'),
)
