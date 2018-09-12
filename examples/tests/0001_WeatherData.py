from os.path import dirname, abspath, join
import sys
THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

import env_dp.core as e
import unittest

class TestWeatherData(unittest.TestCase):

    def test_interval_length(self):
        """Time interval: 2.7.2018 06:30 - 2.7.2018 07:00.
           If data is too long or too short, it fails.
           If start of interval is invalid, it fails.
           If end of interval is invalid, it fails.
        """
        w = e.WeatherData(cache=False)
        s_time = 1530505800
        e_time = 1530507600
        data = w.weather_data(s_time, e_time)

        self.assertEqual(e_time - s_time + 1, len(data))
        self.assertEqual(s_time, data[0]['at'])
        self.assertEqual(e_time, data[-1]['at'])


if __name__ == '__main__':
    unittest.main()
