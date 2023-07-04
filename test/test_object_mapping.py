# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/PyRacetimeGG/blob/main/LICENSE


def test_rate():
    from pyracetimegg.object_mapping import Rate
    from time import time

    frame_rate = 10
    rate = Rate(frame_rate)

    start_time = time()
    for _ in range(frame_rate * 5):
        rate.sleep()
    result = time() - start_time
    assert 4.9 < result < 5.1
