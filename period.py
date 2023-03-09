import schoolsoft_api, datetime
from typing import Iterable, Union, Generator

class Period:


    def __init__(self, api: schoolsoft_api.Api, name: str, weeks: Iterable[int], weekday: int, time: Union[datetime.time, datetime.datetime], end: Union[datetime.time, datetime.datetime, int], tz: datetime.tzinfo = None, human_readable_name: str = None, conversion: dict = {}):
        self._api = api
        self._name = name.split(" -")[0]
        self._human_readable_name = human_readable_name or conversion.get(self._name, self._name)
        print(conversion.get(self._name, self._name))
        self._tz = tz or datetime.datetime.now().tzinfo
        self._weeks = set(weeks)
        self._weekday = weekday + 1
        if isinstance(time, datetime.time):
            self._time = time
        else:
            self._time = datetime.time(time.hour, time.minute, time.second, time.microsecond)
        if isinstance(end, datetime.time):
            self._end = end
        elif isinstance(end, datetime.datetime):
            self._end = datetime.time(end.hour, end.minute, end.second, end.microsecond)
        else:
            self._end = time + datetime.timedelta(minutes=end)
        self._length: datetime.timedelta = end - time

    def getDates(self, isoyearHT: int = None, isoyearVT: int = None, weeks: Iterable[int] = None) -> Generator[datetime.datetime, None, None]:
        nowYear, nowWeek, _ = datetime.datetime.now().isocalendar()
        yearHT = isoyearHT or (nowYear if nowWeek > 26 else nowYear - 1)
        yearVT = isoyearVT or (nowYear if nowWeek < 27 else nowYear + 1)
        weeks = weeks or self._weeks

        for week in weeks:
            if week < 27:
                yield datetime.datetime.fromisocalendar(year=yearVT, week=week, day=self._weekday)
            else:
                yield datetime.datetime.fromisocalendar(year=yearHT, week=week, day=self._weekday)
    
    def __str__(self) -> str:
        l = list(self._weeks)
        l.sort()
        l = [str(_) for _ in l]
        return f"{self._length.seconds//60} minutes {self._human_readable_name} at {self._time.strftime('%H:%M')}. Weeks {', '.join(l)} on {self.getDates().__next__().strftime('%A')}."
        