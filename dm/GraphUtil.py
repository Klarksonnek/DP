from os.path import dirname, abspath, join
import sys
import matplotlib.pyplot as plt
import numpy as np

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

from dm.ValueUtil import ValueUtil


class GraphUtil:
    @staticmethod
    def gen_duration_histogram(events, action, extensions, title,
                               intervals, threshold):
        """ Vygenerovanie histogramu dlzok vetrania.

        :param events: zoznam eventov
        :param action: show|save - pre ulozenie alebo zobrazenie histogramu
        :param extensions: zoznam pripon v pripade, ze sa ma subor ulozit
        :param title: nazov grafu
        :param intervals: zoznam intervalov v minutach, pre ktore sa ma pocitat pocet hodnot
        :param threshold: hodnota, ktora sa pripocita/odpocita od intervalu a vytvori sa rozsah hodnot
                          pre dany stlpec v histograme
        :return:
        """
        durations = ValueUtil.events_duration(events, None)

        x = []
        y = []
        for interval in intervals:
            x.append('%d - %d' % (interval - threshold, interval + threshold))
            y.append(0)

        threshold *= 60
        for value in durations:
            for k in range(0, len(intervals)):
                interval = intervals[k] * 60

                if (interval - threshold) < value < (interval + threshold):
                    y[k] += 1
                    break

        fig, ax = plt.subplots(figsize=(8, 5))
        y_pos = np.arange(len(x))

        plt.bar(y_pos, y, align='center', alpha=0.5, color='#0504aa')
        plt.grid(axis='y', alpha=0.5)
        plt.xticks(y_pos, x)
        plt.xlabel('Ventilation length [min]')
        plt.ylabel('Frequency')
        plt.title(title)

        text = 'celkom eventov: {0}\n'.format(len(events))
        text += 'eventy, ktore vyhovuju intervalom: {0}'.format(sum(y))
        plt.text(len(x) * 0.5, max(y)*0.8, text)

        # nastavenie, aby sa aj pri malej figsize zobrazoval nazov X osy
        plt.tight_layout()

        if 'save' in action:
            filename = '{0}_{1}'.format('histogram_delays', title)
            for extension in extensions:
                fig.savefig(filename + '.' + extension, bbox_inches='tight', pad_inches=0)

        if 'show' in action:
            plt.show()
