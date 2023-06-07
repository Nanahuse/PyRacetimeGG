# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/PyRacetimeGG/blob/main/LICENSE

from datetime import datetime, timedelta
from io import BytesIO
from json import loads
from time import sleep, time
from zoneinfo import ZoneInfo
from PIL import Image
from requests import get


class RequestThrottle:
    def __init__(self) -> None:
        self._request_throttling_per_second = 10
        self._time = time()

    def set_request_throttling_per_second(self, number: int):
        if number <= 0:
            ValueError(f"number should be over 0, but number={number}")
        self._request_throttling_per_second = number

    def wait(self):
        time_diff = time() - self._time
        sleep_time = 1 / self._request_throttling_per_second - time_diff
        if sleep_time > 0:
            sleep(sleep_time)
        self._time = time()


def throttling_request(url):
    REQUEST_THROTTLE.wait()
    return get(url)


def fetch_json(url: str):
    return loads(throttling_request(url).text)


def fetch_image_from_url(url: str):
    return Image.open(BytesIO(throttling_request(url).content))


def joint_url(*args: str):
    return "/".join(tmp.strip("/") for tmp in args)


def place2str(place: int):
    str_place = str(place)
    match str_place[-1]:
        case "1":
            if str_place[-2:] == "11":
                return f"{place}th"
            else:
                return f"{place}st"
        case "2":
            if str_place[-2:] == "12":
                return f"{place}th"
            else:
                return f"{place}nd"
        case "3":
            return f"{place}rd"
        case _:
            return f"{place}th"


def parse(string: str, parsers: tuple[str]):
    for parser in parsers:
        tmp, string = string.split(parser, 1)
        yield tmp
    if len(string) != 0:
        yield string


def str2datetime(string: str):
    if "." in string:
        year, month, day, hour, min, second, micro = parse(string, ("-", "-", "T", ":", ":", ".", "Z"))
    else:
        year, month, day, hour, min, second = parse(string, ("-", "-", "T", ":", ":", "Z"))
        micro = "0"
    return datetime(
        int(year), int(month), int(day), int(hour), int(min), int(second), int(micro[:3]), tzinfo=ZoneInfo("UTC")
    )


def str2timedelta(string: str):
    if "." in string:
        day, hour, min, second, milli = parse(string[1:], ("DT", "H", "M", ".", "S"))
    else:
        day, hour, min, second = parse(string[1:], ("DT", "H", "M", "S"))
        milli = "0"
    return timedelta(days=int(day), hours=int(hour), minutes=int(min), seconds=int(second), milliseconds=int(milli[:3]))


REQUEST_THROTTLE = RequestThrottle()
