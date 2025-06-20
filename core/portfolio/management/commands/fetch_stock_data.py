import yfinance as yf
from datetime import date
from django.core.management.base import BaseCommand
from portfolio.models import Holding, DailySummary

class Command(BaseCommand):
    help = 'Fetch daily stock data for each holding and save it'

    def handle(self, *args, **kwargs):
        today = date.today()
        for holding in Holding.objects.all():
            ticker = holding.ticker
            print(f"Fetching data for: {ticker}")
            stock = yf.Ticker(ticker)
            hist = stock.history(period='1d')

            if hist.empty:
                self.stdout.write(self.style.WARNING(f"No data for {ticker}"))
                continue

            row = hist.iloc[0]
            open_price = row['Open']
            close_price = row['Close']
            high_price = row['High']
            low_price = row['Low']
            total_value = close_price * float(holding.quantity)

            summary, created = DailySummary.objects.get_or_create(
                holding = holding,
                date = today,
                defaults = {
                    'open_price': open_price,
                    'close_price': close_price,
                    'high_price': high_price,
                    'low_price': low_price,
                    'total_value': total_value
                }
            )

            if not created:
                summary.open_price = open_price
                summary.close_price = close_price
                summary.high_price = high_price
                summary.low_price = low_price
                summary.total_value = total_value
                summary.save()

            self.stdout.write(self.style.SUCCESS(
                f"{'Created' if created else 'Updated'} {ticker} for {today}"
            ))