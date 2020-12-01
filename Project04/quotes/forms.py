from django import forms
from .models import Stock, Trade, Position


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ["ticker"]
    
class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = ["stock_name", "quantity", "price", "trade_type"]

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ["stock_name", "quantity", "average"]
