from django.db import models


class Stock(models.Model):
    ticker = models.CharField(max_length=10)

    def __str__(self):
        return self.ticker

class Transactions(models.Model):
        stock_name = models.CharField(max_length=10)
        quantity = models.IntegerField()
        value = models.IntegerField()
        buy_sell = models.IntegerField()


