# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/PyRacetimeGG/blob/main/LICENSE


from pyracetimegg.api import RacetimeGGAPI

api = RacetimeGGAPI()


def test_search_user():
    user = api.search_user(name="Nanahuse", discriminator="2723")[0]
    assert user.name == "Nanahuse"


def test_search_user_by_term():
    user = api.search_user_by_term("Nanahuse#2723")[0]
    assert user.name == "Nanahuse"


def test_fetch_all_races():
    race = api.fetch_all_races()
    race


def test_fetch_user():
    user = api.fetch_user("xldAMBlqvY3aOP57")
    assert user.name == "Nanahuse"


def test_fetch_category():
    category = api.fetch_category("smw")
    assert category.name == "Super Mario World"


def test_fetch_race():
    race = api.fetch_race("smw/comic-baby-9383")
    assert race.goal.name == "Small Only"
    race2 = api.fetch_race("smw", "comic-baby-9383")  # overload method
    assert race == race2
    race3 = api.fetch_race("smw", "mega-dupe-1280")  # overload method
    assert race != race3


def test_fetch_by_url():
    test_user = api.fetch_user_by_url("https://racetime.gg/user/xldAMBlqvY3aOP57")
    user = api.fetch_user("xldAMBlqvY3aOP57")
    assert test_user == user

    test_category = api.fetch_category_by_url("https://racetime.gg/smw")
    category = api.fetch_category("smw")
    assert test_category == category

    test_race = api.fetch_race_by_url("https://racetime.gg/smw/comic-baby-9383")
    race = api.fetch_race("smw/comic-baby-9383")
    assert test_race == race
