# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/PyRacetimeGG/blob/main/LICENSE

from json import JSONDecodeError
import re
from pyracetimegg.objects import (
    User,
    UserDetail,
    Entrant,
    Race,
    RaceDetail,
    RaceWithEntrants,
    Category,
    CategoryDetail,
    LeaderBoardParticipant,
)
from pyracetimegg.utils import fetch_json, joint_url


def fetch_user(user_id: str, *, site_url: str = "https://racetime.gg/"):
    """
    fetch user data from user_id

    Args:
        user_id (str):
        site_url (str, optional):
            if you want to connect a site other than racetime.gg
            Defaults to https://racetime.gg/.
    Returns:
        UserDetail
    """
    url = joint_url(site_url, "user", user_id, "data")
    try:
        json_data = fetch_json(url)
        return UserDetail.from_json(json_data)
    except JSONDecodeError:
        return None


def fetch_category(category_slug: str, *, site_url: str = "https://racetime.gg/"):
    """
    fetch a category by category_slug.
    https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints#category-detail

    Args:
        category_slug (str):
        site_url (str, optional):
            if you want to connect a site other than racetime.gg
            Defaults to https://racetime.gg/.
    Returns:
        CategoryDetail
    """
    url = joint_url(site_url, category_slug, "data")
    try:
        json_data = fetch_json(url)
        return CategoryDetail.from_json(json_data)
    except JSONDecodeError:
        return None


def fetch_race(category_slug: str, race_slug: str, *, site_url: str = "https://racetime.gg/"):
    """
    fetch a race by category_slug and race_slug.
    https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints#race-detail

    Args:
        category_slug (str):
        race_slug (str):
        site_url (str, optional):
            if you want to connect a site other than racetime.gg
            Defaults to https://racetime.gg/.
    Returns:
        CategoryDetail
    """
    url = joint_url(site_url, category_slug, race_slug, "data")
    try:
        json_data = fetch_json(url)
        return RaceDetail.from_json(json_data)
    except JSONDecodeError:
        return None


def fetch_category_leaderboard(
    category: Category | str, *, site_url: str = "https://racetime.gg/"
) -> dict[str, tuple[LeaderBoardParticipant]]:
    """
    fetch a list of category's leaderboard.
    https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints#category-leaderboards

    Args:
        category (Category|CategoryDetail|str):
        site_url (str, optional):
            if you want to connect a site other than racetime.gg
            Defaults to https://racetime.gg/.
    Returns:
        dict[str,tuple[LeaderBoardParticipant]] key->goal_name
    """

    match category:
        case Category():
            slug = category.slug
        case str():
            slug = category
        case _:
            raise ValueError("category must be Category | CategoryDetail | str(slug)")

    url = joint_url(site_url, slug, "leaderboards/data")
    try:
        json_data = fetch_json(url)
    except JSONDecodeError:
        raise ValueError("cagegory slug should be wrong")

    leaderboards = dict()

    for leaderboard in json_data["leaderboards"]:
        goal_name = leaderboard["goal"]
        ranking = tuple(LeaderBoardParticipant.from_json(participant) for participant in leaderboard["rankings"])

        leaderboards[goal_name] = ranking
    return leaderboards


def _fetch_past_races(url_base: str, limit_num: int):
    i_race = 0
    i_page = 1
    flag = True
    while flag:
        url = f"{url_base}page={i_page}"
        try:
            json_data = fetch_json(url)
        except JSONDecodeError:
            raise ValueError()
        for race_json in json_data["races"]:
            yield race_json
            i_race += 1
            if i_race == limit_num:
                flag = False
                break
        if i_page == json_data["num_pages"]:
            flag = False
        else:
            i_page += 1


def fetch_past_user_races(user: User | str, limit_num: int = 100, *, site_url: str = "https://racetime.gg/"):
    """
    fetch a list of all finished races that the user paticipated in.
    https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints#past-user-races

    Args:
        user (User|str): user:User or user_id:str
        site_url (str, optional):
            if you want to connect a site other than racetime.gg
            Defaults to https://racetime.gg/.
    Returns:
        tuple[Race]
    """
    if (not isinstance(limit_num, int)) & (limit_num <= 0):
        ValueError("limit_num must be int & >0")

    match user:
        case User():
            user_id = user.id
        case str():
            user_id = user

    url = joint_url(site_url, "user", user_id, "/races/data?")
    return tuple(Race.from_json(race_json) for race_json in _fetch_past_races(url, limit_num))


def fetch_past_user_races_show_entrants(
    user: User | str, limit_num: int = 100, *, site_url: str = "https://racetime.gg/"
):
    """
    fetch a list of all finished races that the user paticipated in.
    https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints#past-user-races

    Args:
        user (User|str): user:User or user_id:str
        site_url (str, optional):
            if you want to connect a site other than racetime.gg
            Defaults to https://racetime.gg/.
    Returns:
        tuple[Race]
    """
    if (not isinstance(limit_num, int)) & (limit_num <= 0):
        ValueError("limit_num must be int & >0")

    match user:
        case User():
            user_id = user.id
        case str():
            user_id = user

    url = joint_url(site_url, "user", user_id, "/races/data?show_entrants=yes&")
    return tuple(
        RaceWithEntrants(
            Race.from_json(race_json), tuple(Entrant.from_json(entrants) for entrants in race_json["entrants"])
        )
        for race_json in _fetch_past_races(url, limit_num)
    )


def fetch_past_category_races(category: Category | str, limit_num: int = 50, *, site_url: str = "https://racetime.gg/"):
    """
    fetch a list of all finished category's races.
    https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints#past-user-races

    Args:
        category (Category|str):
        liit_num (int): fetch rase number limit
        site_url (str, optional):
            if you want to connect a site other than racetime.gg
            Defaults to https://racetime.gg/.
    Returns:
        tuple[RaceOutline]
    """
    if (not isinstance(limit_num, int)) & (limit_num <= 0):
        ValueError("limit_num must be int & >0")

    match category:
        case Category():
            category_slug = category.slug
        case str():
            category_slug = category
        case _:
            raise ValueError("category must be Category | str(slug)")

    url = joint_url(site_url, category_slug, "/races/data?")
    return tuple(Race.from_json(race_json) for race_json in _fetch_past_races(url, limit_num))


def fetch_past_category_races_show_entrants(
    category: Category | str, limit_num: int = 50, *, site_url: str = "https://racetime.gg/"
):
    """
    fetch a list of all finished category's races.
    https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints#past-user-races

    Args:
        category (Category|str):
        liit_num (int): fetch rase number limit
        site_url (str, optional):
            if you want to connect a site other than racetime.gg
            Defaults to https://racetime.gg/.
    Returns:
        tuple[RaceOutline]
    """
    if (not isinstance(limit_num, int)) & (limit_num <= 0):
        ValueError("limit_num must be int & >0")

    match category:
        case Category():
            category_slug = category.slug
        case str():
            category_slug = category
        case _:
            raise ValueError("category must be Category | str(slug)")

    url = joint_url(site_url, category_slug, "/races/data?show_entrants=yes&")
    return tuple(
        RaceWithEntrants(
            Race.from_json(race_json), tuple(Entrant.from_json(entrants) for entrants in race_json["entrants"])
        )
        for race_json in _fetch_past_races(url, limit_num)
    )


def search_user(*, name: str | None = None, discriminator: str | None = None, site_url: str = "https://racetime.gg/"):
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
        site_url (str, optional):
            if you want to connect a site other than racetime.gg
            Defaults to https://racetime.gg/.

    Returns:
        User
    """
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

    url = joint_url(site_url, f"user/search?{query}")
    json_data = fetch_json(url)
    return tuple(User.from_json(tmp) for tmp in json_data["results"])


def search_user_by_term(term: str, *, site_url: str = "https://racetime.gg/"):
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
    url = joint_url(site_url, f"user/search?term={term}")
    json_data = fetch_json(url)
    return tuple(User.from_json(tmp) for tmp in json_data["results"])
