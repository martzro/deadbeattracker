from datetime import datetime
from pydantic import BaseModel, model_validator
from dataclasses import dataclass
from . import logger

class LogLocation(BaseModel):
    address: str
    longitude: str
    latitude: str
    time: str

    def to_date_time(self) -> datetime:
         t = Time(self.time)
         return t.to_date_time()

class ReportRow(BaseModel):
     start_time: float
     end_time: float
     address: str
     seconds_spent: int

@dataclass
class Time():
    time: str

    def to_date_time(self) -> datetime:
            try:
                ts = datetime.strptime(self.time,
                                        '%Y-%m-%dT%H:%M:%S.%f')
            except:
                try:
                    ts = datetime.fromisoformat(self.time)
                except Exception as e:
                    logger.error(e)
                    raise e
                
            logger.debug(f'converted time {self.time} to {ts}')
            return ts