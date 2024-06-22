import requests
from datetime import date
from .models import Monumetric, Mediavine, AdThrive

def fetch_and_update(url, model, ad_platform):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get('sellers', [])
        for item in data:
            domain = item['domain']
            if not model.objects.filter(domain=domain, ad_platform=ad_platform).exists():
                model.objects.create(
                    seller_id=item.get('seller_id', ''),
                    name=item.get('name', ''),
                    domain=domain,
                    seller_type=item.get('seller_type', ''),
                    date_first_added=date.today(),
                    ad_platform=ad_platform
                )

def update_data():
    fetch_and_update('http://monumetric.com/sellers.json', Monumetric, 'monumetric')
    fetch_and_update('http://mediavine.com/sellers.json', Mediavine, 'mediavine')
    fetch_and_update('http://cafemedia.com/sellers.json', AdThrive, 'adthrive')
