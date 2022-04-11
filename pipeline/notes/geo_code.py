import functools
import logging

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

log = logging.getLogger(__name__)

geolocator = Nominatim(user_agent="barry_li_notes_processing_pipeline")
geocode_limit = RateLimiter(geolocator.geocode, min_delay_seconds=1)
geocode = functools.lru_cache(maxsize=1024)(
    functools.partial(geocode_limit, timeout=5)
)


def geo_code(location):
    loc = geocode(location)
    try:
        log.info(f'Geocoding: {location}.')
        return {
            'address': loc.address,
            'latitude': loc.latitude,
            'longitude': loc.longitude,
        }
    except Exception as e:
        log.error(f'Failed to geocode: {location}. Exception: {e}.')
        return {
            'address': None,
            'latitude': None,
            'longitude': None,
        }
