from .models import Trade, Position, User

import numpy as np
import requests
import json


def getPrice(symbol):
    api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ str(symbol) +"/quote?token=pk_378fb4b735894bae8434380e31b2f915")

    try:
        api = json.loads(api_request.content)
        return float(api["latestPrice"])
    except Exception as e:
        api = "Error..."

def getChart(symbol):
    api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ str(symbol) +"/chart/today?token=pk_378fb4b735894bae8434380e31b2f915")

    data = []
    labels = []
    
    try:
        api = json.loads(api_request.content)
        
        for i, point in enumerate(api):
            avg = point['average']
            
            if avg is None:
                data.append(data[-1])
            else:
                avg = '{:20,.2f}'.format(float(avg))
                data.append(avg)

            if i % 15 == 0:
                labels.append(point['label'])
            else:
                labels.append('')

        return data, labels

    except Exception as e:
        print(e)
        return "Error...", None

def getCharts(positions):
    labels = []
    charts = np.array([])

    for position in positions:
        data, labels = getChart(position.stock_name)

        if not isinstance(data, list):
            continue

        data = np.array(data, dtype=np.float) * position.quantity

        if(charts.size < 1):
            charts = data
        else:
            charts = np.add(charts, data)

    return charts.tolist(), labels


def validateTrade(trade):
    if trade.trade_type == 0: 
        user = getUser()
        cost = trade.price * trade.quantity

        return user.balance >= cost
    else:
        current = getPosition(trade.stock_name)

        if current:
            # if position exists
            return current.quantity >= trade.quantity

        else:
            # if position does not exist
            return False
            

def updatePositions(trade):
    current = getPosition(trade.stock_name)

    if current:
        # if position exists

        if trade.trade_type == 0:
            current.average = (current.average*current.quantity + trade.price*trade.quantity) / (current.quantity + trade.quantity)
            current.quantity = current.quantity + trade.quantity

            current.save()
        else:
            current.quantity = current.quantity - trade.quantity
            current.delete() if (current.quantity <= 0) else current.save()

    else:
        # if position does not exist
        if trade.trade_type == 0:
            position = Position(stock_name=trade.stock_name,quantity=trade.quantity,average=trade.price)
            position.save()

    updateUserBalance(trade)


def updateUserBalance(trade):
    user = getUser()

    if trade.trade_type == 0:
        user.balance = user.balance - (trade.quantity * trade.price)
    else:
        user.balance = user.balance + (trade.quantity * trade.price)
    
    user.save()
            

def getPosition(symbol):
    try:
        return Position.objects.get(stock_name=symbol)
    except Position.DoesNotExist:
        return None

def getUser():
    return User.objects.get(id=1)