# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/PyRacetimeGG/blob/main/LICENSE

from __future__ import annotations
from abc import ABC, abstractclassmethod, abstractmethod
from io import BytesIO
from json import loads
from time import time, sleep
from typing import Any, Type
from requests import get
from PIL import Image
from pyracetimegg.utils import joint_url


ID = str
TAG = str
CACHE = dict[Type, dict[ID, dict[TAG, Any]]]


class APIBase(object):
    def __init__(self, site_url: str, request_per_second: int = 1) -> None:
        self.__site_url = site_url
        self.__throttled_request = ThrottledRequest(request_per_second)
        self.__cache: CACHE = dict()

    @property
    def site_url(self):
        return self.__site_url

    def get_instance(self, type_: Type[iObject], id: ID):
        if not issubclass(type_, iObject):
            raise ValueError()
        return type_(self, id)

    def store_data(self, type_: Type[iObject], id: ID, data_dict: dict[TAG, Any]):
        """
        store in cache

        Args:
            type_ (Type[iObject]): fisrt key
            id (ID): second key
            data_dict (dict[TAG, Any]): if there is same tag data, it will be updated by data_dict's one.
        """
        name = type_._class_name
        if name not in self.__cache:
            self.__cache[name] = dict()
        if id not in self.__cache[name]:
            self.__cache[name][id] = dict()
        self.__cache[name][id].update(data_dict)
        return self.get_instance(type_, id)

    def clear(self, instance: iObject):
        """
        clear instance cached data

        Args:
            instance (iObject): target instance
        """
        try:
            self.__cache[instance._class_name].pop(instance.id)
        except KeyError:
            pass

    def get_data_from_cache(self, instance: iObject, tag: TAG) -> Any:
        """
        get cached data

        Args:
            instance (iObject): target instance
            tag (TAG): target tag
        """
        try:
            return self.__cache[instance._class_name][instance.id][tag]
        except KeyError:
            raise

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
    def __init__(self, api: APIBase, id: ID) -> None:
        if not isinstance(id, ID):
            ValueError("id should be ID type")
        self._api = api
        self.__id = id

    @property
    def id(self):
        return self.__id

    @classmethod
    @property
    def _class_name(cls):
        return cls.__name__

    def clear(self):
        """
        clear itself from cache
        """
        try:
            self._api.clear(self)
        except KeyError:
            pass

    def _get(self, tag: TAG):
        """
        get tag data from cache
        """
        if tag not in dir(self):
            raise KeyError("wrong tag")
        try:
            return self._api.get_data_from_cache(self, tag)
        except KeyError:
            pass
        return self._fetch_from_api(tag)

    @abstractmethod
    def _fetch_from_api(self, tag: TAG) -> Any:
        """
        fetch tag data from api.
        if it has already loaded, it update.
        """
        raise NotImplementedError()

    @abstractmethod
    def _load_all(self):
        """
        fetch data from api.
        """
        raise NotImplementedError()

    def load(self, tag: TAG | tuple[TAG] | list[TAG] | None = None):
        """
        fetch data from api.
        if it has already loaded, it update.

        Args:
            tag (TAG | tuple[TAG] | list[TAG] | None, optional): if tag is None, fetch all data. Defaults to None.
        """
        match tag:
            case TAG():
                if tag not in dir(self):
                    raise KeyError("wrong tag")
                self._fetch_from_api(tag)
            case tuple() | list():
                for tmp in tag:
                    self._fetch_from_api(tmp)
            case None:
                self._load_all()

    @abstractclassmethod
    def _load_from_json(cls, api: APIBase, json_: dict[TAG, Any]) -> iObject:
        """
        store data in cache from json.
        if it has already loaded, it update.
        """
        raise NotImplementedError()


class ThrottledRequest(object):
    def __init__(self, request_per_second: int) -> None:
        self.__request_cycletime = 1 / request_per_second
        self.__time = 0

    def get(self, url: str):
        time_diff = time() - self.__time
        sleep_time = self.__request_cycletime - time_diff
        if sleep_time > 0:
            sleep(sleep_time)
            self.__time += self.__request_cycletime
        else:
            self.__time = time()
        return get(url)

    def get_json(self, url: str) -> dict[str, Any]:
        return loads(self.get(url).text)

    def get_image(self, url: str):
        return Image.open(BytesIO(self.get(url).content))
