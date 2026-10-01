from .database import save_location as db_save_adress
from .database import generate_report
from .geotag import geotag_from_coordinates
from .models import LogLocation, Time, ReportRow
from . import logger

def save_location(
        location: LogLocation,
        userid: int
    ) -> bool:
    address = geotag_from_coordinates(
        latitude=location.latitude,
        longitude=location.longitude
    ).address

    logger.info(f'saving address {address} for user {userid}')

    try:
        db_save_adress(
        address=address,
        userid=userid,
        timestamp=location.time,
        epoch_time=location.to_date_time().timestamp()
        )
    except Exception as e:
        logger.error(e)
        raise e
    return True

def get_report(
        userid: int,
        asof: str
) -> list[ReportRow]:
    t = Time(asof)

    report = [ReportRow(**row)
              for row in generate_report(
                            userid=userid,
                            asof=t.to_date_time().timestamp()
                            )
            ]

    return report