# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/PyRacetimeGG/blob/main/LICENSE

import re
from typing import overload
from pyracetimegg.object_mapping import APIBase


class RacetimeGGAPI(object):
    def __init__(self, site_url: str = "https://racetime.gg/", request_per_second: int = 1) -> None:
        self.__api = APIBase(site_url, request_per_second)

    def search_user(self, *, name: str | None = None, discriminator: str | None = None):
        """
        search user by name or discriminator
        https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints#user-search

        Args:
            name (str | None, optional):
                user's name. head-match. case insensitive
                Defaults to None.
            discriminator (str | None, optional):
                4 digits discriminator. e.g. '0844'. Exact match only.
                Defaults to None.
        Returns:
            User
        """
        from pyracetimegg.objects.user import User

        if discriminator is not None:
            if not re.match("[0-9][0-9][0-9][0-9]", discriminator):
                ValueError("discriminator should be a set of four digits, e.g. '0844'")

        match name, discriminator:
            case str(), str():
                query = f"name={name}&discriminator={discriminator}"
            case str(), None:
                query = f"name={name}"
            case None, str():
                query = f"discriminator={discriminator}"
            case _:
                ValueError("must be set name or discriminator")

        json_data = self.__api.fetch_json_from_site(f"user/search?{query}")
        return tuple(User._load_from_json(self.__api, tmp) for tmp in json_data["results"])

    def search_user_by_term(self, term: str):
        """
        serch user by name or partial name or (name and discriminator)

        https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints#user-search

        Args:
            term (str): term
            site_url (user, optional):
                if you want to connect a site other than racetime.gg
                Defaults to https://racetime.gg/.
        Returns:
            User
        """
        from pyracetimegg.objects.user import User

        json_data = self.__api.fetch_json_from_site(f"user/search?term={term}")
        return tuple(User._load_from_json(self.__api, tmp) for tmp in json_data["results"])

    def fetch_all_races(self):
        """
        all open and ongoing races

        https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints#all-races
        """
        from pyracetimegg.objects.race import Race

        json_data = self.__api.fetch_json_from_site("races/data")
        return tuple(Race._load_from_json(self.__api, tmp) for tmp in json_data["races"])

    def fetch_user(self, user_id: str):
        """
        https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints#url-fields

        Args:
            user_id (str): you can find at URL
        """
        from pyracetimegg.objects.user import User

        user: User = self.__api.get_instance(User, user_id)
        user.load("name")
        return user

    def fetch_category(self, category_slug: str):
        """
        https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints#category-detail

        Args:
            category_slug (str): you can find at URL
        """
        from pyracetimegg.objects.category import Category

        category: Category = self.__api.get_instance(Category, category_slug)
        category.load("name")
        return category

    @overload
    def fetch_race(self, race_name: str):
        """
        https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints#race-detail

        Args:
            race_name (str): you can find at URL.  it looks like xxx/xxx-xxx-xxx
        """
        ...

    @overload
    def fetch_race(self, category_slug: str, race_slug: str):
        """
        https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints#race-detail

        Args:
            category_slug (str): you can find at URL.
            race_slug (str): you can find at URL. it looks like xxx-xxx-xxx
        """
        ...

    def fetch_race(self, *args):
        from pyracetimegg.objects.race import Race

        match len(args):
            case 1:
                if not re.fullmatch("[0-9a-z-]+/[a-z]+-[a-z]+-[0-9]+", args[0]):
                    ValueError(
                        """race_name is wrong. it looks like xxx/xxx-xxx-xxx.
                        Plese check https://github.com/Nanahuse/PyRacetimeGG#how-to-know-category-slug"""
                    )
                name = args[0]
            case 2:
                if not re.fullmatch("[0-9a-z-]+", args[0]):
                    ValueError(
                        """category_slug is something wrong.
                        Plese check https://github.com/Nanahuse/PyRacetimeGG#how-to-know-category-slug"""
                    )
                if re.fullmatch("[a-z]+-[a-z]+-[0-9]+", args[1]):
                    ValueError(
                        """race_slug is something wrong.
                        Please check https://github.com/Nanahuse/PyRacetimeGG#how-to-know-race-slug"""
                    )
                name = f"{args[0]}/{args[1]}"
            case _:
                raise ValueError("args shuld be one or two")

        race: Race = self.__api.get_instance(Race, name)
        race.load("slug")
        return race

    def fetch_by_url(self, url: str):
        if re.fullmatch(self.__api.get_url("user", "[0-9a-zA-Z]+"), url):
            return self.fetch_user(url.split("/")[-1])
        elif re.fullmatch(self.__api.get_url("[0-9a-z-]+"), url):
            return self.fetch_category(url.split("/")[-1])
        elif re.fullmatch(self.__api.get_url("[0-9a-z-]+/[a-z]+-[a-z]+-[0-9]+"), url):
            category_slug, race_slug = url.split("/")[-2:]
            return self.fetch_race(category_slug, race_slug)
        else:
            raise ValueError(f"wrong url: url={url}")
