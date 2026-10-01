import requests
from datetime import datetime, timedelta
from faker import Faker
from time import sleep
from src.app.models import LogLocation
from src.app.geotag import get_nominatim
from src.app import logger

test_url = 'http://192.168.0.128:8000'

def test_save_location():
    endpoint = f'{test_url}/log/100'
    headers = {}
    faker = Faker()
    lat, long, name, _, _ = faker.location_on_land()
    location = LogLocation(
        address=name,
        longitude=long,
        latitude=lat,
        time=str(datetime.now().isoformat())
    ).model_dump()
    print(location)
    resp = requests.post(endpoint, headers=headers, json=location)
    assert resp.status_code == 200, resp.content


def test_multiple_locations_get_report():
    logger.debug(f'test case test_multiple_locations_get_report')
    post_endpoint = f'{test_url}/log/200'
    get_endpoint = f'{test_url}/report/200'
    with get_nominatim() as gp:
        locations = [
            # '10 innerbelt rd 02143 somerville MA',
            '12A Tyler St, Somerville, MA 02143',
            '400 Somerville Ave, Somerville, MA 02143'
        ]
        for location in locations:
            gc = gp.geocode(location)
            lat,long,address = (gc.latitude, gc.longitude, gc.address)
            logger.debug(f'{lat=} {long=} {address=}')
            for time in range(1,5):
                headers = {}
                location = LogLocation(
                    address=address,
                    longitude=str(long),
                    latitude=str(lat),
                    time=(datetime.now() + timedelta(minutes=time)).isoformat()
                ).model_dump()
                logger.debug(location)
                resp = requests.post(post_endpoint, headers=headers, json=location)
                assert resp.status_code == 200, resp.content
            sleep(5)

        resp = requests.get(get_endpoint, params={'asof': (datetime.now() - timedelta(days=1)).isoformat()})
        assert resp.status_code == 200, resp.status_code            
        
        for row in resp.json():
                print(row)
            

