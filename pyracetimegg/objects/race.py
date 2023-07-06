# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/PyRacetimeGG/blob/main/LICENSE

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from inspect import currentframe
from threading import Lock
from typing import Sequence, overload, TYPE_CHECKING
from sys import maxsize
from pyracetimegg.object_mapping import APIBase, iObject, ID, DATA, TAG
from pyracetimegg.utils import str2datetime, str2timedelta, place2str

if TYPE_CHECKING:
    from typing_extensions import SupportsIndex
    from pyracetimegg.objects.user import User
    from pyracetimegg.objects.category import Category


class Race(iObject):
    class Status(Enum):
        OPEN = "open"
        INVITATIONAL = "invitational"
        PENDING = "pending"
        IN_PROGRESS = "in_progress"
        FINISHED = "finished"
        CANCELLED = "cancelled"

        @classmethod
        def from_str(cls, string: str):
            for status in Race.Status:
                if status.value == string:
                    return status
            raise ValueError(string)

    @dataclass(frozen=True)
    class Entrant(object):
        class Status(Enum):
            REQUESTED = "requested"  # requested to join
            INVITED = "invited"  # invited to join
            DECLINED = "declined"  # declined invitation
            READY = "ready"
            NOT_READY = "not_ready"
            IN_PROGRESS = "in_progress"
            DONE = "done"
            DNF = "dnf"  # did not finish, i.e. forfeited
            DQ = "dq"  # disqualified

            @classmethod
            def from_str(cls, string: str):
                for tmp in Race.Entrant.Status:
                    if tmp.value == string:
                        return tmp
                raise ValueError(string)

        user: User
        team: str | None
        status: Status
        finish_time: timedelta | None
        finished_at: datetime | None
        place: int

        @property
        def place_ordinal(self):
            return place2str(self.place)

        score: int | None
        score_change: int | None

        comment: str | None
        has_comment: bool
        stream_live: bool
        stream_override: bool

        @classmethod
        def from_json(cls, api: APIBase, json_data: dict):
            from pyracetimegg.objects.user import User

            return Race.Entrant(
                api.get_instance(User, json_data["user"]),
                json_data.get("team", None),
                Race.Entrant.Status.from_str(json_data["status"]["value"]),
                str2timedelta(json_data["finish_time"]) if json_data["finish_time"] is not None else None,
                str2datetime(json_data["finished_at"]) if json_data["finished_at"] is not None else None,
                json_data["place"],
                json_data["score"],
                json_data["score_change"],
                json_data["comment"],
                json_data["has_comment"],
                json_data["stream_live"],
                json_data["stream_override"],
            )

    @property
    def slug(self) -> str:
        return self._get(currentframe().f_code.co_name)

    @property
    def name(self):
        return self.id

    @property
    def status(self) -> Race.Status:
        return self._get(currentframe().f_code.co_name)

    @property
    def goal(self) -> Goal:
        return self._get(currentframe().f_code.co_name)

    @property
    def info(self) -> str:
        return self._get(currentframe().f_code.co_name)

    @property
    def category(self) -> Category:
        return self._get(currentframe().f_code.co_name)

    @property
    def url(self):
        return self._api.get_url(self.name)

    @property
    def data_url(self):
        return f"{self.url}/data"

    @property
    def websocket_url(self):
        return self._api.get_url("ws/race", self.slug)

    @property
    def websocket_bot_url(self):
        return self._api.get_url("ws/o/bot", self.slug)

    @property
    def websocket_oauth_url(self):
        return self._api.get_url("ws/o/race", self.slug)

    @property
    def version(self) -> int:
        return self._get(currentframe().f_code.co_name)

    @property
    def info_bot(self) -> str:
        return self._get(currentframe().f_code.co_name)

    @property
    def info_user(self) -> str:
        return self._get(currentframe().f_code.co_name)

    @property
    def team_race(self) -> bool:
        return self._get(currentframe().f_code.co_name)

    # Race info (Time)
    @property
    def opened_at(self) -> datetime:
        return self._get(currentframe().f_code.co_name)

    @property
    def opened_by(self) -> User:
        return self._get(currentframe().f_code.co_name)

    @property
    def start_delay(self) -> timedelta:
        return self._get(currentframe().f_code.co_name)

    @property
    def started_at(self) -> datetime | None:
        return self._get(currentframe().f_code.co_name)

    @property
    def ended_at(self) -> datetime | None:
        return self._get(currentframe().f_code.co_name)

    @property
    def cancelled_at(self) -> datetime | None:
        return self._get(currentframe().f_code.co_name)

    @property
    def unlisted(self) -> bool:
        return self._get(currentframe().f_code.co_name)

    # Race Option
    @property
    def time_limit(self) -> timedelta:
        return self._get(currentframe().f_code.co_name)

    @property
    def time_limit_auto_complete(self) -> bool:
        return self._get(currentframe().f_code.co_name)

    @property
    def require_even_teams(self) -> bool:
        return self._get(currentframe().f_code.co_name)

    @property
    def streaming_required(self) -> bool:
        return self._get(currentframe().f_code.co_name)

    @property
    def auto_start(self) -> bool:
        return self._get(currentframe().f_code.co_name)

    @property
    def recordable(self) -> bool:
        return self._get(currentframe().f_code.co_name)

    @property
    def recorded(self) -> bool:
        return self._get(currentframe().f_code.co_name)

    @property
    def recorded_by(self) -> User | None:
        return self._get(currentframe().f_code.co_name)

    @property
    def allow_comments(self) -> bool:
        return self._get(currentframe().f_code.co_name)

    @property
    def hide_comments(self) -> bool:
        return self._get(currentframe().f_code.co_name)

    @property
    def allow_prerace_chat(self) -> bool:
        return self._get(currentframe().f_code.co_name)

    @property
    def allow_midrace_chat(self) -> bool:
        return self._get(currentframe().f_code.co_name)

    @property
    def allow_non_entrant_chat(self) -> bool:
        return self._get(currentframe().f_code.co_name)

    @property
    def chat_message_delay(self) -> timedelta:
        return self._get(currentframe().f_code.co_name)

    @property
    def monitors(self) -> tuple[User]:
        return self._get(currentframe().f_code.co_name)

    @property
    def entrants(self) -> tuple[Entrant]:
        return self._get(currentframe().f_code.co_name)

    @property
    def entrants_count(self) -> int:
        return self._get(currentframe().f_code.co_name)

    @property
    def entrants_count_finished(self) -> int:
        return self._get(currentframe().f_code.co_name)

    @property
    def entrants_count_inactive(self) -> int:
        return self._get(currentframe().f_code.co_name)

    def load_all(self):
        self._fetch_from_api("category")

    def _fetch_from_api(self, tag: TAG):
        json_data = self._api.fetch_json(self.data_url)
        _, data = self._format_api_data(json_data)
        return data

    def _format_api_data(self, data_from_api: dict) -> tuple[ID, DATA]:
        from pyracetimegg.objects.user import User
        from pyracetimegg.objects.category import Category

        output = dict()
        id = data_from_api["name"]
        category_slug, slug = id.split("/")
        data_from_api.setdefault("category", {"slug": category_slug})
        data_from_api["slug"] = slug

        for key, value in data_from_api.items():
            match key:
                case "status":
                    output[key] = Race.Status.from_str(value["value"])
                case "goal":
                    output[key] = Goal(value["name"], value["custom"])
                case "opened_at" | "started_at" | "ended_at" | "cancelled_at":
                    output[key] = str2datetime(value) if value is not None else None
                case "time_limit" | "start_delay" | "chat_message_delay":
                    output[key] = str2timedelta(value) if value is not None else None
                case "category":
                    output[key] = self._api.get_instance(Category, value)
                case "opened_by" | "recorded_by":
                    if value is None:
                        output[key] = None
                    else:
                        output[key] = self._api.get_instance(User, value)
                case "monitors":
                    output[key] = tuple(self._api.get_instance(User, tmp) for tmp in value)
                case "entrants":
                    output[key] = tuple(Race.Entrant.from_json(self._api, tmp) for tmp in value)
                case _:
                    if key in (
                        "slug",
                        "info",
                        "version",
                        "info_bot",
                        "info_user",
                        "team_race",
                        "unlisted",
                        "time_limit_auto_complete",
                        "require_even_teams",
                        "streaming_required",
                        "auto_start",
                        "recordable",
                        "recorded",
                        "allow_comments",
                        "hide_comments",
                        "allow_prerace_chat",
                        "allow_midrace_chat",
                        "allow_non_entrant_chat",
                        "entrants_count",
                        "entrants_count_finished",
                        "entrants_count_inactive",
                    ):
                        output[key] = value

        return id, output


class PastRaces(Sequence[Race]):
    def __init__(self, obj: Category | User) -> None:
        from pyracetimegg.objects.user import User
        from pyracetimegg.objects.category import Category

        self.__api = obj._api
        match obj:
            case Category():
                self._base_path = obj.slug
            case User():
                self._base_path = f"user/{obj.id}"
            case _:
                raise ValueError()
        self.__lock = Lock()
        with self.__lock:
            self.__race_cache: list[Race | None] | None = None

    def __fetch_json(self, page_num: int):
        return self.__api.fetch_json_from_site(self._base_path, f"races/data?show_entrants=yes&page={page_num}")

    def __init_list(self):
        with self.__lock:
            if self.__race_cache is not None:
                return
            json_data = self.__fetch_json(1)
            self.__race_cache: list[Race | None] = [None] * json_data["count"]
            for i, race in enumerate(json_data["races"]):
                self.__race_cache[i] = self.__api.get_instance(Race, race)

    def load(self):
        """
        CAPTION: All data will be loaded. Take a large amount of time.
        If data has loaded, reload
        """
        self.clear()
        self.__init_list()
        for _ in self:
            pass

    @property
    def have_loaded(self):
        """
        have all race been loaded

        Returns:
            _type_: _description_
        """
        self.__init_list()
        return None in self.__race_cache

    @overload
    def __getitem__(self, item: int) -> Race:
        ...

    @overload
    def __getitem__(self, item: slice) -> tuple[Race]:
        ...

    def __getitem__(self, item):
        self.__init_list()
        match item:
            case int():
                length = len(self)
                if item < -length:
                    raise IndexError()
                elif item < 0:
                    index = length + item
                elif item < length:
                    index = item
                else:
                    raise IndexError()

                with self.__lock:
                    if self.__race_cache[index] is not None:
                        return self.__race_cache[index]
                    else:
                        i_page = index // 10 + 1  # 0-9 => 1, 10-19 => 2, ...
                        json_data = self.__fetch_json(i_page)

                        for i, race in enumerate(json_data["races"]):
                            try:
                                self.__race_cache[(i_page - 1) * 10 + i] = self.__api.get_instance(Race, race)
                            except IndexError:
                                self.__race_cache.append(self.__api.get_instance(Race, race))
                        return self.__race_cache[index]
            case slice():
                start, stop, step = item.indices(len(self))
                return tuple(self[index] for index in range(start, stop, step))

    def __iter__(self):
        self.__init_list()
        i = 0
        while True:
            try:
                yield self[i]
            except IndexError:
                break
            i += 1

    def __contains__(self, key: object) -> bool:
        """
        CAPTION: All data will be loaded. Take a large amount of time.
        """
        if not self.have_loaded:
            self.load()
        return key in self.__race_cache

    def __len__(self):
        self.__init_list()
        return len(self.__race_cache)

    def index(self, value: Race, start: SupportsIndex = 0, stop: SupportsIndex = maxsize) -> int:
        """
        CAPTION: All data will be loaded. Take a large amount of time.
        """
        if not self.have_loaded:
            self.load()
        return self.__race_cache.index(value, start, stop)

    def count(self, value: Race) -> int:
        """
        CAPTION: All data will be loaded. Take a large amount of time.
        """
        if not self.have_loaded:
            self.load()
        return self.__race_cache.count(value)

    def clear(self):
        with self.__lock:
            self.__race_cache = None


@dataclass(frozen=True)
class Goal(object):
    name: str
    custom: bool
