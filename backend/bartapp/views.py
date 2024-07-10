from django.shortcuts import render

from django.http import JsonResponse
import requests

def get_departures(request):
    API_KEY = 'MW9S-E7SL-26DU-VV8V'
    BART_API_URL = f'http://api.bart.gov/api/etd.aspx?cmd=etd&orig=all&key={API_KEY}&json=y'

    response = requests.get(BART_API_URL)  # Corrected this line to use the variable
    data = response.json()
    return JsonResponse(data)