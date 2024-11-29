#!/usr/bin/env python
import unittest
import json

from location import Coords


class TestLocation(unittest.TestCase):
    def setUp(self):
        pass

    def test_mount_diablo_eagle_peak(self):
        """
        (US-CA) Mount Diablo -- Eagle Peak
        https://www.f5len.org/tools/locator/
        locator: CM97AV76UA
        latitude: 37.901687598628186
        longitude: -121.93842262029649
        """

        loc = Coords.from_dec_degrees(lat=37.901687598628186,
                                      lon=-121.93842262029649)

        maiden = loc.to_maidenhead(precision=4).upper()
        self.assertTrue(maiden, "CM97AV76UA"[0:9])

        [[lat_deg, lat_min, lat_sec, lat_hemisphere],
         [lon_deg, lon_min, lon_sec, lon_hemisphere]] = loc.to_deg_min_sec()

        print(f"location: {loc}")
        print(f"maidenhead: {maiden}")
        print(f"lat: {lat_deg}, {lat_min}, {lat_sec:0.2f} {lat_hemisphere}")
        print(f"lon: {lon_deg}, {lon_min}, {lon_sec:0.2f} {lon_hemisphere}")


    def test_mount_diablo_bald_knob(self):
        """
        (US-CA) Mount Diablo -- Bald Knob
        https://www.f5len.org/tools/locator/
        locator: CM97AV84BJ
        latitude: 37.89244968464312
        longitude: -121.9255114719272
        """

        loc = Coords.from_dec_degrees(lat=37.89244968464312,
                                      lon=-121.9255114719272)

        maiden = loc.to_maidenhead(precision=4).upper()
        self.assertTrue(maiden, "CM97AV84BJ"[0:9])

        [[lat_deg, lat_min, lat_sec, lat_hemisphere],
         [lon_deg, lon_min, lon_sec, lon_hemisphere]] = loc.to_deg_min_sec()

        print(f"location: {loc}")
        print(f"maidenhead: {maiden}")
        print(f"lat: {lat_deg}, {lat_min}, {lat_sec:0.2f} {lat_hemisphere}")
        print(f"lon: {lon_deg}, {lon_min}, {lon_sec:0.2f} {lon_hemisphere}")
