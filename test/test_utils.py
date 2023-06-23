# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/PyRacetimeGG/blob/main/LICENSE


def test_place2str():
    from pyracetimegg.utils import place2str

    assert place2str(1) == "1st"
    assert place2str(11) == "11th"
    assert place2str(21) == "21st"
    assert place2str(2) == "2nd"
    assert place2str(12) == "12th"
    assert place2str(22) == "22nd"
    assert place2str(3) == "3rd"
    assert place2str(13) == "13rd"
    assert place2str(4) == "4th"


def test_parse():
    from pyracetimegg.utils import parse

    day, hour, min, second = parse("1DT02H03M04S", ("DT", "H", "M", "S"))
    assert day == "1"
    assert hour == "02"
    assert min == "03"
    assert second == "04"


def test_str2datetime():
    from datetime import datetime
    from zoneinfo import ZoneInfo
    from pyracetimegg.utils import str2datetime

    assert str2datetime("2022-03-20T11:50:38.007Z") == datetime(2022, 3, 20, 11, 50, 38, 7, tzinfo=ZoneInfo("UTC"))


def test_str2timedelta():
    from datetime import timedelta
    from pyracetimegg.utils import str2timedelta

    assert str2timedelta("P0DT00H18M07.497596S") == timedelta(minutes=18, seconds=7, milliseconds=497)
    assert str2timedelta("P1DT00H00M00S") == timedelta(days=1)


def test_joint_url():
    from pyracetimegg.utils import joint_url

    assert joint_url("a", "/b", "/c/", "d", "e/") == "a/b/c/d/e"
