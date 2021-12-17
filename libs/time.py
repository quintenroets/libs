import calendar
import os
from datetime import datetime
from dateutil import tz

from libs.parser import Parser
from libs.cli import Cli

def to_string(utc_string):
    string = Parser.rbetween(utc_string, None, ":")

    date, time = string.split("T")
    year, month, day = date.split("-")
    hour, min = time.split(":")

    hour = str(int(hour) + 1)
    month = calendar.month_name[int(month)]
    day, hour = day.lstrip("0"), hour.lstrip("0")
    return f"{day} {month} {year} - {hour}:{min}"

def utc_to_epoch(string, format="%Y-%m-%dT%H:%M:%S.%fZ"):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal() # convert to own timezone

    timestamp = datetime.strptime(string, format)

    timestamp = timestamp.replace(tzinfo=from_zone)
    central = timestamp.astimezone(to_zone)

    return central.timestamp()

def epoch_to_utc(time):
    return datetime.fromtimestamp(time).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

def set_time(file, timestamp):
    if not timestamp:
        return

    if type(timestamp) == str:
        # need seconds since epoch
        timestamp = utc_to_epoch(timestamp) + 3600

    os.utime(file, (timestamp, timestamp))
    Cli.run(f'touch -d "@{timestamp}" "{file}"')
