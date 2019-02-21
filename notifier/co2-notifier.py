#!/usr/bin/env python3

from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '..', ''))
sys.path.append(CODE_DIR)

from dm.BeeeOnClient import BeeeOnClient
from dm.DateTimeUtil import DateTimeUtil
import logging
import time
import subprocess
import os

CONFIG_DIR = os.path.expanduser('~/.config/co2-notifier')
CONFIG_FILE = CONFIG_DIR + '/api.key'
API_KEY = 'chu1oomah5wiayeiK4Hogoo2keetah2biu9koopheth6ef6eeB3doh5veivaiyahb0chiemoh0ahma5i'
GATEWAY_ID = 1816820318180747
DEVICE_ID = 0xa900811026800001
SENSOR_ID = 2

CO2_LIMIT = 1200               # ppm
SLEEP_TIME = 10                # seconds
DELAY_BETWEEN_SEND = 5 * 60    # minutes


def extract_value(sensor_info, device_id):
    return sensor_info[device_id]['current']


def send_notification(text):
    subprocess.call(['notify-send', 'CO2 Notification', text])


if __name__ == '__main__':
    logging.basicConfig(filename='/tmp/co2_analyzer.log', level=logging.DEBUG)
    cl = BeeeOnClient("ant-work.fit.vutbr.cz", 8010)
    cl.api_key = API_KEY

    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            cl.token_id = f.read().strip()
    else:
        with open(CONFIG_FILE, 'w') as f:
            f.write(cl.token_id + '\n')

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

            time_out_str = DateTimeUtil.utc_timestamp_to_str(measured_time, '%Y/%m/%d %H:%M:%S')
            logging.debug(time_out_str + ': ' + measured_value)

            text = 'Aktualna koncentracia {0} ppm'.format(int(float(measured_value)))

            if last_time_notification is None or last_time_notification + DELAY_BETWEEN_SEND < time.time():
                if float(measured_value) > CO2_LIMIT:
                    text += ", (limit " + str(CO2_LIMIT) + " ppm), prosim vyvetrajte."

                last_time_notification = time.time()
                send_notification(text)
                logging.debug('send notification')

        os.remove(CONFIG_FILE)

    except KeyboardInterrupt:
        loop_end = True
        os.remove(CONFIG_FILE)
    except:
        send_notification('notificator failed')
    finally:
        del cl
