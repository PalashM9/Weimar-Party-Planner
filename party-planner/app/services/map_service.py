from typing import Optional
from urllib.parse import quote_plus


def build_osm_map_url(
    latitude: Optional[float],
    longitude: Optional[float],
    address: Optional[str] = None
) -> Optional[str]:
    if latitude is not None and longitude is not None:
        return f"https://www.openstreetmap.org/?mlat={latitude}&mlon={longitude}#map=16/{latitude}/{longitude}"

    if address:
        return f"https://www.openstreetmap.org/search?query={quote_plus(address)}"

    return None
