import sqlite3
from pathlib import Path
from . import logger

DATABASE = Path(__file__).parent / '../database/db.db'

def database() -> sqlite3.Connection:
    return sqlite3.connect(DATABASE)

def generate_report(
        userid: str,
        asof: int
) -> list[dict]:
    day_in_seconds = 86_400
    """
    make report of time in locations since asof date
    asof date should be epoch time
    """

    sql = f"""
select
min(epochtime) as           start_time,
max(epochtime) as           end_time,   
                            address,
round(max(epochtime) -
min(epochtime),0) as        seconds_spent
from log
where userid = ?
and epochtime >= ?
group by
userid,
address
"""
    with database() as db:
        cur = db.cursor()
        cur.execute(sql, (userid, asof))
        columns = [i[0] for i in cur.description]
        return [
            dict(zip(columns, row))
            for row in cur.fetchall()
        ]
    return resp

def save_location(
    address: str,
    userid: str,
    timestamp: str,
    epoch_time: float,
    ) -> bool:
    sql = f"""
insert into log (address,userid,timestamp,epochtime) values (?,?,?,?)
"""
    with database() as db:
        db.execute(sql, (address,userid,timestamp,epoch_time))
        db.commit()

    logger.debug(f'saved {address} {userid} {timestamp} {epoch_time} with sql {sql}')

def setup() -> None:
    sql = """
create table if not exists users (
id number primary key
);

create table if not exists log (
address text,
userid number,
timestamp text,
epochtime number
);

create index if not exists user_idx on log(userid);
"""

    with database() as db:
        db.executescript(sql)

if __name__ == '__main__':
    setup()