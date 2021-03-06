from django.shortcuts import render, redirect
from .models import Stock, Trade, User, Position
from .forms import StockForm, TradeForm
from django.contrib import messages
from .utils import getPrice, updatePositions, validateTrade, getChart, getCharts, getUser

def home(request):
    import requests
    import json

    if request.method == 'POST':
        ticker = request.POST['ticker']

        #pk_378fb4b735894bae8434380e31b2f915

        api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ ticker +"/quote?token=pk_378fb4b735894bae8434380e31b2f915")

        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        return render(request, 'home.html', {'api': api})

    else:
        return render(request, 'home.html', {'ticker': ""})


def trade(request):
    import requests
    import json

    user, created = User.objects.get_or_create(
        id = 1,
        defaults={'balance': 1000000.00},
    )

    # data, labels = getChart("aapl")
    account_value = user.balance
    positions = Position.objects.all()

    ticker = request.GET.get('ticker', '')
    if ticker == '':
        data, labels = getCharts(positions)
        title = 'Your Account Value'
    else:
        title = 'Ticker: ' + ticker
        data, labels = getChart(ticker)
    
    for position in positions:
        account_value += position.quantity * getPrice(position.stock_name)
        position.price = getPrice(position.stock_name) * position.quantity

    return render(request, 'trade.html', {'balance': user.balance, 'value': account_value, 'positions': positions, 'data': data, 'labels': labels, 'title': title})

def add_stock(request):
    import requests
    import json

    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Stock Has Been Added Successfully!"))
            return redirect ('add_stock')
    else:
        ticker = Stock.objects.all()
        output =[]
        for ticker_item in ticker:
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ str(ticker_item) +"/quote?token=pk_378fb4b735894bae8434380e31b2f915")

            try:
                api = json.loads(api_request.content)
                api['id'] = ticker_item.id
                output.append(api)
            except Exception as e:
                api = "Error..."

        return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})

def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock Has Been Deleted!"))
    return redirect ('add_stock')

def history(request):
    trades = Trade.objects.all()
    return render(request, 'history.html', {'trades': trades})

def add_trade (request):
    if request.method == 'POST':
        data = {
            'stock_name': request.POST['stock_name'],
            'quantity': request.POST['quantity'],
            'price': getPrice(request.POST['stock_name']),
            'trade_type': request.POST['trade_type'],
        }

        form = TradeForm(data or None)
        print(data['trade_type'])

        if form.is_valid():
            new_trade = form.save(commit=False)

            if not validateTrade(new_trade):
                messages.error(request, ("Your trade was invalid!"))
                return redirect('trade')

            
            trade = form.save()

            updatePositions(trade)

            messages.success(request, ("Trade was made successfully!"))
            return redirect ('trade')
        else: 
            messages.error(request, ("There was an issue with your entry, please try again.", form.errors))
            return redirect ('trade')

def reset (request):
    Trade.objects.all().delete()
    Position.objects.all().delete()
    
    user = getUser()
    user.balance = 1000000.00
    user.save()

    return redirect ('trade')
