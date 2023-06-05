from __future__ import annotations
from abc import ABC, abstractproperty, abstractclassmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum
from pyracetimegg.utils import fetch_json, fetch_image_from_url, joint_url, str2datetime, str2timedelta, place2str


class Pronouns(StrEnum):
    NONE = "none"
    SHE_HER = "she/her"
    HE_HIM = "he/him"
    THEY_THEM = "they/them"
    SHE_THEY = "she/they"
    HE_THEY = "he/they"
    OTHER_ASK = "other/ask!"

    @classmethod
    def from_str(cls, string: str):
        for pronouns in Pronouns:
            if pronouns.value == string:
                return pronouns
        if string is None:
            return Pronouns.NONE
        raise ValueError(string)


@dataclass(frozen=True)
class User(object):
    id: str
    name: str
    discriminator: str
    avatar: str | None  # image_URL
    pronouns: Pronouns
    flair: str
    twitch_name: str
    twitch_display_name: str
    can_moderate: bool
    teams: tuple[str] | None

    @property
    def full_name(self):
        return f"{self.name}#{self.discriminator}"

    @property
    def url(self):
        return f"/user/{self.id}"

    @property
    def data_url(self):
        return f"{self.url}/data"

    @property
    def twitch_channel(self):
        return f"https://www.twitch.tv/{self.twitch_name}"

    def fetch_avatar_image(self):
        """
        fetch avatar image
        if avatar image is not setted, return None

        Returns:
            PIL.Image.Image | None: avatar image or None
        """
        if self.avatar is None:
            return None
        else:
            return fetch_image_from_url(self.avatar)

    def fetch_detail(self, site_url: str = "https://racetime.gg/"):
        """
        fetch detail infomation

        Args:
            site_url (str, optional): if you want to connect a site other than racetime.gg
            Defaults to https://racetime.gg/.

        Returns:
            UserDetail
        """
        return UserDetail.from_json(fetch_json(joint_url(site_url, self.data_url)))

    @classmethod
    def from_json(cls, json_data: dict):
        return User(
            json_data["id"],
            json_data["name"],
            json_data["discriminator"],
            json_data["avatar"],
            Pronouns.from_str(json_data["pronouns"]),
            json_data["flair"],
            json_data["twitch_name"],
            json_data["twitch_display_name"],
            json_data["can_moderate"],
            json_data.get("teams", None),
        )


@dataclass(frozen=True)
class UserDetail(User):
    @dataclass(frozen=True)
    class Stats(object):
        joined: int
        first: int
        second: int
        third: int
        forfeits: int

    stats: Stats | None

    def fetch_detail(self, *, site_url: str = "https://racetime.gg/"):
        """
        Return itself. Because Userdetail is already detailed.

        Args:
            site_url (str, optional): not work

        Returns:
            UserDetail
        """
        return self

    @classmethod
    def from_json(cls, json_data: dict):
        return UserDetail(
            json_data["id"],
            json_data["name"],
            json_data["discriminator"],
            json_data["avatar"],
            Pronouns.from_str(json_data["pronouns"]),
            json_data["flair"],
            json_data["twitch_name"],
            json_data["twitch_display_name"],
            json_data["can_moderate"],
            json_data.get("teams", None),
            UserDetail.Stats(**json_data["stats"]) if "stats" in json_data else None,
        )


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
            for tmp in Entrant.Status:
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
    def from_json(cls, json_data: dict):
        return Entrant(
            User.from_json(json_data["user"]),
            json_data["team"],
            Entrant.Status.from_str(json_data["status"]["value"]),
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


@dataclass(frozen=True)
class LeaderBoardParticipant(object):
    user: User
    place: int
    score: int | None
    best_time: timedelta
    times_raced: int

    @property
    def place_ordinal(self):
        return place2str(self.place)

    @classmethod
    def from_json(cls, json_data: dict):
        return LeaderBoardParticipant(
            User.from_json(json_data["user"]),
            json_data["place"],
            json_data["score"],
            str2timedelta(json_data["best_time"]),
            json_data["times_raced"],
        )


@dataclass(frozen=True)
class Emote(object):
    name: str
    url: str

    def fetch_image(self):
        """
        fetch emote image

        Returns:
            PIL.Image.Image: emote image
        """
        return fetch_image_from_url(self.url)


@dataclass(frozen=True)
class Goal(object):
    name: str
    custom: bool


@dataclass(frozen=True)
class Category(object):
    name: str
    short_name: str
    slug: str
    image: str  # URL

    @property
    def url(self):
        return f"/{self.slug}"

    @property
    def data_url(self):
        return f"{self.url}/data"

    def fetch_image(self):
        """
        fetch category image

        Returns:
            PIL.Image.Image: category image
        """
        return fetch_image_from_url(self.image)

    def fetch_detail(self, site_url: str = "https://racetime.gg/"):
        """
        fetch detail infomation

        Args:
            site_url (str, optional): if you want to connect a site other than racetime.gg, use this argument.
            Defaults to https://racetime.gg/.

        Returns:
            CategoryDetail
        """
        return CategoryDetail.from_json(fetch_json(joint_url(site_url, self.data_url)))

    @classmethod
    def from_json(cls, json_data: dict):
        return Category(**json_data)


@dataclass(frozen=True)
class CategoryDetail(Category):
    info: str  # HTML
    streaming_required: bool
    owners: tuple[User]
    moderators: tuple[User]
    goals: tuple[Goal]
    current_races: tuple[Race]
    emotes: tuple[Emote]

    def fetch_detail(self, site_url: str = "https://racetime.gg/"):
        """
        Return itself. Because Userdetail is already detailed.

        Args:
            site_url (str, optional): not work

        Returns:
            CategoryDetail
        """
        return self

    @classmethod
    def from_json(cls, json_data: dict):
        return CategoryDetail(
            json_data["name"],
            json_data["short_name"],
            json_data["slug"],
            json_data["image"],
            json_data["info"],
            json_data["streaming_required"],
            tuple(User.from_json(user_data) for user_data in json_data["owners"]),
            tuple(User.from_json(user_data) for user_data in json_data["moderators"]),
            tuple(Goal(goal_data, False) for goal_data in json_data["goals"]),
            tuple(Race.from_json(race_data) for race_data in json_data["current_races"]),
            tuple(Emote(emote, url) for emote, url in json_data["emotes"].items()),
        )


@dataclass(frozen=True)
class iRace(ABC):
    class Status(StrEnum):
        OPEN = "open"
        INVITATIONAL = "invitational"
        PENDING = "pending"
        IN_PROGRESS = "in_progress"
        FINISHED = "finished"
        CANCELLED = "cancelled"

        @classmethod
        def from_str(cls, string: str):
            for status in iRace.Status:
                if status.value == string:
                    return status
            raise ValueError(string)

    slug: str
    status: iRace.Status
    goal: Goal
    info: str
    opened_at: datetime
    started_at: datetime | None
    time_limit: timedelta

    @abstractproperty
    def category_slug(self) -> int:
        raise NotImplementedError()

    @property
    def name(self):
        return f"{self.category_slug}/{self.slug}"

    @property
    def url(self):
        return f"/{self.name}"

    @property
    def data_url(self):
        return f"{self.url}/data"

    @abstractproperty
    def entrants_count() -> int:
        raise NotImplementedError()

    @abstractproperty
    def entrants_count_finished() -> int:
        raise NotImplementedError()

    @abstractproperty
    def entrants_count_inactive() -> int:
        raise NotImplementedError()

    @abstractclassmethod
    def from_json(cls, json_data: dict):
        raise NotImplementedError()


@dataclass(frozen=True)
class Race(iRace):
    category_slug_: str
    entrants_count_: int
    entrants_count_finished_: int
    entrants_count_inactive_: int

    @property
    def category_slug(self):
        return self.category_slug_

    @property
    def entrants_count(self):
        return self.entrants_count_

    @property
    def entrants_count_finished(self):
        return self.entrants_count_finished_

    @property
    def entrants_count_inactive(self):
        return self.entrants_count_inactive_

    def fetch_detail(self, site_url: str = "https://racetime.gg/"):
        """
        fetch detail infomation

        Args:
            site_url (str, optional): if you want to connect a site other than racetime.gg, use this argument.
            Defaults to https://racetime.gg/.

        Returns:
            RaceDetail
        """
        return RaceDetail.from_json(fetch_json(joint_url(site_url, self.data_url)))

    @classmethod
    def from_json(cls, json_data: dict):
        category_slug, slug = json_data["name"].split("/")
        return Race(
            slug,
            Race.Status.from_str(json_data["status"]["value"]),
            Goal(**json_data["goal"]),
            json_data["info"],
            str2datetime(json_data["opened_at"]),
            str2datetime(json_data["started_at"]) if json_data["started_at"] is not None else None,
            str2timedelta(json_data["time_limit"]),
            category_slug,
            int(json_data["entrants_count"]),
            int(json_data["entrants_count_finished"]),
            int(json_data["entrants_count_inactive"]),
        )


@dataclass(frozen=True)
class RaceDetail(iRace):
    # Race info (General)
    version: int
    category: Category
    info_bot: str
    info_user: str
    team_race: bool

    @property
    def category_slug(self):
        return self.category.slug

    @property
    def websocket_url(self):
        return f"/ws/race/{self.slug}"

    @property
    def websocket_bot_url(self):
        return f"/ws/o/bot/{self.slug}"

    @property
    def websocket_oauth_url(self):
        return f"/ws/o/race/{self.slug}"

    # Race info (Time)
    # opened_at: datetime
    opened_by: User
    start_delay: timedelta
    # started_at: datetime | None
    ended_at: datetime | None
    cancelled_at: datetime | None
    unlisted: bool  # hidden from category view except for moderators
    # Race Option
    # time_limit: timedelta
    time_limit_auto_complete: bool
    require_even_teams: bool
    streaming_required: bool
    auto_start: bool
    recordable: bool
    recorded: bool
    recorded_by: User | None
    allow_comments: bool
    hide_comments: bool
    allow_prerace_chat: bool
    allow_midrace_chat: bool
    allow_non_entrant_chat: bool
    chat_message_delay: timedelta

    # People
    monitors: tuple[User]
    entrants: tuple[Entrant]

    @property
    def entrants_count(self):
        return len(self.entrants)

    @property
    def entrants_count_finished(self):
        return len(tuple(tmp for tmp in self.entrants if tmp.status is Entrant.Status.DONE))

    @property
    def entrants_count_inactive(self):
        return len(tuple(tmp for tmp in self.entrants if (tmp is Entrant.Status.DQ) | (tmp is Entrant.Status.DNF)))

    @classmethod
    def from_json(cls, json_data: dict):
        return RaceDetail(
            json_data["slug"],
            Race.Status.from_str(json_data["status"]["value"]),
            Goal(**json_data["goal"]),
            json_data["info"],
            str2datetime(json_data["opened_at"]),
            str2datetime(json_data["started_at"]) if json_data["started_at"] is not None else None,
            str2timedelta(json_data["time_limit"]),
            json_data["version"],
            Category(
                json_data["category"]["name"],
                json_data["category"]["short_name"],
                json_data["category"]["slug"],
                json_data["category"]["image"],
            ),
            json_data["info_bot"],
            json_data["info_user"],
            json_data["team_race"],
            User.from_json(json_data["opened_by"]),
            str2timedelta(json_data["start_delay"]),
            str2datetime(json_data["ended_at"]) if json_data["ended_at"] is not None else None,
            str2datetime(json_data["cancelled_at"]) if json_data["cancelled_at"] is not None else None,
            json_data["unlisted"],
            json_data["time_limit_auto_complete"],
            json_data["require_even_teams"],
            json_data["streaming_required"],
            json_data["auto_start"],
            json_data["recordable"],
            json_data["recorded"],
            User.from_json(json_data["recorded_by"]) if json_data["recorded_by"] is not None else None,
            json_data["allow_comments"],
            json_data["hide_comments"],
            json_data["allow_prerace_chat"],
            json_data["allow_midrace_chat"],
            json_data["allow_non_entrant_chat"],
            str2timedelta(json_data["chat_message_delay"]),
            tuple(User.from_json(user_data) for user_data in json_data["monitors"]),
            tuple(Entrant.from_json(user_data) for user_data in json_data["entrants"]),
        )


@dataclass(frozen=True)
class RaceWithEntrants(object):
    race: Race
    entrants: tuple[Entrant]
