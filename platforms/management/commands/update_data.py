# platforms/management/commands/update_data.py

import requests
from django.core.management.base import BaseCommand
from platforms.models import Monumetric, Mediavine, AdThrive
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetch and update ad platform data'

    def handle(self, *args, **kwargs):
        self.update_data('http://monumetric.com/sellers.json', Monumetric, 'monumetric')
        self.update_data('http://mediavine.com/sellers.json', Mediavine, 'mediavine')
        self.update_data('http://cafemedia.com/sellers.json', AdThrive, 'adthrive')

    def update_data(self, url, model, platform_name):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses

            data = response.json()

            # Extract sellers data
            sellers = data.get('sellers', [])

            for item in sellers:
                if not model.objects.filter(domain=item['domain'], ad_platform=platform_name).exists():
                    model.objects.create(
                        seller_id=item['seller_id'],
                        name=item['name'],
                        domain=item['domain'],
                        seller_type=item['seller_type'],
                        ad_platform=platform_name
                    )
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            logger.error(f"Request error occurred: {req_err}")
        except ValueError as val_err:
            logger.error(f"Value error occurred (possibly non-JSON response): {val_err}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}")
