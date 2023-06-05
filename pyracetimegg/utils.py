# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/PyRacetimeGG/blob/main/LICENSE

from datetime import datetime, timedelta
from io import BytesIO
from json import loads
from zoneinfo import ZoneInfo
from PIL import Image
from requests import get


def fetch_json(url: str):
    return loads(get(url).text)


def fetch_image_from_url(url: str):
    return Image.open(BytesIO(get(url).content))


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
