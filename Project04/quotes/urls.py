from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    
    path('trade.html', views.trade, name="trade"),

    path('add_stock.html', views.add_stock, name="add_stock"),

    path('delete/<stock_id>', views.delete, name="delete"),

    path('history.html', views.history, name="history"),

    path('add_trade', views.add_trade, name="add_trade"),




]