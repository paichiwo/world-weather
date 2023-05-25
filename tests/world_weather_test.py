import unittest

from world_weather import (
    format_date_long,
    format_date_short,
    mtr_per_sec_to_km_per_hour,
)


class WorldWeatherTest(unittest.TestCase):
    def test_speed(self):
        self.assertEqual(10.8, mtr_per_sec_to_km_per_hour(3))

    def test_format_date(self):
        iso = "2023-05-24"
        self.assertEqual("24 May", format_date_short(iso))
        self.assertEqual("Wed, 24 May", format_date_long(iso))
