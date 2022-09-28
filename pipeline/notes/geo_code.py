import functools
import logging

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

log = logging.getLogger(__name__)

geolocator = Nominatim(user_agent="barry_li_notes_processing_pipeline")

geocode_limit = RateLimiter(geolocator.geocode, min_delay_seconds=1)
reverse_limit = RateLimiter(geolocator.reverse, min_delay_seconds=1)

geocode = functools.lru_cache(maxsize=1024)(
    functools.partial(geocode_limit, timeout=5)
)

reverse = functools.lru_cache(maxsize=1024)(
    functools.partial(reverse_limit, timeout=5)
)


def geo_code(location):
    try:
        loc = geocode(location, language='en')
        rev = reverse((loc.latitude, loc.longitude), language='en')

        rev_address = rev.raw.get('address')

        log.info(f'Geocoding: {location}.')
        return {
            'address': loc.address,
            'latitude': loc.latitude,
            'longitude': loc.longitude,
            'city': rev_address.get('city') if rev_address is not None else None,
            'state': rev_address.get('state') if rev_address is not None else None,
            'country': rev_address.get('country') if rev_address is not None else None,
            'country_code': rev_address.get('country_code') if rev_address is not None else None,
        }
    except Exception as e:
        log.error(f'Failed to geocode: {location}. Exception: {e}.')
        return {
            'address': None,
            'latitude': None,
            'longitude': None,
            'city': None,
            'state': None,
            'country': None,
            'country_code': None,
        }
