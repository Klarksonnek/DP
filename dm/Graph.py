import copy
import logging
from dm.DateTimeUtil import DateTimeUtil


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

            if value is None:
                y.append('Null')
            else:
                y.append(value)

        return {
            'timestamps': x,
            'values': y,
            'label_x': label,
            'color': color,
            'open_close': column == 'open_close',
        }

    def gen(self, data, output, scale_padding_min=0, scale_padding_max=0,
            g_type='line', min_value=None, max_value=None, global_range=False):
        f = open(output, 'w')

        f.write('<!DOCTYPE html>\n')
        f.write('<html>\n')
        f.write('	<head>\n')
        f.write('		<link href="' + self.__path + '/chart.css" rel="stylesheet">\n')
        f.write(
            '		<script src="' + self.__path + '/jquery-3.2.1.slim.min.js"></script>\n')
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

                    if 'open_close' in g and g['open_close']:
                        continue

                    if 'Null' in numbers:
                        continue

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
                f.write(
                    '		<div width="900px" height="500" style="padding: 50px; float: left">\n')

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
                    if 'open_close' in g and g['open_close']:
                        continue

                    numbers = g['values']

                    if not numbers:
                        self.__log.warning(
                            'graph \'%s\' with label \'%s\' does not any value' %
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
            open_close_graph_type = False
            for g in row['graphs']:
                if 'open_close' in g:
                    open_close_graph_type = g['open_close']

                str_dataset += '						{\n'
                str_dataset += '							label: "' + g['label_x'] + '",\n'
                str_dataset += '							borderColor: "' + g[
                    'color'] + '",\n'
                str_dataset += '							backgroundColor: "' + g[
                    'color'] + '",\n'
                str_dataset += '							fill: false,\n'
                str_dataset += '							data: ' + str(g['values']) + ',\n'

                if open_close_graph_type:
                    str_dataset += '							yAxisID: "open-close-y"\n'
                else:
                    str_dataset += '							yAxisID: "y-axis-' + str(
                        g_id) + '"\n'

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

            if open_close_graph_type:
                str_options += '							{\n'
                str_options += '								type: "linear",\n'
                str_options += '								display: true,\n'
                str_options += '								position: "right",\n'
                if g_type == 'bar':
                    str_options += '								stacked: true,\n'
                else:
                    str_options += '								stacked: false,\n'
                str_options += '								id: "open-close-y",\n'
                str_options += '								ticks: {\n'
                str_options += '									min: 0,\n'
                str_options += '									max: 1\n'
                str_options += '								}\n'
                str_options += '							},\n'

            f.write('		<script>\n')
            f.write(
                '			var ctx = document.getElementById("g' + str(canvas_id) + '");\n')
            f.write('			var myChart1 = new Chart(ctx, {\n')
            f.write('				type: "' + g_type + '",\n')
            f.write('				data: {\n')
            f.write(
                '					labels: ' + str(row['graphs'][0]['timestamps']) + ',\n')
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
