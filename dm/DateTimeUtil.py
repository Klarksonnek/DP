"""Converts various time formats (one to another).
"""
import datetime
import pytz

__author__ = ''
__email__ = ''


class DateTimeUtil:
    @staticmethod
    def local_time_str_to_utc(date_str, timezone='Europe/Prague', format='%Y/%m/%d %H:%M:%S'):
        # https://www.saltycrane.com/blog/2009/05/converting-time-zones-datetime-objects-python/

        datetime_obj_naive = datetime.datetime.strptime(date_str, format)
        datetime_obj_pacific = pytz.timezone(timezone).localize(datetime_obj_naive)

        return datetime_obj_pacific

    @staticmethod
    def utc_timestamp_to_local_time(timestamp, timezone='Europe/Prague'):
        utc = datetime.datetime.fromtimestamp(timestamp, pytz.timezone('UTC'))
        local_time = utc.astimezone(pytz.timezone(timezone))

        return local_time

    @staticmethod
    def utc_timestamp_to_str(timestamp, format='%Y-%m-%d %H:%M:%S'):
        local_time = DateTimeUtil.utc_timestamp_to_local_time(timestamp, 'Europe/Prague')

        return local_time.strftime(format)

    @staticmethod
    def create_interval_str(start, end):
        out = DateTimeUtil.utc_timestamp_to_str(start)
        out += ' - '
        out += DateTimeUtil.utc_timestamp_to_str(end, '%H:%M:%S')

        return out
