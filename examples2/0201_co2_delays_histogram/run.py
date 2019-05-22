"""Histogram of CO2 decrease delays.
"""
from os.path import dirname, abspath, join
import sys
sys.path.append(abspath(join(dirname(__file__), '../..', '')))

from dm.ConnectionUtil import ConnectionUtil
from dm.FilterUtil import FilterUtil
from dm.Storage import Storage
from dm.ValueUtil import ValueUtil
from matplotlib import colors
import copy
import logging
import matplotlib.pyplot as plt
import numpy as np

__author__ = ''
__email__ = ''


def detect_sensor_delays(events, window_size, threshold, value_attr_name,
                         delays_attr_name):

    out = []
    for i in range(0, len(events)):
        event = events[i]

        values = event['measured'][value_attr_name]
        event[delays_attr_name] = ValueUtil.detect_sensor_delay(values, window_size, threshold)

        if event[delays_attr_name] > 10:
            out.append(event)

    return out


# https://matplotlib.org/gallery/statistics/hist.html
# https://realpython.com/python-histograms/
# https://matplotlib.org/1.2.1/examples/pylab_examples/histogram_demo.html
def gen_graph(data, action, extensions, title):
    data = copy.deepcopy(data)
    fig, ax = plt.subplots(figsize=(8, 3))

    x_min = 0
    x_max = 160

    out = []
    for row in data:
        if x_min < row < x_max:
            out.append(row)

    n, bins, patches = plt.hist(x=out, bins=20, color='#0504aa',
                                alpha=0.7, rwidth=0.85)

    fracs = n / n.max()
    norm = colors.Normalize(fracs.min(), fracs.max())
    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)

    plt.text(120, 90, r'$\mu=%.1f,\ \sigma=%.1f$' % (np.mean(out), np.std(out)), size=11)

    plt.grid(axis='y', alpha=0.5)
    plt.xlabel('Oneskorenie senzora [s]')
    plt.ylabel('Frequency')
    plt.xlim(x_min, x_max)
    plt.ylim(0, 100)
    # plt.title(title)

    # nastavenie, aby sa aj pri malej figsize zobrazoval nazov X osy
    plt.tight_layout()

    if 'save' in action:
        filename = '{0}_{1}'.format('histogram_delays', title)
        print('{0}: {1}'.format(filename, len(out)))

        for extension in extensions:
            fig.savefig(filename + '.' + extension, bbox_inches='tight', pad_inches=0)

    if 'show' in action:
        plt.show()


def delays(events, extensions: list, action, window_size, threshold):
    logger = logging.getLogger()
    logger.disabled = True

    logging.info('start detecting of sensor delays')
    ev = detect_sensor_delays(events, window_size, threshold, 'co2_in_ppm',
                              'co2_sensor_delays')
    events_delays = ValueUtil.delays(ev, 'co2_sensor_delays')
    logging.info('end detecting of sensor delays')

    title = 'window_size:{0},threshold:{1}'.format(window_size, threshold)
    gen_graph(events_delays, action, extensions, title)

    logger.disabled = False


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    logging.info('start')
    table_name = 'measured_filtered_peto'

    # stiahnutie dat
    con = ConnectionUtil.create_con()
    storage = Storage('examples/events_peto.json', 0, table_name)
    d = storage.load_data(con, 0, 0, 'co2_in_ppm')
    logging.info('downloaded events: %d' % len(d))

    # aplikovanie filtrov na eventy
    filtered = FilterUtil.only_valid_events(d)

    # for travis
    if ConnectionUtil.is_testable_system():
        filtered = filtered[:ConnectionUtil.MAX_TESTABLE_EVENTS]

    logging.info('events after applying the filter: %d' % len(filtered))

    extensions = ['eps']
    delays(filtered, extensions, ['save'], 11, 15)
    delays(filtered, extensions, ['save'], 16, 10)
    delays(filtered, extensions, ['save'], 16, 15)
    delays(filtered, extensions, ['save'], 16, 20)
    delays(filtered, extensions, ['save'], 16, 25)
    delays(filtered, extensions, ['save'], 21, 15)
    delays(filtered, extensions, ['save'], 21, 20)
    delays(filtered, extensions, ['save'], 21, 25)
    delays(filtered, extensions, ['save'], 21, 30)
    delays(filtered, extensions, ['save'], 21, 35)
    delays(filtered, extensions, ['save'], 21, 40)

    logging.info('end')
