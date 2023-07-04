# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/PyRacetimeGG/blob/main/LICENSE

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from io import BytesIO
from json import loads
from time import time, sleep
from threading import Lock
from typing import Any, Iterable, overload
from requests import get
from PIL import Image
from pyracetimegg.utils import joint_url


ID = str
TAG = str
DATA = dict[TAG, Any]


@dataclass(frozen=True)
class _Cache:
    cache: DATA = field(default_factory=dict)
    lock_update: Lock = field(default_factory=Lock)
    _lock_chache: Lock = field(default_factory=Lock)

    def __getitem__(self, item: TAG):
        with self._lock_chache:
            return self.cache[item]

    def update(self, data: dict):
        with self._lock_chache:
            self.cache.update(data)

    def clear(self):
        with self._lock_chache:
            self.cache.clear()


class APIBase(object):
    def __init__(self, site_url: str, request_per_second: int = 1) -> None:
        self.__site_url = site_url
        self.__throttled_request = ThrottledRequest(request_per_second)
        self.__cache: dict[str, dict[ID, _Cache]] = dict()
        self.__lock = Lock()

    @property
    def site_url(self):
        return self.__site_url

    @overload
    def get_instance(self, type_: type[iObject], id: ID):
        ...

    @overload
    def get_instance(self, type_: type[iObject], data_from_api: Any):
        ...

    def get_instance(self, type_: type[iObject], arg: ID | Any):
        if not issubclass(type_, iObject):
            raise ValueError()
        return type_(self, arg)

    def get_cache(self, class_name: str, id: ID):
        with self.__lock:
            return self.__cache.setdefault(class_name, dict()).setdefault(id, _Cache())

    def get_url(self, *paths: str):
        return joint_url(self.site_url, *paths)

    def fetch(self, url: str):
        return self.__throttled_request.get(url)

    def fetch_json(self, url: str) -> dict:
        """
        Args:
            url (str): FULL_URL
        Returns:
            dict: json data
        """
        return self.__throttled_request.get_json(url)

    def fetch_json_from_site(self, *paths: str):
        """
        Args:
            path (str): paths without site_url
        Returns:
            dict: json data
        """
        return self.fetch_json(self.get_url(*paths))

    def fetch_image_from_url(self, url: str):
        """
        Args:
            url (str): FULL_URL
        Returns:
            dict: json data
        """
        return self.__throttled_request.get_image(url)


class iObject(ABC):
    @overload
    def __init__(self, api: APIBase, id: ID):
        ...

    @overload
    def __init__(self, api: APIBase, data_from_api: Any):
        ...

    def __init__(self, api: APIBase, arg: ID | Any) -> None:
        self._api = api
        match arg:
            case ID():
                self.__id = arg
                self.__cache = api.get_cache(type(self).__name__, self.id)
            case _:
                id, data = self._format_api_data(arg)
                self.__id = id
                self.__cache = api.get_cache(type(self).__name__, self.id)
                self.__cache.update(data)

    def __eq__(self, __value: object) -> bool:
        if type(self) is not type(__value):
            return False
        return self.id == __value.id

    @property
    def id(self):
        return self.__id

    def clear(self):
        """
        clear itself from cache
        """
        with self.__cache.lock_update:
            self.__cache.clear()

    def _get(self, tag: TAG):
        """
        get tag data from cache
        """
        with self.__cache.lock_update:
            try:
                return self.__cache[tag]
            except KeyError:
                pass
            type(self)
            data = self._fetch_from_api(tag)
            self.__cache.update(data)
            return self.__cache[tag]

    def load(self, tag: TAG | Iterable[TAG] | None = None):
        """
        fetch data from api.
        if it has already loaded, it update.
        if tag is None, this func work as load_all.
        Args:
            tag : Default->None.
        """

        def _fetch_tag(tag_):
            if tag not in dir(self):
                raise KeyError("wrong tag")
            data = self._fetch_from_api(tag_)
            self.__cache.update(data)

        match tag:
            case TAG():
                with self.__cache.lock_update:
                    _fetch_tag(tag)
            case Iterable():
                with self.__cache.lock_update:
                    for tmp_tag in tag:
                        _fetch_tag(tmp_tag)
            case None:
                self.load_all()
            case _:
                raise ValueError()

    @abstractmethod
    def load_all(self):
        """
        fetch data from api.
        """
        raise NotImplementedError()

    @abstractmethod
    def _fetch_from_api(self, tag: TAG) -> DATA:
        """
        fetch tag data from api.
        return raw api data.
        """
        raise NotImplementedError()

    @abstractmethod
    def _format_api_data(self, data_from_api: Any) -> tuple[ID, DATA]:
        raise NotImplementedError()


class ThrottledRequest(object):
    def __init__(self, request_per_second: int) -> None:
        self.__rate = Rate(request_per_second)
        self.__lock = Lock()

    def get(self, url: str):
        with self.__lock:
            self.__rate.sleep()
            return get(url)

    def get_json(self, url: str) -> dict[str, Any]:
        return loads(self.get(url).text)

    def get_image(self, url: str):
        return Image.open(BytesIO(self.get(url).content))


class Rate(object):
    def __init__(self, frame_rate) -> None:
        self.__cycletime = 1 / frame_rate
        self.__time = 0

    def sleep(self):
        time_diff = time() - self.__time
        sleep_time = self.__cycletime - time_diff
        if sleep_time > 0:
            sleep(sleep_time)
            self.__time += self.__cycletime
        else:
            self.__time = time()
