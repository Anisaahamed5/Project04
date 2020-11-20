from django.shortcuts import render

def home(request):
    import requests
    import json

    #pk_378fb4b735894bae8434380e31b2f915
    
    api_request = requests.get("https://cloud.iexapis.com/stable/stock/aapl/quote?token=pk_378fb4b735894bae8434380e31b2f915")

    try:
        api = json.loads(api_request.content)
    except Expection as e:
        api = "Error..."

    return render(request, 'home.html', {'api': api})

def about(request):
    return render(request, 'about.html', {})

