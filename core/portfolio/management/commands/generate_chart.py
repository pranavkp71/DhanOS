import matplotlib.pyplot as plt
from django.core.management.base import BaseCommand
from portfolio.models import Portfolio
from datetime import timedelta

class Command(BaseCommand):
    help = 'Generate a line chart of total portfolio value over time'

    def handle(self, *args, **kwargs):
        portfolio = Portfolio.objects.first()
        if not portfolio:
            self.stdout.write(self.style.WARNING("No portfolio found."))
            return

        date_values = {}

        for holding in portfolio.holdings.all():
            for summary in holding.daily_summaries.all():
                if summary.date not in date_values:
                    date_values[summary.date] = 0
                date_values[summary.date] += float(summary.total_value)

        if not date_values:
            self.stdout.write(self.style.WARNING("No daily data found."))
            return

        dates = sorted(date_values.keys())
        values = [date_values[dt] for dt in dates]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, values, marker='o')
        plt.title(f"{portfolio.name} - Total Value Over Time")
        plt.xlabel("Date")
        plt.ylabel("Total Value (₹)")
        plt.grid(True)

        filename = f"{portfolio.name.replace(' ', '_').lower()}_chart.png"
        filepath = f"charts/{filename}"
        plt.savefig(filepath)
        plt.close()

        self.stdout.write(self.style.SUCCESS(f"Chart saved to {filepath}"))
