from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from portfolio.models import Portfolio
import os
import re

class Command(BaseCommand):
    help = "Send portfolio performance email with chart"

    def handle(self, *args, **kwargs):
        portfolio = Portfolio.objects.first()
        if not portfolio:
            self.stdout.write(self.style.ERROR("No portfolio found"))
            return
        
        user_email = portfolio.user.email
        if not user_email:
            self.stdout.write(self.style.ERROR("User does not have an email"))
            return
        
        safe_name = re.sub(r'\W+', '_', portfolio.name.lower())
        filename = f"{safe_name}_chart.png"
        filepath = os.path.join("charts", filename)

        subject = f"{portfolio.name} - Daily Portfolio Report"
        body = f"""
Hi {portfolio.user.username},

Attached is your latest portfolio performance chart.
You can log in to view detailed stats.

Regards,
DhanOs
"""
        
        msg = EmailMessage(subject, body, to={user_email})
        if os.path.exists(filepath):
            msg.attach_file(filepath)
        else:
            self.stdout.write(self.style.WARNING(f"Chart not found: {filepath}"))

        msg.send()
        self.stdout.write(self.style.SUCCESS(f"Email send to {user_email}"))