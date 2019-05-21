from os.path import dirname, abspath, join
import sys
sys.path.append(abspath(join(dirname(__file__), '../..', '')))

from dm.Performance import Performance


OUTPUT_FILENAME = '0202_open_detector/out.csv'
BEFORE_TIME = 10 * 60
AFTER_TIME = 10 * 60

if __name__ == '__main__':
    p = Performance(abspath(OUTPUT_FILENAME))

    table, _, _ = p.simple()
    print(table)

    table, wrong, _ = p.with_delay(BEFORE_TIME, AFTER_TIME)
    print(table)

    for row in wrong:
        print(row)
