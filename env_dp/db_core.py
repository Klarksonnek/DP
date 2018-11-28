import configparser
import datetime
import json
import mysql.connector
import os
import pytz
import logging
import copy


TABLE_NAME = 'view_all'


def create_con(config_file='/etc/dp/config.ini'):
    # example travis hostname: travis-job-d072bd30-f722-4d10-*
    hostname = os.uname()[1]
    if 'travis' in hostname:
        return mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='',
            database='demo'
        )

    config = configparser.ConfigParser()
    config.read(config_file)

    return mysql.connector.connect(
        host=config['db']['host'],
        user=config['db']['user'],
        passwd=config['db']['passwd'],
        database=config['db']['database']
    )


def root_folder():
    pwd = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(pwd, './..', '')) + '/'


class DateTimeUtil:
    @staticmethod
    def local_time_str_to_utc(date_str, timezone='Europe/Prague', format='%Y/%m/%d %H:%M:%S'):
        # https://www.saltycrane.com/blog/2009/05/converting-time-zones-datetime-objects-python/

        datetime_obj_naive = datetime.datetime.strptime(date_str, format)
        datetime_obj_pacific = pytz.timezone(timezone).localize(datetime_obj_naive)

        return datetime_obj_pacific

    @staticmethod
    def utc_timestamp_to_local_time(timestamp, timezone='Europe/Prague'):
        utc = datetime.datetime.fromtimestamp(timestamp, pytz.timezone('UTC'))
        local_time = utc.astimezone(pytz.timezone(timezone))

        return local_time

    @staticmethod
    def utc_timestamp_to_str(timestamp, format='%Y-%m-%d %H:%M:%S'):
        local_time = DateTimeUtil.utc_timestamp_to_local_time(timestamp, 'Europe/Prague')

        return local_time.strftime(format)


class DBUt:
    @staticmethod
    def select_interval_size(table_name: str, start: int, end: int, column: str, owner: str):
        """Zistenie poctu zaznamov, ktore nie su null v danom stlpci

        :param owner:
        :param column:
        :param table_name:
        :param start:
        :param end:
        :return:
        """

        sql = 'SELECT COUNT(*) FROM ' + table_name
        sql += ' WHERE measured_time >= ' + str(start)
        sql += ' and measured_time <= ' + str(end)
        sql += ' and ' + column + ' IS NOT NULL'
        sql += ' and owner = \'' + owner + '\''

        return sql

    @staticmethod
    def select_interval(table_name: str, start: int, end: int, columns: str, owner: str):
        """Vyber casoveho intervalu na zaklade zadanych casov.

        :param columns: zoznam stlpcov, ktore sa maju vybrat, hviezdicka znaci vsetky stlpce
        :param table_name: nazov tabulky, z ktorej sa maju vyberat udaje
        :param start: timestamp zaciatku intervalu
        :param end: timestamp konca intervalu
        :return: sql dotaz na vyber daneho intervalu
        """

        sql = 'SELECT ' + columns + ' FROM ' + table_name
        sql += ' WHERE measured_time >= ' + str(start)
        sql += ' and measured_time <= ' + str(end)
        sql += ' and owner = \'' + owner + '\''

        return sql

    @staticmethod
    def select_one_value(table_name: str, measured_time: int, columns: str, owner: str):
        """Vyber jednej hodnoty na zaklade zadaneho casu.

        :param columns: zoznam stlpcov, ktore sa maju vybrat, hviezdicka znaci vsetky stlpce
        :param table_name: nazov tabulky, z ktorej sa maju vyberat udaje
        :param measured_time: cas, v ktorom sa nachadza pozadovana hodnota
        :return: sql dotaz na vyber jednej hodnoty
        """

        sql = 'SELECT ' + columns + ' FROM ' + table_name
        sql += ' WHERE measured_time = ' + str(measured_time)
        sql += ' and owner = \'' + owner + '\''

        return sql


class FilterUtil:
    @staticmethod
    def only_valid_events(events):
        out = []

        for event in events:
            if event['valid_event']:
                out.append(event)
        return out

    @staticmethod
    def temperature_diff(events, min_value, max_value):
        out = []

        for event in events:
            temp_in = event['measured']['temperature_in_celsius'][0]
            temp_out = event['measured']['temperature_out_celsius'][0]

            if min_value <= abs(temp_in - temp_out) <= max_value:
                out.append(event)

        return out

    @staticmethod
    def temperature_out_max(events, max_value):
        out = []

        for event in events:
            temp_out = event['measured']['temperature_out_celsius'][0]

            if temp_out < max_value:
                out.append(event)

        return out

    @staticmethod
    def humidity(events, min_out_specific_humidity, min_diff, max_diff):
        out = []

        for event in events:
            specific_in = event['measured']['rh_in_specific_g_kg'][0]
            specific_out = event['measured']['rh_out_specific_g_kg'][0]

            if specific_out < min_out_specific_humidity:
                out.append(event)
                continue

            if min_diff <= abs(specific_out - specific_in) <= max_diff:
                out.append(event)

        return out

    @staticmethod
    def attribute(events, attribute_name, value):
        out = []

        for event in events:
            if event[attribute_name] == value:
                out.append(event)

        return out

    @staticmethod
    def attribute_exclude(events, attribute_name, value):
        out = []

        for event in events:
            if event[attribute_name] != value:
                out.append(event)

        return out


class Storage:
    def __init__(self, filename:str, no_event_time_shift: int, owner: str):
        self.__filename = root_folder() + filename
        self.__no_event_time_shift = no_event_time_shift
        self.__owner = owner

    def read_meta(self):
        with open(self.__filename) as f:
            events = json.load(f)

        out = []
        for event in events['events']:
            # stributy, ktore su spolocne pre vsetky udalosti
            attributes = {
                'e_start': {
                    'readable': event['times']['event_start'],
                    'timestamp': int(DateTimeUtil.local_time_str_to_utc(
                        event['times']['event_start']).timestamp())
                },
                'e_end': {
                    'readable': event['times']['event_end'],
                    'timestamp': int(
                        DateTimeUtil.local_time_str_to_utc(
                            event['times']['event_end']).timestamp())
                },
                'measured': {
                    'pressure_in_hpa': [],
                    'temperature_in_celsius': [],
                    'temperature_out_celsius': [],
                    'rh_in_percentage': [],
                    'rh_in_absolute_g_m3': [],
                    'rh_in_specific_g_kg': [],
                    'rh_out_percentage': [],
                    'rh_out_absolute_g_m3': [],
                    'rh_out_specific_g_kg': [],
                    'co2_in_ppm': [],
                    'co2_in_g_m3': []
                },
                'derivatives': {
                    'after': [],
                    'before': [],
                    'no_event_after': [],
                    'no_event_before': []
                },
                'no_event_time_shift': self.__no_event_time_shift,
                'no_event_columns': None,
                'owner': self.__owner,
                'valid_event': True
            }

            # doplnenie atributov, ktore su specificke pre dany json
            # len sa nakopuruju jednotlive polozky json struktury
            for key, value in event.items():
                if key in ['times', 'devices']:
                    continue
                attributes[key] = value

            out.append(attributes)

        return out

    def load_data(self, con, start_shift: int, end_shift: int, column: str):
        data = self.read_meta()

        cur = con.cursor()
        for i in range(0, len(data)):
            event = data[i]
            owner = event['owner']

            event['start_shift'] = start_shift
            event['end_shift'] = end_shift

            start = event['e_start']['timestamp'] + start_shift
            end = event['e_end']['timestamp'] + end_shift

            # kontrola, ci velkost intervalu v db bez Null hodnot je rovnaka
            # ako rozdiel intervalov
            sql = DBUt.select_interval_size(TABLE_NAME, start, end, column, owner)
            cur.execute(sql)

            if end - start + 1 != cur.fetchone()[0]:
                event['valid_event'] = False
                continue

            # zistanie pozadovaneho intervalu
            cur.execute(DBUt.select_interval(TABLE_NAME, start, end, '*', owner))

            # doplnenie udajov z db do struktury
            for row in cur.fetchall():
                event['measured']['pressure_in_hpa'].append(row[4])
                event['measured']['temperature_in_celsius'].append(row[5])
                event['measured']['temperature_out_celsius'].append(row[6])
                event['measured']['rh_in_percentage'].append(row[7])
                event['measured']['rh_in_absolute_g_m3'].append(row[8])
                event['measured']['rh_in_specific_g_kg'].append(row[9])
                event['measured']['rh_out_percentage'].append(row[10])
                event['measured']['rh_out_absolute_g_m3'].append(row[11])
                event['measured']['rh_out_specific_g_kg'].append(row[12])
                event['measured']['co2_in_ppm'].append(row[13])
                event['measured']['co2_in_g_m3'].append(row[14])

            # ak je nastaveny posun no_eventu na nulu tato cast sa preskoci,
            # v opacnom priapde sa stiahne hodnota
            if event['no_event_time_shift'] != 0:
                sql = DBUt.select_one_value(TABLE_NAME, start + event['no_event_time_shift'],
                                            '*', owner)
                cur.execute(sql)
                event['no_event_columns'] = cur.fetchone()

        return data


class Graph:
    def __init__(self, path):
        self.__path = path
        self.__log = logging.getLogger(self.__class__.__name__)

    @staticmethod
    def db_to_simple_graph(event, column, color, label, number_output_records):
        x = []
        y = []
        length = len(event['measured'][column])

        step = 1
        if number_output_records is not None:
            step = length // number_output_records

            # ak je step nula, znamena to, ze nie je dostatok udajov, vykreslime
            # vsetky dostupne data so step jedna
            if step == 0:
                step = 1

            if step > 1:
                step += 1

        start = event['e_start']['timestamp'] + event['start_shift']
        for i in range(0, length):
            value = event['measured'][column][i]

            if i % step != 0:
                continue

            timestamp = start + i
            x.append(DateTimeUtil.utc_timestamp_to_str(timestamp, '%H:%M:%S'))
            y.append(value)

        return {
            'timestamps': x,
            'values': y,
            'label_x': label,
            'color': color,
        }

    def gen(self, data, output, scale_padding_min=0, scale_padding_max=0,
            g_type='line', min_value=None, max_value=None, global_range=False):
        f = open(output, 'w')

        f.write('<!DOCTYPE html>\n')
        f.write('<html>\n')
        f.write('	<head>\n')
        f.write('		<link href="' + self.__path + '/chart.css" rel="stylesheet">\n')
        f.write('		<script src="' + self.__path + '/jquery-3.2.1.slim.min.js"></script>\n')
        f.write('		<script src="' + self.__path + '/Chart.bundle.js"></script>\n')
        f.write('		<script src="' + self.__path + '/utils.js"></script>\n')
        f.write('	</head>\n')
        f.write('	<body>\n')

        if (max_value is not None or min_value is not None) and global_range:
            raise ValueError('Moze byt bud pouzity parameter global_range alebo min+max')

        global_min = {}
        global_max = {}

        if global_range:
            for i in range(0, len(data)):
                row = data[i]

                for g in row['graphs']:
                    numbers = g['values']

                    if row['group'] not in global_min:
                        global_min[row['group']] = min(numbers)
                    else:
                        tmp = copy.deepcopy(numbers)
                        tmp.append(global_min[row['group']])
                        global_min[row['group']] = min(tmp)

                    if row['group'] not in global_max:
                        global_max[row['group']] = max(numbers)
                    else:
                        tmp = copy.deepcopy(numbers)
                        tmp.append(global_max[row['group']])
                        global_max[row['group']] = max(tmp)

        id = 0
        for i in range(0, len(data)):
            row = data[i]
            id += 1
            canvas_id = 'g' + str(id)

            f.write('		<div style="overflow: auto;float:left">\n')
            f.write('			<canvas class="custom" id="g' + str(canvas_id))
            f.write('" width="900px" height="500" style="float:left"></canvas>\n')

            if 'stat' in row:
                f.write('		<div width="900px" height="500" style="padding: 50px; float: left">\n')

                for key, value in row['stat']:
                    sep = ':'
                    if not key and not value:
                        sep = '&nbsp;'

                    f.write("<div>%s %s %s</div>" % (key, sep, value))
                f.write('		</div>\n')

            f.write('		</div>\n')

            all_min = None
            all_max = None

            if min_value is not None and max_value is not None:
                all_min = min_value
                all_max = max_value
            elif not global_range:
                for g in row['graphs']:
                    numbers = g['values']

                    if not numbers:
                        self.__log.warning('graph \'%s\' with label \'%s\' does not any value' %
                                         (data[i]['title'], g['label_x']))

                    if all_min is None:
                        all_min = min(numbers)
                    else:
                        tmp = copy.deepcopy(numbers)
                        tmp.append(all_min)
                        all_min = min(tmp)

                    if all_max is None:
                        all_max = max(numbers)
                    else:
                        tmp = copy.deepcopy(numbers)
                        tmp.append(all_max)
                        all_max = max(tmp)

            if global_range:
                all_min = global_min[row['group']]
                all_max = global_max[row['group']]

            all_min -= scale_padding_min
            all_max += scale_padding_max

            str_dataset = ""
            g_id = 0
            for g in row['graphs']:
                str_dataset += '						{\n'
                str_dataset += '							label: "' + g['label_x'] + '",\n'
                str_dataset += '							borderColor: "' + g['color'] + '",\n'
                str_dataset += '							backgroundColor: "' + g['color'] + '",\n'
                str_dataset += '							fill: false,\n'
                str_dataset += '							data: ' + str(g['values']) + ',\n'
                str_dataset += '							yAxisID: "y-axis-' + str(g_id) + '"\n'
                str_dataset += '						},\n'

            str_options = ""
            str_options += '							{\n'
            str_options += '								type: "linear",\n'
            str_options += '								display: true,\n'
            str_options += '								position: "left",\n'
            if g_type == 'bar':
                str_options += '								stacked: true,\n'
            else:
                str_options += '								stacked: false,\n'
            str_options += '								id: "y-axis-' + str(g_id) + '",\n'
            str_options += '								ticks: {\n'
            str_options += '									min: ' + str(all_min) + ',\n'
            str_options += '									max: ' + str(all_max) + '\n'
            str_options += '								}\n'
            str_options += '							},\n'

            f.write('		<script>\n')
            f.write('			var ctx = document.getElementById("g' + str(canvas_id) + '");\n')
            f.write('			var myChart1 = new Chart(ctx, {\n')
            f.write('				type: "' + g_type + '",\n')
            f.write('				data: {\n')
            f.write('					labels: ' + str(row['graphs'][0]['timestamps']) + ',\n')
            f.write('					datasets: [\n')
            f.write(str_dataset)
            f.write('					]\n')
            f.write('				},\n')
            f.write('				options: {\n')
            f.write('					responsive: false,\n')
            f.write('					hoverMode: "index",\n')

            if g_type == 'bar':
                f.write('					stacked: true,\n')
            else:
                f.write('					stacked: false,\n')

            f.write('					title: {\n')
            f.write('						display: true,\n')
            f.write('						text: "' + row['title'] + '"\n')
            f.write('					},\n')

            if g_type == 'bar':
                f.write('					tooltips: {\n')
                f.write('						mode: \'index\',\n')
                f.write('						intersect: false\n')
                f.write('					},\n')

            f.write('					scales: {\n')

            f.write('						yAxes: [\n')
            f.write(str_options)
            f.write('						],\n')
            f.write('						xAxes: [{\n')
            f.write('							stacked: true\n')
            f.write('						}],\n')

            f.write('					}\n')
            f.write('				}\n')
            f.write('			});\n')
            f.write('		</script>\n')

        f.write('	</body>\n')
        f.write('</html>\n')
        f.close()