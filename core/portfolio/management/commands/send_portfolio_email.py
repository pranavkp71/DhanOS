from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from portfolio.models import Portfolio
import os
import re

class Command(BaseCommand):
    help = "Send portfolio performance email with chart"

    def handle(self, *args, **kwargs):
        portfolio = Portfolio.objects.all()
        if not portfolio:
            self.stdout.write(self.style.WARNING("No portfolio found"))
            return
        
        for portfolio in portfolio:
            user_email = portfolio.user.email
            if not user_email:
                self.stdout.write(self.style.WARNING(f"User {portfolio.user.username} has no email. Skipping."))
                continue

            safe_name = re.sub(r'\W+', '_', portfolio.name.lower())
            filename = f"{safe_name}_chart.png"
            filepath = os.path.join("charts", filename)

            subject = f"{portfolio.name} - Daily Portfolio Report"
            body = f"""

Dear {portfolio.user.first_name or portfolio.user.username},

We hope you're doing well. Please find attached the latest performance chart for your portfolio: **{portfolio.name}**.

This report reflects the total value trend of your holdings over time, helping you stay informed and make smarter investment decisions.

For a more detailed analysis, you can log in to your DhanOS dashboard at any time.

If you have any questions or need support, feel free to reach out.

Best regards,  
Team DhanOS  
Your Automated Stock Portfolio Assistant

"""
        
        msg = EmailMessage(subject, body, to={user_email})
        if os.path.exists(filepath):
            msg.attach_file(filepath)
        else:
            self.stdout.write(self.style.WARNING(f"Chart not found: {filepath}"))

        msg.send()
        self.stdout.write(self.style.SUCCESS(f"Email send to {user_email}"))