#locations.views.py
from django.shortcuts import render, render_to_response, RequestContext, redirect, get_object_or_404 
from django.contrib import messages
from .forms import LocationForm, LocationInitForm
from django.contrib.auth.models import User
import re
import json
import requests
import urllib2
import urllib
from nyc_geoclient import Geoclient
from django.http import HttpResponse
import logging

'''globals'''

SODA_URL1 = 'http://data-cityofnewyork-us-bnnfmc1phemq.runscope.net/resource/9yzr-h7jq.json?boroughcode='
SODA_URL2 = 'http://data.cityofnewyork.us/resource/zibd-yb3i.json?statusordernumber='
GEOCODE_BASE_URL = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='
SENSOR = '&sensor=true'
GEOCODE_END_URL = '&location_type=ROOFTOP&result_type=street_address&key=AIzaSyCn07k1NLeUoMH1xFXDfB_H1S8IeA0oji4'
sign_desc_list = []
boroughcode = ''
main_street = ''
from_street = ''
to_street = ''

# Create your views here.
# Get an instance of a logger

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  


def whereiam(request):
    ''' 
    Retrieve Location form from whereiam page.
    Base on latitude and longitude:
    1. define address - Google Geocode API
    2. based on address define from street to street block - nyc_Geoclient API
    3. based on street block retreive parking signs - SODA2 API
    4. redirect to display_parking_sign page
    5. pass sign description and other fields as a data parameters and also save them as session variable
    '''
    form = LocationInitForm(request.POST or None)
        
    if form.is_valid():
      
        latitude = request.POST.get('latitude', '')
        longitude = request.POST.get('longitude', '') 
        if latitude is not '' and longitude is not '':
            '''Define address, street segments and parking signs'''
            user = request.user.username
            '''geocode url'''
            url_revgeocod = GEOCODE_BASE_URL + latitude+','+longitude+SENSOR+GEOCODE_END_URL
            georesponse = reverse_geocode(url_revgeocod)
            res_list = georesponse['results']
            #check idf data response is not empty
            if len(res_list) > 0:
                resp_dict = parsegocode(georesponse)
                '''get nearest intersection geoname api'''
                my_message = ''
                if 'mainstreet' in resp_dict:
                    streetName = resp_dict.get('mainstreet').upper()
                else:
                    my_message = 'We are sorry, but there are no information about parking signs in your area' 
                    messages.info(request, my_message)
  
                if 'street_number' in resp_dict:
                    streetNumber = resp_dict.get('street_number').upper()
                else:
                    my_message = 'We are sorry, but there are no information about parking signs in your area' 
                    messages.info(request, my_message)   
      
                if 'borough' in resp_dict:
                    boroughName = resp_dict.get('borough').upper()
                else:
                    my_message = 'We are sorry, but there are no information about parking signs in your area' 
                    messages.info(request, my_message) 
                
                curr_address = ' '
                if 'formatted_address' in resp_dict:     
                    curr_address = resp_dict.get('formatted_address')
                    logger.debug(curr_address)
                    
                '''
                nyc_geoclient api call - define street block intersection
                '''
                try:  
                    block_response = geoclient_intersection(streetNumber, streetName, boroughName)
                    global main_street
                    global from_street
                    global to_street
                    main_street = block_response.get('sideOfStreet').upper()
                    from_street = block_response.get('fromStreet').upper()
                    to_street = block_response.get('toStreet').upper()
                    ''' 
                    Define signsid and directions for street block - SODA call 1 
                    '''
                    url_0 = build_url_0(block_response)
                    data = send_request(url_0)
                    if len(data) > 0:
                        direct_list = get_directions(data)
                        signid_list, signid_direct_list = get_signsid(data)
                        global sign_desc_list
                        sign_desc_list = []
                        ''' get sign descriptions - SODA call 2 '''
                        for i in range(len(signid_list)):
                            url = SODA_URL2+signid_list[i]
                            data = send_request(url)
                            if len(data) > 0:
                                parse_sign_desc(data, signid_direct_list[i]) 
                        request.session['sign_desc_list'] =  sign_desc_list
                        request.session['latitude'] = latitude
                        request.session['longitude'] = longitude
                        request.session['boroughcode'] = boroughcode
                        request.session['main_street'] = main_street
                        request.session['from_street'] = from_street
                        request.session['to_street']   = to_street
                        request.session['curr_address'] = curr_address

                        form = LocationForm()
                        if len(sign_desc_list) > 0:    
                            return render_to_response('location_select_parking_sign.html', 
                                                     {'latitude':latitude, 'longitude':longitude, 'signdesc':sign_desc_list, 'form':form, 'disable': False, 'curr_address':curr_address }, 
                                                     context_instance=RequestContext(request))
                        else:  
                            my_message = 'We are sorry, but there are no information about parking signs in your area' 
                            messages.info(request, my_message)  
                            
                        my_message = 'We are sorry, but there are no information about parking signs in your area' 
                        messages.info(request, my_message)  
                        
                except ValueError: 
                    my_message = 'We are sorry, but there are no information about parking signs in your area' 
                    messages.info(request, my_message)
                except Exception as e: 
                    my_message = 'We are sorry, but there are no information about parking signs in your area' 
                    messages.info(request, my_message)
                    logger.error(e)
        logger.debug('latitude: '+latitude)
        logger.debug('longitude: '+longitude)
                    
    return render_to_response("location_latlng.html",
                              locals(),
                              context_instance=RequestContext(request))
  
def select_parking_sign(request):
    '''
    select parking sign, hours, save location 
    '''
    form = LocationForm(request.POST or None)
    latitude  = request.session.get('latitude', '')
    longitude = request.session.get('longitude', '') 
        
    if form.is_valid():
        ''' record location info into database'''
        save_it = form.save(commit=False)
        save_it.user = request.user.username
        save_it.latitude = request.session.get('latitude', '') 
        save_it.longitude = request.session.get('longitude', '') 
        save_it.boroughcode = request.session.get('boroughcode','')
        save_it.main_street = request.session.get('main_street', '')
        save_it.from_street = request.session.get('from_street', '')
        save_it.to_street = request.session.get('to_street', '')
        signdesc = request.POST.get('signdesc', '')
        sign_direction = signdesc[-1]
        save_it.direction = sign_direction
        sign_id = signdesc[-10:]
        sign_id = sign_id[:-2]
        save_it.signid = sign_id
        save_it.signdesc = signdesc[:-11]
        signdesc = signdesc[:-11]
        save_it.hours = request.POST.get('hours', '')
        hours = request.POST.get('hours', '')
        save_it.stsus = 'O'
        save_it.save()
        curr_address = request.session.get('curr_address','')       
        my_message = 'Location has been saved' 
        messages.info(request, my_message) 
       
        ''' add event to google calendar '''
        #email = request.user.email
        #create_google_event(signdesc, hours, email) - has to be implemented
        
    return render_to_response('location_select_parking_sign.html',
                              {'latitude':latitude, 'longitude':longitude, 'disable': True, 'curr_address': curr_address },
                              context_instance=RequestContext(request))   


#def create_google_event(signdesc, hours, email):
#    ''' create event in google calendar'''
    
    
def reverse_geocode(url_revgeocod):
    '''get request to google geocode api'''
    response = {}
    data = {}
    response = requests.get(url_revgeocod)
    status = response.status_code
    data = response.json()
    return data


def parsegocode(data):
    '''get address'''
    results_list = data['results']
    response_dict = {}
    address_components_list = results_list[0]['address_components']
      
    for s in address_components_list:
        if 'street_number' in (s['types']):
            response_dict.update({'street_number': s['long_name'] })
        if 'route' in (s['types']):
            response_dict.update({'mainstreet': s['long_name'] })
        if 'sublocality' in (s['types']):
            response_dict.update({'borough': s['long_name'] })
        if 'administrative_area_level_1' in (s['types']):
            response_dict.update({'city': s['long_name'] })
            response_dict.update({'state': s['short_name'] })
        if 'postal_code' in (s['types']):
            response_dict.update({'zipcode': s['long_name'] })

    result_status = data['status']
    formatted_address = results_list[0]['formatted_address']
    result_geo_lat = results_list[0]['geometry']['location']['lat']
    result_geo_lng = results_list[0]['geometry']['location']['lng']
    response_dict.update({'formatted_address': formatted_address })
    response_dict.update({'latitude': result_geo_lat })
    response_dict.update({'longitude': result_geo_lng})

    return response_dict


def geoclient_intersection(streetNumber, streetName, boroughName):
    ''' retrieve intersection street1 and street2 with main street''' 
    g = Geoclient('799db7eb', '02b0bed977c344cb27b77e549eb69ed8')
    response_dict = {}
    dataGeo = g.address(streetNumber, streetName, boroughName)
    sideOfStreet = dataGeo['firstStreetNameNormalized']
    fromStreet = dataGeo['highCrossStreetName1']
    toStreet = dataGeo['lowCrossStreetName1']
    borough = dataGeo['firstBoroughName']
    response_dict.update({'sideOfStreet': sideOfStreet})
    response_dict.update({'fromStreet': fromStreet})
    response_dict.update({'toStreet': toStreet})
    response_dict.update({'borough': borough})
    
    return response_dict  
 


def send_request(url):
    ''' send request url, return result''' 
    response = requests.get(url)
    status = response.status_code
    data = response.json()
    
    return data


def build_url_0(data_dict):
    ''' construct url for SODA first call '''
    global boroughcode
   
    b_dict = {'BROOKLYN':'K', 'MANHATTAN':'M', 'QUEENS':'Q', 'STATEN ISLAND':'S', 'BRONX':'B'}
    borough = data_dict.get('borough').upper()
    boroughcode = b_dict.get(borough)   
    side_street = data_dict.get('sideOfStreet').upper() 
    f_street = data_dict.get('fromStreet').upper()
    t_street = data_dict.get('toStreet').upper()
    url = SODA_URL1 + boroughcode + '&fromstreet=' + f_street + '&tostreet=' + t_street + '&sideofstreet=' + side_street
   
    return url
  
     
def get_directions(data):
    '''get list of directions for street intersection'''
    direct_list = []
    
    for i in range(len(data)):
        dict = data[i]
        for key, value in dict.items():
            
            if(key== 'mainstreet'):
                direct_list.append(value)
                
    return direct_list  

def get_signsid(data):
    '''get list of signid and directions '''
    
    signid_list = []
    signid_direct_list = []
    direct = ' '
    for i in range(len(data)):
        dict = data[i]
        for key, value in dict.items():
            if(key== 'mainstreet'):
                direct = value
                                
            if(key== 'statusordernumber'):
                signid_list.append(value) 
                signid_direct_list.append(value + ':' + direct)  
                               
    return signid_list, signid_direct_list      
        
   
 
def parse_sign_desc(data, appendinfo):
    #get list of sign description + signid + direction
    global sign_desc_list 
    for i in range(len(data)):
        dict = data[i]
        for key, value in dict.items():
            if(key == 'signdescription'):
                if('PARKING' in value or 'NO STANDING' in value):
                    #check for duplicates
                    test_value = value.strip() + ':' + appendinfo
                    if test_value not in sign_desc_list:
                        sign_desc_list.append(test_value)
                
    return sign_desc_list
