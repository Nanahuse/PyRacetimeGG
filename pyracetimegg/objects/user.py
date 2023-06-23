# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/PyRacetimeGG/blob/main/LICENSE

from __future__ import annotations
from dataclasses import dataclass
from enum import StrEnum
from inspect import currentframe
from PIL.Image import Image
from typing import Any, TYPE_CHECKING
from pyracetimegg.object_mapping import iObject, TAG

if TYPE_CHECKING:
    from pyracetimegg.object_mapping import APIBase
    from pyracetimegg.objects.race import PastRaces


class User(iObject):
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
            for pronouns in User.Pronouns:
                if pronouns.value == string:
                    return pronouns
            if string is None:
                return User.Pronouns.NONE
            raise ValueError(string)

    @dataclass(frozen=True)
    class _Stats(object):
        joined: int = 0
        first: int = 0
        second: int = 0
        third: int = 0
        forfeits: int = 0

    @property
    def url(self):
        return f"/user/{self.id}"

    @property
    def data_url(self):
        return f"{self.url}/data"

    @property
    def name(self) -> str:
        return self._get(currentframe().f_code.co_name)

    @property
    def discriminator(self) -> str:
        return self._get(currentframe().f_code.co_name)

    @property
    def full_name(self):
        return f"{self.name}#{self.discriminator}"

    @property
    def avatar(self) -> str:
        return self._get(currentframe().f_code.co_name)

    def fetch_avatar_image(self) -> Image:
        return self._api.fetch_image_from_url(self.avatar)

    @property
    def pronouns(self) -> str:
        return self._get(currentframe().f_code.co_name)

    @property
    def flair(self) -> str:
        return self._get(currentframe().f_code.co_name)

    @property
    def twitch_name(self) -> str:
        return self._get(currentframe().f_code.co_name)

    @property
    def twitch_channel(self):
        return f"https://www.twitch.tv/{self.twitch_name}"

    @property
    def twitch_display_name(self) -> str:
        return self._get(currentframe().f_code.co_name)

    @property
    def can_moderate(self) -> bool:
        return self._get(currentframe().f_code.co_name)

    @property
    def teams(self) -> tuple[str]:
        return self._get(currentframe().f_code.co_name)

    @property
    def stats(self) -> _Stats:
        return self._get(currentframe().f_code.co_name)

    @property
    def past_race(self) -> PastRaces:
        return self._get(currentframe().f_code.co_name)

    def _fetch_from_api(self, tag: TAG):
        match tag:
            case "past_race":
                from pyracetimegg.objects.race import PastRaces

                self._api.store_data(User, self.id, {"past_race": PastRaces(self)})
                return self._get(tag)
            case _:
                json_data = self._api.fetch_json_from_site(self.data_url)
                json_data.setdefault("stats", None)
                self._load_from_json(self._api, json_data)
                return self._get(tag)

    def _load_all(self):
        self._fetch_from_api("past_race")
        self._fetch_from_api("id")

    @classmethod
    def _load_from_json(cls, api: APIBase, json_: dict[TAG, Any]) -> User:
        output = dict()
        for key, value in json_.items():
            match key:
                case "pronouns":
                    output[key] = User.Pronouns.from_str(value)
                case "teams":
                    output[key] = tuple(tmp for tmp in value) if value is not None else tuple()
                case "stats":
                    output[key] = User._Stats(**value) if value is not None else User._Stats()
                case _:
                    if key in (
                        "name",
                        "discriminator",
                        "avatar",
                        "flair",
                        "twitch_name",
                        "twitch_display_name",
                        "can_moderate",
                    ):
                        output[key] = value
        return api.store_data(User, json_["id"], output)
