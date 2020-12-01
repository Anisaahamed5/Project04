from .models import Trade, Position, User

def getPrice(symbol):
    import requests
    import json

    api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ str(symbol) +"/quote?token=pk_378fb4b735894bae8434380e31b2f915")

    try:
        api = json.loads(api_request.content)
        return float(api["latestPrice"])
    except Exception as e:
        api = "Error..."

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

        # TODO: FIX THIS
        if trade.trade_type == 0:
            current.quantity = current.quantity + trade.quantity
            current.average = (current.average + trade.price) / current.quantity

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