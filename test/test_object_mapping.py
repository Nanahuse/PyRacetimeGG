# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/PyRacetimeGG/blob/main/LICENSE


def test_throtledrequest():
    from pyracetimegg.object_mapping import ThrottledRequest
    from time import time

    request_per_second = 3
    url = "https://raw.githubusercontent.com/Nanahuse/PyRacetimeGG/main/LICENSE"

    api = ThrottledRequest(request_per_second)

    api.get(url)
    start_time = time()
    for _ in range(request_per_second):
        api.get(url)
    assert 0.9 < time() - start_time < 1.1


def test_APIBase():
    from pyracetimegg.object_mapping import APIBase
    from pyracetimegg import User
    import pytest

    request_per_second = 2
    url = "https://raw.githubusercontent.com/"
    path = "Nanahuse/PyRacetimeGG/main/test/json/user.json"

    api = APIBase(url, request_per_second)
    assert api.site_url == url
    assert api.get_url(*(path.split("/"))) == url + path
    json_data = api.fetch_json_from_site(path)
    user = api.store_data(User, json_data["id"], json_data)

    assert api.get_data_from_cache(user, "name") == "Nanahuse"
    api.clear(user)
    with pytest.raises(KeyError):
        api.get_data_from_cache(User, "name")
