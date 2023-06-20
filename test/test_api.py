# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/PyRacetimeGG/blob/main/LICENSE


from pyracetimegg import RacetimeGGAPI

api = RacetimeGGAPI(request_per_second=3)


def test_site_url():
    assert api.site_url == "https://racetime.gg/"


def test_search_user():
    user = api.search_user(name="Nanahuse", discriminator="2723")[0]
    assert user.name == "Nanahuse"


def test_search_user_by_term():
    user = api.search_user_by_term("Nanahuse#2723")[0]
    assert user.name == "Nanahuse"
