from fastapi import FastAPI, Response, Request
from datetime import datetime
import uvicorn

from .api import save_location, get_report
from .models import LogLocation
from ..logging.logger import logger

app = FastAPI()

@app.get('/')
def index():
    return Response(content='hi',
                    status_code=200)
@app.post("/log/{userid}")
def log(
    location: LogLocation,
    userid: int,
    ) -> Response:
    logger.info(location)

    if location.to_date_time().second == 0:
        location.time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')

    try:
        if save_location(location, userid):
            return Response(status_code=200)
    except Exception as e:
        return Response(
            content=str(e),
            status_code=500
        )

@app.get("/report/{userid}")
def report(
    userid: int,
    asof: str
) -> Response:
    logger.info(f"{userid} {asof}")

    return get_report(
        userid,
        asof
    )
    
if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host='192.168.0.128',
        port=8000
    )