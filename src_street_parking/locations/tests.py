from django.test import TestCase
from locations.models import Location
from django.utils import unittest
#import re
#import json
#import requests
#import urllib2
#import urllib
import views
from views import *
#from nyc_geoclient import Geoclient
from django.http import HttpResponse, HttpRequest
from tests import *


#globals
NO_PARKING = 'PARKING'
NO_STANDING = 'NO STANDING'
SODA_URL1 = 'http://data-cityofnewyork-us-bnnfmc1phemq.runscope.net/resource/9yzr-h7jq.json?boroughcode='
SODA_URL2 = 'http://data.cityofnewyork.us/resource/zibd-yb3i.json?statusordernumber='
GEOCODE_BASE_URL = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='
SENSOR = '&sensor=true'
GEOCODE_END_URL = '&location_type=ROOFTOP&result_type=street_address&key=AIzaSyCn07k1NLeUoMH1xFXDfB_H1S8IeA0oji4'

latitude = '40.714224'
longitude = '-73.961452'
LOCATION_TYPE = 'ROOFTOP'
SENSOR = '&sensor=true'
'''
response = {}
data = {}
url_gmapapi2 = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452&sensor=true&location_type=ROOFTOP&result_type=street_address&key=AIzaSyCn07k1NLeUoMH1xFXDfB_H1S8IeA0oji4'
url_gmapapi3  ='https://maps.googleapis.com/maps/api/geocode/json?latlng=40.714353,-74.005973&sensor=true&location_type=ROOFTOP&result_type=street_address&key=AIzaSyCn07k1NLeUoMH1xFXDfB_H1S8IeA0oji4'
url_gmapapi   ='https://maps.googleapis.com/maps/api/geocode/json?latlng=40.714515,-74.006200&sensor=true&location_type=ROOFTOP&result_type=street_address&key=AIzaSyCn07k1NLeUoMH1xFXDfB_H1S8IeA0oji4'
url_gmapapi1 = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=40.71428,-74.00601&sensor=true&location_type=ROOFTOP&result_type=street_address&key=AIzaSyCn07k1NLeUoMH1xFXDfB_H1S8IeA0oji4'
url_invalid = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224'
'''

class TestLocation(TestCase):
    
    
    def test_reverse_geocode(self):
        #send geocode url
        global data
        url_revgeocod = GEOCODE_BASE_URL + latitude+','+longitude+SENSOR+GEOCODE_END_URL
        data = reverse_geocode(url_revgeocod)
        res_list = data['results']
        self.assertTrue(len(data) > 0)
        self.assertTrue(len(res_list) > 0)
                
    def test_geocode_data(self):
        #parse geocode result
        url_revgeocod = GEOCODE_BASE_URL + latitude+','+longitude+SENSOR+GEOCODE_END_URL
        data = reverse_geocode(url_revgeocod)
        resp_dict = parsegocode(data)
        streetName = resp_dict.get('mainstreet').upper()
        streetNumber = resp_dict.get('street_number').upper()
        boroughName = resp_dict.get('borough').upper()
        print streetName
        print streetNumber
        print boroughName
        self.assertTrue(len(resp_dict) > 0)
        self.assertEqual('BEDFORD AVENUE', streetName)
        self.assertEqual('277', streetNumber)
        self.assertEqual('BROOKLYN', boroughName)
        
    def test_geoclient(self):
        #test geoclient - retrieve block data
        streetName = 'BEDFORD AVENUE'
        streetNumber = '277'
        boroughName = 'BROOKLYN'
        block_response = geoclient_intersection(streetNumber, streetName, boroughName)
        print block_response
        self.assertTrue(len(block_response) > 0)
        #'sideOfStreet': u'BEDFORD AVENUE', 
        #'borough': u'BROOKLYN', 'toStreet': u'GRAND STREET', 'fromStreet': u'SOUTH    1 STREET'
	main_street = block_response.get('sideOfStreet').upper()
        from_street = block_response.get('fromStreet').upper()
        to_street   = block_response.get('toStreet').upper()  
        self.assertEqual('SOUTH    1 STREET', from_street)
        self.assertEqual('GRAND STREET', to_street)
        self.assertEqual('BEDFORD AVENUE', main_street)    
        
    def test_soda_url(self):
        #construct soda url1 for SODA call 1 
        streetName = 'BEDFORD AVENUE'
        streetNumber = '277'
        boroughName = 'BROOKLYN'
        block_response = geoclient_intersection(streetNumber, streetName, boroughName)
        url_0 = build_url_0(block_response)
        print url_0
        test_url = 'http://data-cityofnewyork-us-bnnfmc1phemq.runscope.net/resource/9yzr-h7jq.json?boroughcode=K&fromstreet=SOUTH    1 STREET&tostreet=GRAND STREET&sideofstreet=BEDFORD AVENUE'
        self.assertEqual(test_url, url_0)
        
    def test_soda_call1(self):
        #Define signsid and directions for street block - SODA call 1 
        soda_url = 'http://data-cityofnewyork-us-bnnfmc1phemq.runscope.net/resource/9yzr-h7jq.json?boroughcode=K&fromstreet=SOUTH    1 STREET&tostreet=GRAND STREET&sideofstreet=BEDFORD AVENUE'
        data = send_request(soda_url)
        #print data
            
        self.assertTrue(len(data) > 0)    
         
    def test_get_directions(self):
        #Define signsid and directions for street block - SODA call 1 
        my_data = [{u'boroughcode': u'K', 
        u'sideofstreet': u'BEDFORD AVENUE', u'mainstreet': u'W', u'statusordernumber': u'S-083147', u'tostreet': u'GRAND STREET', u'fromstreet': u'SOUTH    1 STREET'},
        {u'boroughcode': u'K', u'sideofstreet': u'BEDFORD AVENUE',
        u'mainstreet': u'E', u'statusordernumber': u'S-083154', u'tostreet': u'GRAND STREET', u'fromstreet': u'SOUTH    1 STREET'}]
        direct_list = get_directions(my_data)
               
        self.assertTrue(len(direct_list) > 0)
        self.assertTrue('W' in direct_list)
        self.assertTrue('E' in direct_list)
     
    def test_get_signid(self):
        #Define signsid and directions for street block - SODA call 1 
        my_data = [{u'boroughcode': u'K', 
        u'sideofstreet': u'BEDFORD AVENUE', u'mainstreet': u'W', u'statusordernumber': u'S-083147', u'tostreet': u'GRAND STREET', u'fromstreet': u'SOUTH    1 STREET'},
        {u'boroughcode': u'K', u'sideofstreet': u'BEDFORD AVENUE',
        u'mainstreet': u'E', u'statusordernumber': u'S-083154', u'tostreet': u'GRAND STREET', u'fromstreet': u'SOUTH    1 STREET'}]
        signid_list, signid_direct_list = get_signsid(my_data)
        print signid_list
        print signid_direct_list
        self.assertTrue('S-083147' in signid_list)
        self.assertTrue('S-083154' in signid_list)
        self.assertTrue('S-083147:W' in signid_direct_list)
        self.assertTrue('S-083154:E' in signid_direct_list) 
         
    def test_soda2url(self):
        #Define signsid and directions for street block - SODA call 1 
        signid_list = [u'S-083147', u'S-083154']
        signid_direct_list = [u'S-083147:W', u'S-083154:E'] 
        sign_desc_list = []
        ''' get sign descriptions - SODA call 2 '''
        for i in range(len(signid_list)):
            url = SODA_URL2+signid_list[i]
            print 'URL:', url
            test_url1 = 'http://data.cityofnewyork.us/resource/zibd-yb3i.json?statusordernumber=S-083147'
            test_url2 = 'http://data.cityofnewyork.us/resource/zibd-yb3i.json?statusordernumber=S-083154'
            if i == 0:
                self.assertEqual(test_url1, url)
            if i == 1: 
                self.assertEqual(test_url2, url)
            
                
    def test_parse_signdescription(self):
        #parse SODA call2 - sign descriptions 
        signid_direct_list = [u'S-083147:W', u'S-083154:E'] 
        url1 = 'http://data.cityofnewyork.us/resource/zibd-yb3i.json?statusordernumber=S-083147'
        url2 = 'http://data.cityofnewyork.us/resource/zibd-yb3i.json?statusordernumber=S-083154'
        data = send_request(url1)
        #print 'DATA',data
        self.assertTrue(len(data) > 0)
        sign_desc_list = parse_sign_desc(data, signid_direct_list[0]) 
             
        data = send_request(url2)
        #print 'DATA',data
        self.assertTrue(len(data) > 0)
        sign_desc_list = parse_sign_desc(data, signid_direct_list[1]) 
        print 'SIGNS:', sign_desc_list
     
        signs_holder = [u'NO PARKING (SANITATION BROOM SYMBOL) 8-9:30AM MON & THURS <---->:S-083147:W',
                u'NO PARKING (SANITATION BROOM SYMBOL) 8-9:30AM TUES & FRI W/SINGLE ARROW:S-083154:E',
                u'NO PARKING (SANITATION BROOM SYMBOL) 8-9:30AM TUES & FRI<---->:S-083154:E']

        self.assertTrue('NO PARKING (SANITATION BROOM SYMBOL) 8-9:30AM MON & THURS <---->:S-083147:W' in sign_desc_list)
        self.assertTrue('NO PARKING (SANITATION BROOM SYMBOL) 8-9:30AM TUES & FRI W/SINGLE ARROW:S-083154:E' in sign_desc_list)
        self.assertTrue('NO PARKING (SANITATION BROOM SYMBOL) 8-9:30AM TUES & FRI<---->:S-083154:E' in sign_desc_list)
        self.assertEqual(signs_holder, sign_desc_list)
    
if __name__ == '__main__':
    unittest.main()