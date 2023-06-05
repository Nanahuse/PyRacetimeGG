# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/PyRacetimeGG/blob/main/LICENSE


def test_fetch_user():
    from pyracetimegg import fetch_user

    user = fetch_user("xldAMBlqvY3aOP57")
    user


def test_fetch_category():
    from pyracetimegg import fetch_category

    category = fetch_category("smw")
    category


def test_fetch_race():
    from pyracetimegg import fetch_race

    race = fetch_race("smw", "comic-baby-9383")
    race


def test_fetch_category_leaderboard():
    from pyracetimegg import fetch_category_leaderboard

    leaderboard = fetch_category_leaderboard("smw")
    leaderboard


def test_fetch_past_user_races():
    import pytest
    from pyracetimegg import fetch_past_user_races

    races = fetch_past_user_races("xldAMBlqvY3aOP57")
    races = fetch_past_user_races("Ek8wpok5wVB5KQyV")
    assert len(fetch_past_user_races("Ek8wpok5wVB5KQyV", 5)) == 5
    with pytest.raises(ValueError):
        races = fetch_past_user_races("wrongID")
    races


def test_fetch_past_user_races_show_entrants():
    import pytest
    from pyracetimegg import fetch_past_user_races_show_entrants

    races = fetch_past_user_races_show_entrants("xldAMBlqvY3aOP57")
    races = fetch_past_user_races_show_entrants("Ek8wpok5wVB5KQyV")
    assert len(fetch_past_user_races_show_entrants("Ek8wpok5wVB5KQyV", 5)) == 5
    with pytest.raises(ValueError):
        races = fetch_past_user_races_show_entrants("wrongID")
    races


def test_fetch_past_category_races():
    import pytest
    from pyracetimegg import fetch_past_category_races

    races = fetch_past_category_races("smw")
    assert len(fetch_past_category_races("smw", 5)) == 5
    with pytest.raises(ValueError):
        races = fetch_past_category_races("wrongID")
    races


def test_fetch_past_category_races_show_entrants():
    import pytest
    from pyracetimegg import fetch_past_category_races_show_entrants

    races = fetch_past_category_races_show_entrants("smw")
    assert len(fetch_past_category_races_show_entrants("smw", 5)) == 5
    with pytest.raises(ValueError):
        races = fetch_past_category_races_show_entrants("wrongID")
    races


def test_serch_user():
    from pyracetimegg import search_user

    results = search_user(name="nanahuse", discriminator="2723")
    user = results[0]
    assert user.id == "xldAMBlqvY3aOP57"
    assert user.full_name == "Nanahuse#2723"


def test_serch_user_by_term():
    from pyracetimegg import search_user_by_term

    results = search_user_by_term("Nanahuse#2723")
    user = results[0]
    assert user.id == "xldAMBlqvY3aOP57"
    assert user.full_name == "Nanahuse#2723"
