from pyracetimegg import RacetimeGGAPI
from pyracetimegg.object_mapping import APIBase

api = RacetimeGGAPI(request_per_second=3)
api_json = APIBase("https://racetime.gg", 3)


def test_user():
    from pyracetimegg import User

    user = api.fetch_user("xldAMBlqvY3aOP57")
    json_data = api_json.fetch_json("https://racetime.gg/user/xldAMBlqvY3aOP57/data")
    assert user.id == json_data["id"]
    assert user.url == json_data["url"]
    assert user.data_url == json_data["url"] + "/data"
    assert user.name == json_data["name"]
    assert user.discriminator == json_data["discriminator"]
    assert user.full_name == json_data["full_name"]
    assert user.avatar == json_data["avatar"]
    assert user.pronouns == User.Pronouns.NONE
    assert user.flair == json_data["flair"]
    assert user.twitch_name == json_data["twitch_name"]
    assert user.twitch_display_name == json_data["twitch_display_name"]
    assert user.twitch_channel == json_data["twitch_channel"]
    assert user.can_moderate == json_data["can_moderate"]
    assert len(user.teams) == len(json_data["teams"])
    assert user.stats.joined == json_data["stats"]["joined"]
    assert user.stats.first == json_data["stats"]["first"]
    assert user.stats.second == json_data["stats"]["second"]
    assert user.stats.third == json_data["stats"]["third"]
    assert user.stats.forfeits == json_data["stats"]["forfeits"]
    races = user.past_race
    races


def test_pronouns():
    import pytest
    from pyracetimegg import User

    assert User.Pronouns.from_str("other/ask!") is User.Pronouns.OTHER_ASK
    assert User.Pronouns.from_str("he/him") is User.Pronouns.HE_HIM
    with pytest.raises(ValueError):
        User.Pronouns.from_str("hogehoge")
        assert False


def test_category():
    category = api.fetch_category("smw")
    json_data = api_json.fetch_json("https://racetime.gg/smw/data")

    assert category.name == "Super Mario World"
    assert category.short_name == "SMW"
    assert category.slug == "smw"
    assert category.url == "/smw"
    assert category.data_url == "/smw/data"
    assert category.image == "https://racetime.gg/media/Super_Mario_World-285x380.jpg"
    assert category.info == ""
    assert category.streaming_required is False

    assert category.owners[0].id == json_data["owners"][0]["id"]
    assert category.owners[0].name == json_data["owners"][0]["name"]
    assert category.owners[0].flair == json_data["owners"][0]["flair"]

    assert len(category.moderators) == len(json_data["moderators"])
    assert category.moderators[2].id == json_data["moderators"][2]["id"]
    assert category.moderators[2].name == json_data["moderators"][2]["name"]
    assert category.moderators[2].flair == json_data["moderators"][2]["flair"]

    assert len(category.goals) == len(json_data["goals"])
    assert category.goals[0].name == json_data["goals"][0]
    assert category.goals[0].custom is False
    assert category.goals[-1].name == json_data["goals"][-1]
    assert category.goals[-1].custom is False

    assert len(category.current_races) == len(json_data["current_races"])


def test_race():
    from datetime import datetime, timedelta
    from zoneinfo import ZoneInfo

    from pyracetimegg import Race

    race = api.fetch_race("smw", "comic-baby-9383")

    assert race.version == 28
    assert race.name == "smw/comic-baby-9383"
    assert race.status is Race.Status.FINISHED
    assert race.url == "/smw/comic-baby-9383"
    assert race.data_url == "/smw/comic-baby-9383/data"
    assert race.websocket_url == "/ws/race/comic-baby-9383"
    assert race.websocket_bot_url == "/ws/o/bot/comic-baby-9383"
    assert race.websocket_oauth_url == "/ws/o/race/comic-baby-9383"

    assert race.category.slug == "smw"

    assert race.goal.name == "Small Only"
    assert race.goal.custom is False

    assert race.info == ""
    assert race.info_bot is None
    assert race.info_user == ""
    assert race.team_race is False
    assert race.entrants_count == 4
    assert race.entrants_count_finished == 4
    assert race.entrants_count_inactive == 0
    assert race.entrants[0].user.id == "xldAMBlqvY3aOP57"
    assert race.entrants[0].user.full_name == "Nanahuse#2723"
    assert race.entrants[0].team is None
    assert race.entrants[0].status is Race.Entrant.Status.DONE
    assert race.entrants[0].finish_time == timedelta(minutes=17, seconds=13, milliseconds=267)
    assert race.entrants[0].finished_at == datetime(2022, 3, 20, 12, 27, 45, 964, tzinfo=ZoneInfo("UTC"))
    assert race.entrants[0].place == 1
    assert race.entrants[0].place_ordinal == "1st"
    assert race.entrants[0].score is None
    assert race.entrants[0].score_change is None
    assert race.entrants[0].comment is None
    assert race.entrants[0].has_comment is False
    assert race.entrants[0].stream_live is False
    assert race.entrants[0].stream_override is False

    assert race.opened_at == datetime(2022, 3, 20, 11, 50, 38, 7, tzinfo=ZoneInfo("UTC"))
    assert race.start_delay == timedelta(seconds=20)
    assert race.started_at == datetime(2022, 3, 20, 12, 10, 32, 696, tzinfo=ZoneInfo("UTC"))
    assert race.ended_at == datetime(2022, 3, 20, 12, 28, 40, 275, tzinfo=ZoneInfo("UTC"))
    assert race.cancelled_at is None
    assert race.unlisted is False
    assert race.time_limit == timedelta(days=1)
    assert race.time_limit_auto_complete is False
    assert race.require_even_teams is False
    assert race.streaming_required is False
    assert race.auto_start is False

    assert race.opened_by.id == "xldAMBlqvY3aOP57"
    assert race.opened_by.full_name == "Nanahuse#2723"

    assert race.monitors[0].id == "VwLN8B85XK3Pa52R"
    assert race.monitors[0].full_name == "Pesu#1724"

    assert race.recordable is True
    assert race.recorded is False
    assert race.recorded_by is None
    assert race.allow_comments is True
    assert race.hide_comments is False
    assert race.allow_prerace_chat is True
    assert race.allow_midrace_chat is True
    assert race.allow_non_entrant_chat is True
    assert race.chat_message_delay == timedelta(days=0)


def test_pastrace():
    from pyracetimegg import Race

    category = api.fetch_category("smw")
    past_race = category.past_race

    json_data = api_json.fetch_json_from_site("smw/races/data?show_entrants=yes&page=2")
    assert past_race[10].name == json_data["races"][0]["name"]
    assert past_race[10].status is Race.Status.FINISHED
    assert past_race[10].info == json_data["races"][0]["info"]
    assert len(past_race) == json_data["count"]
    races = past_race[:11]
    assert past_race[10].name == races[-1].name


def test_leaderboard():
    leaderboard = api.fetch_category("smw").leaderboard

    json_data = api_json.fetch_json_from_site("smw/leaderboards/data")

    assert leaderboard["11 Exit"][0].place == 1
    assert leaderboard["11 Exit"][0].place_ordinal == "1st"
    assert leaderboard["11 Exit"][0].user.name == json_data["leaderboards"][0]["rankings"][0]["user"]["name"]
