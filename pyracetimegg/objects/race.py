# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/PyRacetimeGG/blob/main/LICENSE

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum
from inspect import currentframe
from typing import Any, Sequence, overload, TYPE_CHECKING
from sys import maxsize
from pyracetimegg.object_mapping import iObject, TAG
from pyracetimegg.utils import str2datetime, str2timedelta, place2str

if TYPE_CHECKING:
    from typing_extensions import SupportsIndex
    from pyracetimegg.object_mapping import APIBase
    from pyracetimegg.objects.user import User
    from pyracetimegg.objects.category import Category


class Race(iObject):
    class Status(StrEnum):
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
        class Status(StrEnum):
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
                User._load_from_json(api, json_data["user"]),
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
        return f"/{self.name}"

    @property
    def data_url(self):
        return f"{self.url}/data"

    @property
    def websocket_url(self):
        return f"/ws/race/{self.slug}"

    @property
    def websocket_bot_url(self):
        return f"/ws/o/bot/{self.slug}"

    @property
    def websocket_oauth_url(self):
        return f"/ws/o/race/{self.slug}"

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

    def _fetch_from_api(self, tag: TAG):
        json_data = self._api.fetch_json_from_site(self.data_url)
        self._load_from_json(self._api, json_data)
        return self._get(tag)

    def _load_all(self):
        self._fetch_from_api("category")

    @classmethod
    def _load_from_json(cls, api: APIBase, json_: dict[TAG, Any]) -> Race:
        from pyracetimegg.objects.user import User
        from pyracetimegg.objects.category import Category

        output = dict()
        id = json_["name"]
        category_slug, slug = id.split("/")
        json_.setdefault("category", {"slug": category_slug})
        json_["slug"] = slug

        for key, value in json_.items():
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
                    output[key] = Category._load_from_json(api, value)
                case "opened_by" | "recorded_by":
                    if value is None:
                        output[key] = None
                    else:
                        output[key] = User._load_from_json(api, value)
                case "monitors":
                    output[key] = tuple(User._load_from_json(api, tmp) for tmp in value)
                case "entrants":
                    output[key] = tuple(Race.Entrant.from_json(api, tmp) for tmp in value)
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

        return api.store_data(Race, id, output)


class PastRaces(Sequence[Race]):
    def __init__(self, obj: Category | User) -> None:
        from pyracetimegg.objects.user import User
        from pyracetimegg.objects.category import Category

        self._api = obj._api
        match obj:
            case Category():
                self._base_path = obj.slug
            case User():
                self._base_path = f"user/{obj.id}"
            case _:
                raise ValueError()

        json_data = self._fetch_json(1)

        self._race_cache: list[Race | None] = [None] * json_data["count"]

        for i, race in enumerate(json_data["races"]):
            self._race_cache[i] = Race._load_from_json(self._api, race)

    def _fetch_json(self, page_num: int):
        return self._api.fetch_json_from_site(self._base_path, f"races/data?show_entrants=yes&page={page_num}")

    def load(self):
        """
        CAPTION: All data will be loaded. Take a large amount of time.
        """
        for _ in self:
            pass

    @property
    def is_loaded(self):
        return None in self._race_cache

    @overload
    def __getitem__(self, item: int) -> Race:
        ...

    @overload
    def __getitem__(self, item: slice) -> tuple[Race]:
        ...

    def __getitem__(self, item):
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

                if self._race_cache[index] is not None:
                    return self._race_cache[index]
                else:
                    i_page = index // 10 + 1  # 0-9 => 1, 10-19 => 2, ...
                    json_data = self._fetch_json(i_page)

                    for i, race in enumerate(json_data["races"]):
                        self._race_cache[(i_page - 1) * 10 + i] = Race._load_from_json(self._api, race)
                    return self._race_cache[index]
            case slice():
                start, stop, step = item.indices(len(self))
                return tuple(self[index] for index in range(start, stop, step))

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

    def __contains__(self, key: object) -> bool:
        """
        CAPTION: All data will be loaded. Take a large amount of time.
        """
        if not self.is_loaded:
            self.load()
        return key in self._race_cache

    def __len__(self):
        return len(self._race_cache)

    def index(self, value: Race, start: SupportsIndex = 0, stop: SupportsIndex = maxsize) -> int:
        """
        CAPTION: All data will be loaded. Take a large amount of time.
        """
        if not self.is_loaded:
            self.load()
        return self._race_cache.index(value, start, stop)

    def count(self, value: Race) -> int:
        """
        CAPTION: All data will be loaded. Take a large amount of time.
        """
        if not self.is_loaded:
            self.load()
        return self._race_cache.count(value)


@dataclass(frozen=True)
class Goal(object):
    name: str
    custom: bool
