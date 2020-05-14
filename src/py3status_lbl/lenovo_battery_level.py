import subprocess

BASH_COMMAND_BATTERY_0 = "upower -i /org/freedesktop/UPower/devices/battery_BAT0"
BASH_COMMAND_BATTERY_1 = "upower -i /org/freedesktop/UPower/devices/battery_BAT1"


class Ubuntu:
    @staticmethod
    def get_battery_status(bash_command):
        process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        return output


class BatteryInfoModel:
    @staticmethod
    def create(battery_status):
        status = battery_status.decode("utf-8").split("\n")
        model = {}
        for element in status:
            data = element.split(":")
            if BatteryInfoModel._skip_element(data):
                continue
            model[data[0].strip()] = data[1].strip()

        return model

    @staticmethod
    def _skip_element(element):
        if len(element) != 2:
            return True
        else:
            return False


class BatteryLevelElement:
    @staticmethod
    def format_message(battery_data_0, battery_data_1, key):
        if key == 'percentage':
            return "B0({}) B1({})".format(battery_data_0[key], battery_data_1[key])
        if key == 'time to empty':
            return BatteryLevelElement._time_as_message("Time left: B0({}h) B1({}h)", key, battery_data_0, battery_data_1)
        if key == 'time to full':
            return BatteryLevelElement._time_as_message("Charging: B0({}h) B1({}h)", key, battery_data_0, battery_data_1)
        return "Key not supported!"

    @staticmethod
    def _time_as_message(msg_pattern, key, battery_data_0, battery_data_1):
        b0 = "-:--"
        if key in battery_data_0:
            b0 = BatteryLevelElement._time_in_hour_format(battery_data_0[key])

        b1 = "-:--"
        if key in battery_data_1:
            b1 = BatteryLevelElement._time_in_hour_format(battery_data_1[key])
        return msg_pattern.format(b0, b1)

    @staticmethod
    def _time_in_hour_format(time_data):
        data = time_data.split(" ")
        if data[1] == 'hours':
            t = float(data[0].replace(',', '.')) * 60
            h = int(t) // 60
            m = int(t) % 60
            return "{}:{:02d}".format(h, m)
        else:
            t = float(data[0].replace(',', '.'))
            return "0:{:02d}".format(int(t))


class Py3status:
    format_clicked = '{msg}'

    def __init__(self):
        self.button = None

    def click_info(self):
        b0_info = BatteryInfoModel.create(Ubuntu.get_battery_status(BASH_COMMAND_BATTERY_0))
        b1_info = BatteryInfoModel.create(Ubuntu.get_battery_status(BASH_COMMAND_BATTERY_1))

        if self.button:
            key = 'time to full' if 'time to full' in b1_info else 'time to empty'
            data = {'msg': BatteryLevelElement.format_message(b0_info, b1_info, key)}
            full_text = self.py3.safe_format(self.format_clicked, data)
            self.button = None
        else:
            full_text = BatteryLevelElement.format_message(b0_info, b1_info, 'percentage')

        return {
            'full_text': full_text
        }

    def on_click(self, event):
        self.button = event['button']
        # Our modules update methods will get called automatically.


if __name__ == "__main__":
    """
    Run module in test mode.
    """
    from py3status.module_test import module_test

    module_test(Py3status)
