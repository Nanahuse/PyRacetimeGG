import pytest


def test_pronouns():
    from pyracetimegg import Pronouns

    assert Pronouns.from_str("other/ask!") is Pronouns.OTHER_ASK
    assert Pronouns.from_str("he/him") is Pronouns.HE_HIM
    with pytest.raises(ValueError):
        Pronouns.from_str("hogehoge")
        assert False


def test_user():
    import json
    from pyracetimegg import UserDetail, Pronouns

    with open("./test/json/user.json") as f:
        data = json.load(f)
    user = UserDetail.from_json(data)

    assert user.id == "xldAMBlqvY3aOP57"
    assert user.full_name == "Nanahuse#2723"
    assert user.name == "Nanahuse"
    assert user.discriminator == "2723"
    assert user.url == "/user/xldAMBlqvY3aOP57"
    assert user.avatar == "https://racetime.gg/media/icon_SbcOLiM.png"
    assert user.pronouns == Pronouns.NONE
    assert user.flair == ""
    assert user.twitch_name == "nanahuse"
    assert user.twitch_display_name == "七伏"
    assert user.twitch_channel == "https://www.twitch.tv/nanahuse"
    assert user.can_moderate is False
    assert user.stats.joined == 3
    assert user.stats.first == 1
    assert user.stats.second == 0
    assert user.stats.third == 1
    assert user.stats.forfeits == 1
    assert len(user.teams) == 0
    user.fetch_avatar_image().save("test/image/avatar0.png")


def test_leaderboard_paticipant():
    from datetime import timedelta
    import json
    from pyracetimegg import LeaderBoardParticipant

    with open("./test/json/leaderboard_paticipant.json") as f:
        data = json.load(f)
    participant = LeaderBoardParticipant.from_json(data)

    assert participant.user.id == "NZ1KRBObA5W4qAyj"
    assert participant.user.full_name == "hami#4073"
    assert participant.place == 7
    assert participant.place_ordinal == "7th"
    assert participant.score == 1517
    assert participant.best_time == timedelta(minutes=23, seconds=19, milliseconds=293)
    assert participant.times_raced == 3


def test_category():
    from datetime import datetime, timedelta
    import json
    from zoneinfo import ZoneInfo
    from pyracetimegg import CategoryDetail, Race, Pronouns

    with open("./test/json/category.json") as f:
        data = json.load(f)
    category = CategoryDetail.from_json(data)

    assert category.name == "Super Mario World"
    assert category.short_name == "SMW"
    assert category.slug == "smw"
    assert category.url == "/smw"
    assert category.data_url == "/smw/data"
    assert category.image == "https://racetime.gg/media/Super_Mario_World-285x380.jpg"
    assert category.info == ""
    assert category.streaming_required is False

    assert category.owners[0].id == "pRbOXG3yAY3ZVKq1"
    assert category.owners[0].full_name == "Umari0#9772"
    assert category.owners[0].avatar is None
    assert category.owners[0].pronouns is Pronouns.HE_HIM
    assert category.owners[0].flair == "moderator"

    assert len(category.moderators) == 5
    assert category.moderators[4].id == "jb8GPMWw6eo1nEk0"
    assert category.moderators[4].full_name == "WKerrick#7319"
    assert category.moderators[4].avatar is None
    assert category.moderators[4].pronouns == Pronouns.NONE
    assert category.moderators[4].flair == "moderator"

    assert len(category.goals) == 10
    assert category.goals[0].name == "11 Exit"
    assert category.goals[0].custom is False
    assert category.goals[-1].name == "Small Only"
    assert category.goals[-1].custom is False

    assert category.current_races[0].name == "smw/comic-baby-9383"
    assert category.current_races[0].status is Race.Status.FINISHED
    assert category.current_races[0].goal.name == "Small Only"
    assert category.current_races[0].goal.custom is False
    assert category.current_races[0].entrants_count == 4
    assert category.current_races[0].entrants_count_finished == 4
    assert category.current_races[0].entrants_count_inactive == 0
    assert category.current_races[0].opened_at == datetime(2022, 3, 20, 11, 50, 38, 7, tzinfo=ZoneInfo("UTC"))
    assert category.current_races[0].started_at is None
    assert category.current_races[0].time_limit == timedelta(days=1)

    tmp = category.current_races[0].fetch_detail()
    tmp


def test_race():
    from datetime import datetime, timedelta
    import json
    from zoneinfo import ZoneInfo
    from pyracetimegg import Entrant, RaceDetail, Race

    with open("./test/json/race.json") as f:
        data = json.load(f)
    race = RaceDetail.from_json(data)

    assert race.version == 28
    assert race.name == "smw/comic-baby-9383"
    assert race.status is Race.Status.FINISHED
    assert race.url == "/smw/comic-baby-9383"
    assert race.data_url == "/smw/comic-baby-9383/data"
    assert race.websocket_url == "/ws/race/comic-baby-9383"
    assert race.websocket_bot_url == "/ws/o/bot/comic-baby-9383"
    assert race.websocket_oauth_url == "/ws/o/race/comic-baby-9383"

    assert race.category.name == "Super Mario World"
    assert race.category.short_name == "SMW"
    assert race.category.slug == "smw"
    assert race.category.url == "/smw"
    assert race.category.data_url == "/smw/data"
    assert race.category.image == "https://racetime.gg/media/Super_Mario_World-285x380.jpg"

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
    assert race.entrants[0].status is Entrant.Status.DONE
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

    tmp = race.category.fetch_detail()
    tmp = race.opened_by.fetch_detail()
    tmp
