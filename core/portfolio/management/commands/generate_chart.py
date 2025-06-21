import matplotlib.pyplot as plt
from django.core.management.base import BaseCommand
from portfolio.models import Portfolio
from datetime import timedelta
import re
import os

class Command(BaseCommand):
    help = 'Generate a line chart of total portfolio value over time'

    def handle(self, *args, **kwargs):
        portfolio = Portfolio.objects.all()

        if not portfolio:
            self.stdout.write(self.style.WARNING("No portfolios found."))
            return

        for portfolio in portfolio:
            date_values = {}

            for holding in portfolio.holdings.all():
                for summary in holding.daily_summaries.all():
                    if summary.date not in date_values:
                        date_values[summary.date] = 0
                    date_values[summary.date] += float(summary.total_value)

            if not date_values:
                self.stdout.write(self.style.WARNING(f"No daily data for {portfolio.name}"))
                continue

            dates = sorted(date_values.keys())
            values = [date_values[dt] for dt in dates]

            plt.figure(figsize=(10, 5))
            plt.plot(dates, values, marker='o')
            plt.title(f"{portfolio.name} - Total Value Over Time")
            plt.xlabel("Date")
            plt.ylabel("Total Value (₹)")
            plt.grid(True)

            safe_name = re.sub(r'\W+', '_', portfolio.name.lower())
            filename = f"{safe_name}_chart.png"
            filepath = os.path.join("charts", filename)

            plt.savefig(filepath)
            plt.close()

            self.stdout.write(self.style.SUCCESS(f"Chart saved for {portfolio.user.username} to {filepath}"))