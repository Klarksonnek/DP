#!/usr/bin/env python3

from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '..', ''))
sys.path.append(CODE_DIR)

print(CODE_DIR)

import env_dp.core as dp
import logging
import time
import subprocess

API_KEY = 'chu1oomah5wiayeiK4Hogoo2keetah2biu9koopheth6ef6eeB3doh5veivaiyahb0chiemoh0ahma5i'
GATEWAY_ID = 1816820318180747
DEVICE_ID = 0xa9004a4a147d0001
SENSOR_ID = 2

CO2_LIMIT = 1600               # ppm
SLEEP_TIME = 10                # seconds
DELAY_BETWEEN_SEND = 5 * 60    # minutes


def extract_value(sensor_info, device_id):
    return sensor_info[device_id]['current']


def send_notification(text):
    subprocess.call(['notify-send', 'CO2 Notification', text])


if __name__ == '__main__':
    logging.basicConfig(filename='/tmp/co2_analyzer.log', level=logging.DEBUG)

    cl = dp.BeeeOnClient("ant-work.fit.vutbr.cz", 8010, cache=False)
    cl.api_key = API_KEY

    loop_end = False
    last_time_notification = None

    try:
        while not loop_end:
            time.sleep(SLEEP_TIME)

            sensor_info = cl.sensors_info(GATEWAY_ID, DEVICE_ID)
            value = extract_value(sensor_info, SENSOR_ID)

            measured_time = value['at']
            measured_value = value['value']

            if measured_value is None:
                continue

            time_out_str = dp.utc_timestamp_to_str(measured_time, '%Y/%m/%d %H:%M:%S')

            logging.debug(time_out_str + ': ' + measured_value)
            if float(measured_value) > CO2_LIMIT:
                text = "Aktualna koncentracia "
                text += str(int(float(measured_value)))
                text += " ppm, (limit " + str(CO2_LIMIT) + " ppm)"
                text += ", prosim vyvetrajte."

                if last_time_notification is None:
                    last_time_notification = time.time()
                    send_notification(text)
                    logging.debug('send notification')
                    continue

                if last_time_notification + DELAY_BETWEEN_SEND < time.time():
                    last_time_notification = time.time()
                    send_notification(text)
                    logging.debug('send notification')

    except KeyboardInterrupt:
        loop_end = True
