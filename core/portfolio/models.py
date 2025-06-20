from django.db import models
from django.contrib.auth.models import User

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolios')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.user.username}"
    
class Holding(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='holdings')
    ticker = models.CharField(max_length=20)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.ticker} - {self.quantity}"
    
class DailySummary(models.Model):
    holding = models.ForeignKey(Holding, on_delete=models.CASCADE, related_name='daily_summaries')
    date = models.DateField()
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_value = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('holding', 'date')

    def __str__(self):
        return f"{self.holdings.ticker} - {self.date}"