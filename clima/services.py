import requests
import json
from django.conf import settings

class Services():

    
    url = 'http://127.0.0.1:5000'

    def get_from_accuweather(lat, lng):
        r = requests.get(Services.url+'/accuweather?latitude='+ lat +'&longitude='+ lng)
        accuweather_result = r.json()
        return accuweather_result

    
    def get_from_noaa(lat, lng):
        r = requests.get(Services.url+'/noaa?latlon='+ lat +','+ lng)
        noaa_result = r.json()
        return noaa_result


    def get_from_weatherdotcom(lat, lon):
        data = {"lat":lat,"lon":lon}
        headers = {
            'Content-Type' : 'application/json'
        }
        r = requests.post(Services.url + '/weatherdotcom', data = json.dumps(data), headers = headers)
        weatherdotcom_result = r.json()
        return weatherdotcom_result

    
    def zip_to_coords(zipcode):
        r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + zipcode + '&key='+ settings.GOOGLE_API_KEY)
        coords = r.json()
        return coords
