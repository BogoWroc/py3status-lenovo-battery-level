import unittest

from py3status_lbl.lenovo_battery_level import BatteryInfoModel, BatteryLevelElement


class MyTestCase(unittest.TestCase):
    def test_convert_linux_battery_status_to_data_model(self):
        expected_battery_info = {'History (charge)': '',
                                 'History (rate)': '',
                                 'capacity': '87,4844%',
                                 'energy': '21 Wh',
                                 'energy-empty': '0 Wh',
                                 'energy-full': '21,17 Wh',
                                 'energy-full-design': '24,05 Wh',
                                 'energy-rate': '9,796 W',
                                 'has history': 'yes',
                                 'has statistics': 'yes',
                                 'icon-name': "'battery-full-symbolic'",
                                 'model': '01AV424',
                                 'native-path': 'BAT1',
                                 'percentage': '99%',
                                 'power supply': 'yes',
                                 'present': 'yes',
                                 'rechargeable': 'yes',
                                 'serial': '4458',
                                 'state': 'discharging',
                                 'technology': 'lithium-polymer',
                                 'time to empty': '2,1 hours',
                                 'vendor': 'Celxpert',
                                 'voltage': '12,23 V',
                                 'warning-level': 'none'}

        txt = b"  native-path:          BAT1\n  vendor:               Celxpert\n  model:                01AV424\n  serial:               4458\n  power supply:         yes\n  updated:              wto, 12 maj 2020, 10:39:01 (11 seconds ago)\n  has history:          yes\n  has statistics:       yes\n  battery\n    present:             yes\n    rechargeable:        yes\n    state:               discharging\n    warning-level:       none\n    energy:              21 Wh\n    energy-empty:        0 Wh\n    energy-full:         21,17 Wh\n    energy-full-design:  24,05 Wh\n    energy-rate:         9,796 W\n    voltage:             12,23 V\n    time to empty:       2,1 hours\n    percentage:          99%\n    capacity:            87,4844%\n    technology:          lithium-polymer\n    icon-name:          'battery-full-symbolic'\n  History (charge):\n    1589272741\t99,000\tdischarging\n  History (rate):\n    1589272741\t9,796\tdischarging\n\n"

        self.assertEqual(expected_battery_info, BatteryInfoModel.create(txt))

    def test_should_return_formatted_message_with_battery_status_displayed_as_percentage(self):
        battery_info_0 = {
            'percentage': '99%',
            'time to empty': '2,1 hours'
        }

        battery_info_1 = {
            'percentage': '50%',
            'time to empty': '1 hours'
        }

        self.assertEqual("B0(99%) B1(50%)",
                         BatteryLevelElement.format_message(battery_info_0, battery_info_1, 'percentage'))

    def test_should_return_formatted_message_with_information_time_to_empty_no_charging_case(self):
        battery_info_0 = {
            'percentage': '99%',
        }

        battery_info_1 = {
            'percentage': '50%',
            'time to empty': '1 hours'
        }

        self.assertEqual("Time left: B0(-:--h) B1(1:00h)",
                         BatteryLevelElement.format_message(battery_info_0, battery_info_1, 'time to empty'))

    def test_should_return_formatted_message_with_information__time_to_full_charging_case(self):
        battery_info_0 = {
            'percentage': '99%',
        }

        battery_info_1 = {
            'percentage': '50%',
            'time to full': '1 hours'
        }

        self.assertEqual("Charging: B0(-:--h) B1(1:00h)",
                         BatteryLevelElement.format_message(battery_info_0, battery_info_1, 'time to full'))

    def test_should_return_time_in_hours(self):
        self.assertEqual("1:12", BatteryLevelElement._time_in_hour_format("1,2 hours"))
        self.assertEqual("0:33", BatteryLevelElement._time_in_hour_format("33,3 minutes"))


if __name__ == '__main__':
    unittest.main()
