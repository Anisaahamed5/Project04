from django.shortcuts import render

def home(request):
    import requests
    import json

    if request.method == 'POST':
        ticker = request.POST['ticker']

        #pk_378fb4b735894bae8434380e31b2f915
        # GET www.mysite.com/newuser => Returns the new user page
        # POST www.mysite.com/newuser => signs up a new user with the form data

        api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ ticker +"/quote?token=pk_378fb4b735894bae8434380e31b2f915")

        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        return render(request, 'home.html', {'api': api})

    else:
        return render(request, 'home.html', {'ticker': "enter a ticker symbol above"})


def about(request):
    return render(request, 'about.html', {})

def add_stock(request):
    return render(request, 'add_stock.html', {})



