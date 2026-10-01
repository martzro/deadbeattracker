import geopy
import certifi
import ssl

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx
def get_nominatim():
    return geopy.Nominatim(user_agent='roman')
def geotag_from_coordinates(
        latitude: str,
        longitude: str
) -> geopy.Location:

    with get_nominatim() as g:
        return g.reverse(
            query=f'{latitude},{longitude}'
        )

