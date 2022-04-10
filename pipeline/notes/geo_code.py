import logging

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

log = logging.getLogger(__name__)

geolocator = Nominatim(user_agent="barry_li_notes_processing_pipeline")


def geo_code(location):
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    loc = geocode(location)
    return loc
