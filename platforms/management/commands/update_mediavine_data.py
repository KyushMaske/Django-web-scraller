# platforms/management/commands/update_mediavine_data.py

import csv
import os
import requests
from datetime import datetime
from django.core.management.base import BaseCommand
from platforms.models import Mediavine

class Command(BaseCommand):
    help = 'Fetch and update Mediavine data and save updates to CSV if changes are detected'

    def handle(self, *args, **kwargs):
        url = 'http://mediavine.com/sellers.json'

        try:
            # Fetch data from Mediavine API
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            sellers = data.get('sellers', [])

            # Track updates for CSV export
            updates = []

            # Compare fetched data with existing database entries
            for item in sellers:
                obj, created = Mediavine.objects.update_or_create(
                    domain=item['domain'],
                    defaults={
                        'seller_id': item['seller_id'],
                        'name': item['name'],
                        'seller_type': item['seller_type'],
                        'date_first_added': datetime.now().date(),  # Assuming today's date for new entries
                        'ad_platform': 'mediavine',
                    }
                )
                if created or obj.date_first_added != datetime.now().date():
                    updates.append({
                        'seller_id': item['seller_id'],
                        'name': item['name'],
                        'domain': item['domain'],
                        'seller_type': item['seller_type'],
                        'date_first_added': obj.date_first_added.strftime('%Y-%m-%d'),
                        'ad_platform': 'mediavine',
                    })

            # Save updates to CSV file if changes are detected
            if updates:
                self.save_updates_to_csv(updates)
                self.stdout.write(self.style.SUCCESS('Saved updates to CSV'))

            else:
                self.stdout.write(self.style.NOTICE('No changes detected, no CSV file saved'))

        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Request error occurred: {e}"))

    def save_updates_to_csv(self, updates):
        filename = 'mediavine_updates.csv'
        file_path = os.path.join('updates', filename)  # Save in 'updates' directory

        os.makedirs('updates', exist_ok=True)  # Create 'updates' directory if it doesn't exist

        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['seller_id', 'name', 'domain', 'seller_type', 'date_first_added', 'ad_platform']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for update in updates:
                writer.writerow(update)
