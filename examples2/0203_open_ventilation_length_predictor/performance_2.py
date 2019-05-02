import numpy as np


def gen_mask(size, mask):
    out = []
    shift = len(mask) // 2

    for i in range(0, size):
        row = []
        tmp_shift = shift
        for k in range(0, size):
            if tmp_shift < 0:
                row.append(0)
            elif tmp_shift < len(mask):
                row.append(mask[tmp_shift])
            else:
                row.append(0)

            tmp_shift += 1
        out.append(row)

        shift -= 1

    return np.matrix(np.matrix(out).transpose())


def gen_table(input_data, data2, perform, mask):
    if mask is not None:
        out = 'mask: ' + str(mask) + '\n'
    else:
        out = ''

    acc = None
    if perform is not None:
        acc = round(perform * 100, 2)
        out += 'accuracy: {0:6.2f}%\n'.format(acc)

    for i in range(0, len(input_data)):
        title = input_data[i]['title']
        out += '{0:12}'.format(title)

        for item in data2[i]:
            out += '{0:7}'.format(item)
        out += '\n'

    return out, acc


if __name__ == '__main__':
    out = []

    with open('performance.txt', 'r') as f:
        for i, line in enumerate(f):
            if i <= 4:
                continue

            row = line.split('\t')
            for k in range(0, len(row)):
                column = row[k].strip()
                if column == '':
                    continue

                if k == 0:
                    title = column.split('[')[1].replace(':', '')
                    title = title.replace(']', '')
                    new_title = []

                    for item in filter(None, title.split('-')):
                        try:
                            new_title.append(round(float(item.strip()), 1))
                        except:
                            new_title.append('')

                    title_str = '[{0:4} - {1:4}]'.format(new_title[0], new_title[1])
                    out.append({
                        'title': title_str,
                        'values': [],
                        'index': i-5,
                    })
                else:
                    out[i-5]['values'].append(int(column))

    list_of_arrays = []
    for item in out:
        list_of_arrays.append(item['values'])

    mt_data = np.matrix(list_of_arrays)
    mt_data_sum = mt_data.sum()

    # mask = [0, 1, 0]
    mask = [0.5, 1, 0.5]
    # mask = [0.5, 0.75, 1, 0.75, 0.5]
    # mask = [0.25, 0.5, 0.75, 1, 0.75, 0.5, 0.25]

    mt_mask = gen_mask(mt_data.shape[0], mask)

    mt_performance = np.multiply(mt_data, mt_mask)
    mt_sum = mt_performance.sum()

    print('mask map')
    print(gen_table(out, mt_mask.tolist(), None, None)[0])
    print(gen_table(out, mt_data.tolist(), mt_sum/mt_data_sum, mask)[0])
