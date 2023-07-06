# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/PyRacetimeGG/blob/main/LICENSE

from __future__ import annotations
from dataclasses import dataclass
from datetime import timedelta
from inspect import currentframe
from typing import TYPE_CHECKING
from pyracetimegg.object_mapping import APIBase, iObject, ID, TAG, DATA
from pyracetimegg.utils import str2timedelta, place2str

if TYPE_CHECKING:
    from pyracetimegg.objects.user import User
    from pyracetimegg.objects.race import Race, PastRaces, Goal


class Category(iObject):
    @property
    def slug(self) -> str:
        return self.id

    @property
    def name(self) -> str:
        return self._get(currentframe().f_code.co_name)

    @property
    def short_name(self) -> str:
        return self._get(currentframe().f_code.co_name)

    @property
    def url(self):
        return self._api.get_url(self.slug)

    @property
    def data_url(self):
        return f"{self.url}/data"

    @property
    def image(self) -> str:
        return self._get(currentframe().f_code.co_name)

    def fetch_image(self):
        return self._api.fetch_image_from_url(self.image)

    @property
    def info(self) -> str:
        return self._get(currentframe().f_code.co_name)

    @property
    def streaming_required(self) -> bool:
        return self._get(currentframe().f_code.co_name)

    @property
    def owners(self) -> tuple[User]:
        return self._get(currentframe().f_code.co_name)

    @property
    def moderators(self) -> tuple[User]:
        return self._get(currentframe().f_code.co_name)

    @property
    def goals(self) -> tuple[Goal]:
        return self._get(currentframe().f_code.co_name)

    @property
    def current_races(self) -> tuple[Race]:
        return self._get(currentframe().f_code.co_name)

    @property
    def emotes(self) -> tuple[Emote]:
        return self._get(currentframe().f_code.co_name)

    @property
    def past_race(self) -> PastRaces:
        return self._get(currentframe().f_code.co_name)

    @property
    def leaderboard(self) -> dict[str, tuple[LeaderBoardParticipant]]:
        return self._get(currentframe().f_code.co_name)

    def load_all(self):
        self.load(("past_race", "leaderboard", "id"))

    def _fetch_from_api(self, tag: TAG) -> DATA:
        from pyracetimegg.objects.category import LeaderBoardParticipant

        match tag:
            case "past_race":
                from pyracetimegg.objects.race import PastRaces

                return {"past_race": PastRaces(self)}
            case "leaderboard":
                json_data = self._api.fetch_json(f"{self.url}/leaderboards/data")
                leaderboards = dict()
                for leaderboard in json_data["leaderboards"]:
                    goal_name = leaderboard["goal"]
                    leaderboards[goal_name] = tuple(
                        LeaderBoardParticipant.from_json(self._api, participant)
                        for participant in leaderboard["rankings"]
                    )
                return {"leaderboard": leaderboards}
            case _:
                json_data = self._api.fetch_json(self.data_url)
                _, data = self._format_api_data(json_data)
                return data

    def _format_api_data(self, data_from_api: dict) -> tuple[ID, DATA]:
        from pyracetimegg.objects.race import Race, Goal
        from pyracetimegg.objects.user import User

        id = data_from_api["slug"]
        output = dict()
        for key, value in data_from_api.items():
            match key:
                case "owners" | "moderators":
                    output[key] = tuple(self._api.get_instance(User, tmp) for tmp in value)
                case "goals":
                    output[key] = tuple(Goal(goal, False) for goal in value)
                case "current_races":
                    output[key] = tuple(self._api.get_instance(Race, race) for race in value)
                case "emotes":
                    output[key] = tuple(Emote(emote, url, self._api) for emote, url in value.items())
                case "current_races":
                    output[key] = tuple(self._api.get_instance(Race, tmp) for tmp in value)
                case _:
                    if key in ("name", "short_name", "image", "info", "streaming_required"):
                        output[key] = value
        return id, output


@dataclass(frozen=True)
class Emote(iObject):
    name: str
    url: str
    _api: APIBase

    def fetch_image(self):
        """
        fetch emote image

        Returns:
            PIL.Image.Image: emote image
        """
        return self._api.fetch_image_from_url(self.url)


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
    def from_json(cls, api: APIBase, json_data: dict):
        from pyracetimegg.objects.user import User

        return LeaderBoardParticipant(
            api.get_instance(User, json_data["user"]),
            json_data["place"],
            json_data["score"],
            str2timedelta(json_data["best_time"]),
            json_data["times_raced"],
        )
