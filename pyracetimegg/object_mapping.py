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

    def _get_instance(self, type_: Type[iObject], id: ID):
        if not issubclass(type_, iObject):
            raise ValueError()
        return type_(self, id)

    def _store_data(self, type_: Type[iObject], id: ID, data_dict: dict[TAG, Any]):
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
        return self._get_instance(type_, id)

    def _clear(self, instance: iObject):
        """
        clear instance cached data

        Args:
            instance (iObject): target instance
        """
        try:
            self.__cache[instance._class_name].pop(instance.id)
        except KeyError:
            pass

    def _get_data_from_cache(self, instance: iObject, tag: TAG) -> Any:
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

    def _get_url(self, *paths: str):
        return joint_url(self.__site_url, *paths)

    def _fetch(self, url: str):
        return self.__throttled_request.get(url)

    def _fetch_json(self, url: str) -> dict:
        """
        Args:
            url (str): FULL_URL
        Returns:
            dict: json data
        """
        return loads(self._fetch(url).text)

    def _fetch_json_from_site(self, *paths: str):
        """
        Args:
            path (str): paths without site_url
        Returns:
            dict: json data
        """
        return self._fetch_json(self._get_url(*paths))

    def _fetch_image_from_url(self, url: str):
        """
        Args:
            url (str): FULL_URL
        Returns:
            dict: json data
        """
        return Image.open(BytesIO(self._fetch(url).content))


class iObject(ABC):
    def __init__(self, api: APIBase, id: ID) -> None:
        if not isinstance(id, ID):
            ValueError("id should be ID type")
        self._api = api
        self._id = id

    @property
    def id(self):
        return self._id

    @classmethod
    @property
    def _class_name(cls):
        return cls.__name__

    def clear(self):
        """
        clear itself from cache
        """
        try:
            self._api._clear(self)
        except KeyError:
            pass

    def _get(self, tag: TAG):
        """
        get tag data from cache
        """
        if tag not in dir(self):
            raise KeyError("wrong tag")
        try:
            return self._api._get_data_from_cache(self, tag)
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
        self._request_cycletime = 1 / request_per_second
        self._time = time()

    def get(self, url: str):
        time_diff = time() - self._time
        sleep_time = self._request_cycletime - time_diff
        if sleep_time > 0:
            sleep(sleep_time)
        self._time = time()
        return get(url)
