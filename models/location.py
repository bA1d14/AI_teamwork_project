import socket
import os
import IP2Location
import json
import urllib.request
class Location():
    def __init__(self):

        resource = urllib.request.urlopen('https://api.ipregistry.co/?key=c9qw7jv0pu8kv9')
        payload = json.loads(resource.read().decode('utf-8'))
        self.latitude = payload['location']['latitude']
        self.longtitude = payload['location']['longitude']

    def get_current_location(self):

        return self.latitude,self.longtitude

    def set_location(self,lon,lat):
        self.longtitude=lon
        self.latitude=lat

location=Location()