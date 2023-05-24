import socket
import unittest

from world_weather import get_user_location


class WorldWeatherTest(unittest.TestCase):
    def test_get_user_location(self):
        ip = socket.gethostbyname("be-299-ar01.santaclara.ca.sfba.comcast.net")
        self.assertEqual("68.86.143.93", ip)

        location = get_user_location(ip)
        self.assertEqual("San Jose, US", location)
