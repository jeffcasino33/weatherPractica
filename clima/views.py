from django.shortcuts import render
from django.http.response import JsonResponse
import json
from clima.services import Services

def average_temperature(request, latlng, filters):

    #convert the 2 params in URL (latlng, filters) in arrays delimited by ","

    filters = filters.split(',')
    latlng = latlng.split(',')

    results = []

    #first parameter in URL can be either a zipcode or coordinates (separated by ',') so validating its len() we can decide if there
    #are 2 coordinates or 1 zipcode to convert it

    if(len(latlng) <= 1):
        latlng = zip_to_coords(latlng[0])

    # for each filter we call its method and append the result to results[]
    for i in filters:
        if (i == 'noaa'):
            results.append(get_from_noaa(latlng))
        
        if (i == 'accuweather'):
            results.append(get_from_accuweather(latlng))

        if (i == 'weatherdotcom'):
            results.append(get_from_weatherdotcom(latlng))
    
    
    #validate if there is any error and return error message or get the average for all the temperatures in results[] and return in Json
    if ("error" in results):
        return JsonResponse({'error': "must be a valid coordinates or zipcode"})

    avg = sum(results) / len(results)

    return JsonResponse({'average_temperature': avg})


#each method call its corresponding Service in Services.py and return an integer for the temperature (in fahrenheit)

def get_from_noaa(latlng):

    try:
        res = Services.get_from_noaa(latlng[0], latlng[1])
    except:
        return "error"

    return int(res['today']['current']['fahrenheit'])

def get_from_accuweather(latlng):

    try:
        res = Services.get_from_accuweather(latlng[0], latlng[1])
    except:
        return "error"

    return int(res['simpleforecast']['forecastday'][0]['current']['fahrenheit'])

def get_from_weatherdotcom(latlng):

    try:
        res = Services.get_from_weatherdotcom(float(latlng[0]), float(latlng[1]))
    except:
        return "error"

    return int(res['query']['results']['channel']['condition']['temp'])


#here we call a Service to transform zipcodes to lat lng throught google maps api

def zip_to_coords(zipcode):

    try:
        r = Services.zip_to_coords(zipcode)
        res = [str(r['results'][0]['geometry']['location']['lat']), str(r['results'][0]['geometry']['location']['lng'])]
    except:
        return "error"

    return res