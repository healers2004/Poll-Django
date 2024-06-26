import geoip2.database
from django.conf import settings

def get_geolocation(ip):
    reader = geoip2.database.Reader(settings.GEOIP_CITY)
    try:
        response = reader.city(ip)
        return {
            'ip': ip,
            'city': response.city.name,
            'country': response.country.name,
        }
    except geoip2.errors.AddressNotFoundError:
        return {
            'ip': ip,
            'city': None,
            'country': None,
        }
