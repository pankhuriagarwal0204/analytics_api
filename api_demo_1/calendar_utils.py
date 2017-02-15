import calendar
import datetime

import pytz


class calendar_iterators():

    def __init__(self):
        self.Calendar = calendar.Calendar()

    def get_daystart_time(self, _date=datetime.date.today()):
        today_beginning = datetime.datetime.combine(_date, datetime.time()).replace(tzinfo=pytz.UTC)
        return today_beginning

    def lastmonthiterator(self, strdate):
        date = datetime.datetime.strptime(str(strdate), '%Y-%m-%d').date()
        day = int(date.strftime('%d'))
        month = int(date.strftime('%m'))
        year = int(date.strftime('%Y'))
        end = self.get_daystart_time(date)
        if (month == 1):
            start = datetime.datetime(year - 1, 12, day).replace(tzinfo=pytz.UTC)
        else:
            start = datetime.datetime(year, month - 1, day).replace(tzinfo=pytz.UTC)
        while True:
            yield start
            start = start + datetime.timedelta(days=1)
            if start == end:
                break

    def monthstartend(self, strdate):
        date = datetime.datetime.strptime(str(strdate), '%Y-%m-%d').date()
        year = int(date.strftime('%Y'))
        month = int(date.strftime('%m'))
        lastdate = calendar.monthrange(year=year, month=month)[1]
        start = datetime.datetime(year, month, 1)
        end = datetime.datetime(year, month, lastdate)
        return start, end

    def lastmonthstartend(self, strdate):
        date = datetime.datetime.strptime(str(strdate), '%Y-%m-%d').date()
        day = int(date.strftime('%d'))
        month = int(date.strftime('%m'))
        year = int(date.strftime('%Y'))
        end = self.get_daystart_time(date)
        if (month == 1):
            start = datetime.datetime(year - 1, 12, day)
        else:
            start = datetime.datetime(year, month - 1, day)
        return start, end + datetime.timedelta(days=1)

    def weekstartend(self, strdate):
        date = datetime.datetime.strptime(str(strdate), '%Y-%m-%d').date()
        start = self.get_daystart_time(date)
        end = start + datetime.timedelta(days=7)
        return start, end

    def daystartend(self, strdate):
        date = datetime.datetime.strptime(str(strdate), '%Y-%m-%d').date()
        start = self.get_daystart_time(date)
        end = start + datetime.timedelta(days=1)
        return start, end