from os.path import dirname, abspath, join
import sys
sys.path.append(abspath(join(dirname(__file__), '../..', '')))

from dm.AttributeUtil import AttributeUtil
from dm.CSVUtil import CSVUtil
from dm.ConnectionUtil import ConnectionUtil
from dm.DateTimeUtil import DateTimeUtil
from dm.FilterUtil import FilterUtil
from dm.Storage import Storage
from dm.attrs.DifferenceBetweenRealLinear import DifferenceBetweenRealLinear
from dm.attrs.FirstDifferenceAttrA import FirstDifferenceAttrA
from dm.attrs.FirstDifferenceAttrB import FirstDifferenceAttrB
from dm.attrs.InOutDiff import InOutDiff
from dm.attrs.SecondDifferenceAttr import SecondDifferenceAttr
from dm.selectors.interval.SimpleIntervalSelector import SimpleIntervalSelector
from dm.selectors.row.CachedDiffRowWithIntervalSelector import CachedDiffRowWithIntervalSelector
import logging


no_events_records = [
    # 1. iteration
    ('2018/11/27 08:10:30', 'nothing'),
    ('2018/11/29 02:08:00', 'nothing'),
    ('2018/11/30 23:02:00', 'nothing'),
    ('2018/12/01 12:52:00', 'nothing'),
    ('2018/12/01 16:00:30', 'nothing'),
    ('2018/12/02 01:15:30', 'nothing'),
    ('2018/12/03 10:08:30', 'nothing'),
    ('2018/12/03 15:08:30', 'nothing'),
    ('2018/12/06 18:26:00', 'nothing'),
    ('2018/12/06 23:31:30', 'nothing'),

    # 2. iteration
    ('2018/12/01 15:48:00', 'nothing'),
    ('2018/12/02 10:28:00', 'nothing'),
    ('2018/12/03 10:08:00', 'nothing'),
    ('2018/12/03 23:00:30', 'nothing'),
    ('2018/12/04 12:16:30', 'nothing'),
    ('2018/12/05 08:19:00', 'nothing'),
    ('2018/12/07 11:55:30', 'nothing'),
    ('2018/12/07 22:44:00', 'nothing'),
    ('2018/12/19 12:26:00', 'nothing'),
    ('2018/12/19 17:28:30', 'nothing'),

    # 3. iteration
    ('2018/12/03 18:51:00', 'nothing'),
    ('2018/12/16 07:55:30', 'nothing'),
    ('2018/12/22 08:17:00', 'nothing'),
    ('2018/12/24 07:27:00', 'nothing'),
    ('2018/12/24 08:11:00', 'nothing'),
    ('2018/12/26 12:45:30', 'nothing'),
    ('2018/12/27 12:49:30', 'nothing'),
    ('2018/12/27 15:39:30', 'nothing'),
    ('2018/12/28 11:54:00', 'nothing'),
    ('2018/12/28 15:40:00', 'nothing'),

    # 4. iteration
    ('2018/12/26 18:32:00', 'nothing'),
    ('2018/12/27 20:19:30', 'nothing'),
    ('2018/12/28 06:19:30', 'nothing'),
    ('2018/12/30 07:27:00', 'nothing'),
    ('2018/12/30 10:06:00', 'nothing'),
    ('2018/12/31 06:38:00', 'nothing'),
    ('2018/12/31 11:53:30', 'nothing'),
    ('2019/01/01 17:04:00', 'nothing'),
    ('2019/01/08 06:42:00', 'nothing'),
    ('2019/01/08 21:53:30', 'nothing'),

    # 5. iteration
    ('2018/12/27 23:48:00', 'nothing'),
    ('2018/12/28 09:42:30', 'nothing'),
    ('2018/12/28 22:01:00', 'nothing'),
    ('2018/12/31 06:27:30', 'nothing'),
    ('2018/12/31 11:53:30', 'nothing'),
    ('2019/01/02 10:04:30', 'nothing'),
    ('2019/01/03 06:18:30', 'nothing'),
    ('2019/01/04 21:53:00', 'nothing'),
    ('2019/01/07 06:21:30', 'nothing'),
    ('2019/01/08 10:18:30', 'nothing'),

    # 6. iteration
    ('2018/12/26 06:18:30', 'nothing'),
    ('2019/01/08 21:59:00', 'nothing'),
    ('2019/01/13 09:07:30', 'nothing'),
    ('2019/01/19 22:32:00', 'nothing'),
    ('2019/02/01 18:21:30', 'nothing'),
    ('2019/02/11 16:58:00', 'nothing'),
    ('2019/02/15 20:06:30', 'nothing'),
    ('2019/02/19 18:06:30', 'nothing'),
    ('2019/02/27 18:58:30', 'nothing'),
    ('2019/03/02 19:42:30', 'nothing'),

    # 7. iteration
    ('2019/03/03 15:01:30', 'nothing'),
    ('2019/03/08 12:21:00', 'nothing'),
    ('2019/03/09 07:55:30', 'nothing'),
    ('2019/03/10 19:12:00', 'nothing'),
    ('2019/03/10 19:48:00', 'nothing'),
    ('2019/03/14 06:23:30', 'nothing'),
    ('2019/03/14 07:28:00', 'nothing'),
    ('2019/03/15 12:50:30', 'nothing'),
    ('2019/03/20 10:40:00', 'nothing'),
    ('2019/03/21 08:02:30', 'nothing'),

    # 8. iteration
    ('2019/02/27 18:58:30', 'nothing'),
    ('2019/03/09 07:55:30', 'nothing'),
    ('2019/03/14 07:28:00', 'nothing'),
    ('2019/03/24 10:23:00', 'nothing'),
    ('2018/11/26 22:27:00', 'nothing'),
    ('2018/12/06 20:56:00', 'nothing'),
    ('2018/12/16 07:55:30', 'nothing'),
    ('2018/12/26 06:18:30', 'nothing'),
    ('2018/12/26 18:31:30', 'nothing'),
    ('2019/01/15 06:58:00', 'nothing'),

    # 9. iteration
    ('2019/01/05 16:09:00', 'nothing'),
    ('2019/01/05 16:57:30', 'nothing'),
    ('2019/01/08 21:58:30', 'nothing'),
    ('2019/01/19 12:14:00', 'nothing'),
    ('2019/01/19 21:12:00', 'nothing'),
    ('2019/02/08 06:31:30', 'nothing'),
    ('2019/03/05 06:23:30', 'nothing'),
    ('2019/03/09 07:55:30', 'nothing'),
    ('2019/03/15 08:08:30', 'nothing'),
    ('2019/03/20 10:40:00', 'nothing'),

    # 10. iteration
    ('2019/01/16 07:48:00', 'nothing'),
    ('2019/01/19 12:14:00', 'nothing'),
    ('2019/01/21 21:45:00', 'nothing'),
    ('2019/02/11 11:13:30', 'nothing'),
    ('2019/01/30 19:27:30', 'nothing'), # dvojzakmit
    ('2019/01/30 19:28:00', 'nothing'),
    ('2019/02/20 18:47:30', 'nothing'),
    ('2019/02/20 18:48:00', 'nothing'),
    ('2019/02/24 11:03:30', 'nothing'),
    ('2019/02/24 11:05:00', 'nothing'),

    # 11. iteration
    ('2018/12/03 07:14:00', 'nothing'),
    ('2018/12/03 07:14:30', 'nothing'),
    ('2018/12/26 18:32:30', 'nothing'),
    ('2019/01/05 16:58:00', 'nothing'),
    ('2019/01/21 21:46:00', 'nothing'),
    ('2019/01/21 21:50:00', 'nothing'),
    ('2019/01/30 19:28:00', 'nothing'),
    ('2019/02/20 18:47:30', 'nothing'),
    ('2019/02/20 18:48:00', 'nothing'),
    ('2019/02/27 18:58:30', 'nothing'),

    # 12. iteration
    ('2018/12/03 07:14:00', 'nothing'),
    ('2018/12/03 07:14:30', 'nothing'),
    ('2018/12/20 10:42:00', 'nothing'),
    ('2018/12/20 10:42:30', 'nothing'),
    ('2019/01/27 11:15:30', 'nothing'),
    ('2019/01/27 11:16:00', 'nothing'),
    ('2019/01/30 19:28:00', 'nothing'),
    ('2019/02/11 11:11:30', 'nothing'),
    ('2019/02/20 18:47:30', 'nothing'),
    ('2019/02/20 18:48:00', 'nothing'),

    # 13. iteration
    ('2018/12/03 07:14:00', 'nothing'),
    ('2018/12/03 07:14:30', 'nothing'),
    ('2019/01/16 11:29:00', 'nothing'),
    ('2019/01/16 11:29:30', 'nothing'),
    ('2019/01/30 19:28:00', 'nothing'),
    ('2019/02/11 09:39:00', 'nothing'),
    ('2019/02/11 09:40:30', 'nothing'),
    ('2019/02/11 16:52:00', 'nothing'),
    ('2019/02/13 22:14:00', 'nothing'),
    ('2019/02/13 22:14:30', 'nothing'),

    # 14. iteration
    ('2018/12/07 15:35:00', 'nothing'),
    ('2018/12/20 10:42:00', 'nothing'),
    ('2018/12/20 10:42:30', 'nothing'),
    ('2019/01/15 09:15:00', 'nothing'),
    ('2019/02/04 18:51:00', 'nothing'),
    ('2019/02/04 18:51:30', 'nothing'),
    ('2019/02/11 09:39:00', 'nothing'),
    ('2019/02/20 18:48:00', 'nothing'),
    ('2019/02/24 11:05:00', 'nothing'),
    ('2019/02/27 18:58:30', 'nothing'),

    # 15. iteration
    ('2018/12/20 10:42:00', 'nothing'),
    ('2018/12/20 10:42:30', 'nothing'),
    ('2019/02/04 18:51:00', 'nothing'),
    ('2019/02/04 18:51:30', 'nothing'),
    ('2019/02/20 18:48:00', 'nothing'),
    ('2019/02/24 11:05:00', 'nothing'),
    ('2019/03/14 18:09:30', 'nothing'),
    ('2019/03/16 12:21:30', 'nothing'),
    ('2019/03/16 12:22:00', 'nothing'),
    ('2019/03/25 09:15:30', 'nothing'),

    # 16. iteration
    ('2018/12/20 10:42:00', 'nothing'),
    ('2018/12/20 10:42:30', 'nothing'),
    ('2019/01/16 11:28:00', 'nothing'),
    ('2019/01/16 11:30:00', 'nothing'),
    ('2019/01/21 21:52:00', 'nothing'),
    ('2019/02/04 18:51:00', 'nothing'),
    ('2019/02/20 18:48:00', 'nothing'),
    ('2019/01/28 22:03:30', 'nothing'), # trojzakmity
    ('2019/01/28 22:04:00', 'nothing'),
    ('2019/01/28 22:04:30', 'nothing'),

    # 17. iteration
    ('2018/12/20 07:03:00', 'nothing'),
    ('2018/12/20 10:42:00', 'nothing'),
    ('2019/01/15 09:16:00', 'nothing'),
    ('2019/01/16 11:28:30', 'nothing'),
    ('2019/01/21 21:45:00', 'nothing'),
    ('2019/01/21 21:50:30', 'nothing'),
    ('2019/01/25 06:50:30', 'nothing'),
    ('2019/01/27 11:15:30', 'nothing'),
    ('2019/02/03 08:20:30', 'nothing'),
    ('2019/02/11 09:39:30', 'nothing'),

    # 18. iteration
    ('2018/12/20 10:42:00', 'nothing'),
    ('2019/01/30 06:17:30', 'nothing'),
    ('2019/02/07 20:46:00', 'nothing'),
    ('2019/02/07 20:47:30', 'nothing'),
    ('2019/02/13 22:09:00', 'nothing'),
    ('2019/02/13 22:12:30', 'nothing'),
    ('2019/02/14 07:15:30', 'nothing'),
    ('2019/02/14 07:16:00', 'nothing'),
    ('2019/02/20 18:48:00', 'nothing'),
    ('2019/03/16 12:22:00', 'nothing'),

    # 19. iteration
    ('2019/01/16 11:30:30', 'nothing'),
    ('2019/02/14 07:15:30', 'nothing'),
    ('2019/02/14 07:16:00', 'nothing'),
    ('2019/03/09 16:24:30', 'nothing'),
    ('2019/03/25 19:22:30', 'nothing'),
    ('2019/03/25 19:23:00', 'nothing'),
    ('2019/01/13 18:50:00', 'nothing'), # ctyrzakmit
    ('2019/01/13 18:50:30', 'nothing'),
    ('2019/01/13 18:51:00', 'nothing'),
    ('2019/01/13 18:51:30', 'nothing'),

    # 20. iteration
    ('2019/01/13 18:50:00', 'nothing'),
    ('2019/01/13 18:50:30', 'nothing'),
    ('2019/01/13 18:51:00', 'nothing'),
    ('2019/01/13 18:51:30', 'nothing'),
    ('2019/01/16 11:28:00', 'nothing'),
    ('2019/01/16 11:37:00', 'nothing'),
    ('2019/01/23 07:11:00', 'nothing'),
    ('2019/01/23 07:11:30', 'nothing'),
    ('2019/01/23 07:12:00', 'nothing'),
    ('2019/03/16 15:26:00', 'nothing'),

    # 21. iteration
    ('2019/01/13 18:50:00', 'nothing'),
    ('2019/01/13 18:50:30', 'nothing'),
    ('2019/01/13 18:51:00', 'nothing'),
    ('2019/01/15 09:15:00', 'nothing'),
    ('2019/01/26 12:10:00', 'nothing'),
    ('2019/01/26 12:10:30', 'nothing'),
    ('2019/02/04 09:42:00', 'nothing'),
    ('2019/02/04 09:42:30', 'nothing'),
    ('2019/02/04 09:43:00', 'nothing'),
    ('2019/02/14 07:15:30', 'nothing'),

    # 22. iteration
    ('2019/01/13 18:50:00', 'nothing'),
    ('2019/01/13 18:50:30', 'nothing'),
    ('2019/01/13 18:51:00', 'nothing'),
    ('2019/01/26 12:10:00', 'nothing'),
    ('2019/02/04 09:42:30', 'nothing'),
    ('2019/02/04 09:43:00', 'nothing'),
    ('2019/02/10 10:34:00', 'nothing'),
    ('2019/02/10 10:34:30', 'nothing'),
    ('2019/02/13 22:14:30', 'nothing'),
    ('2019/02/20 18:48:00', 'nothing'),

    # 23. iteration
    ('2019/01/13 18:50:30', 'nothing'),
    ('2019/01/13 18:51:00', 'nothing'),
    ('2019/02/04 09:43:00', 'nothing'),
    ('2019/02/10 10:34:00', 'nothing'),
    ('2019/02/10 10:34:30', 'nothing'),
    ('2019/02/21 18:02:00', 'nothing'),
    ('2019/02/21 18:02:30', 'nothing'),
    ('2019/02/21 18:03:00', 'nothing'),
    ('2019/03/25 19:22:30', 'nothing'),
    ('2019/03/25 19:23:00', 'nothing'),

    # 24. iteration
    ('2018/12/22 08:17:30', 'nothing'),
    ('2019/01/13 18:50:30', 'nothing'),
    ('2019/01/13 18:51:00', 'nothing'),
    ('2019/02/04 09:43:00', 'nothing'),
    ('2019/02/10 10:34:00', 'nothing'),
    ('2019/02/21 18:02:00', 'nothing'),
    ('2019/02/21 18:02:30', 'nothing'),
    ('2019/03/09 16:24:00', 'nothing'),
    ('2019/03/25 19:22:30', 'nothing'),
    ('2019/03/25 19:23:00', 'nothing'),

    # 25. iteration
    ('2019/01/13 18:50:30', 'nothing'),
    ('2019/01/13 18:51:00', 'nothing'),
    ('2019/01/20 21:25:00', 'nothing'),
    ('2019/01/20 21:25:30', 'nothing'),
    ('2019/01/20 21:26:00', 'nothing'),
    ('2019/01/20 21:26:30', 'nothing'),
    ('2019/02/10 10:34:00', 'nothing'),
    ('2019/02/13 22:10:00', 'nothing'),
    ('2019/02/21 18:02:00', 'nothing'),
    ('2019/02/21 18:02:30', 'nothing'),

    # 26. iteration
    ('2019/01/13 18:51:00', 'nothing'),
    ('2019/01/20 21:25:00', 'nothing'),
    ('2019/01/20 21:25:30', 'nothing'),
    ('2019/01/20 21:26:00', 'nothing'),
    ('2019/01/20 21:26:30', 'nothing'),
    ('2019/01/26 12:09:30', 'nothing'),
    ('2019/01/26 12:10:30', 'nothing'),
    ('2019/01/26 12:11:30', 'nothing'),
    ('2019/01/30 06:17:30', 'nothing'),
    ('2019/02/10 10:34:00', 'nothing'),

    # 27. iteration
    ('2018/12/07 15:35:00', 'nothing'),
    ('2019/01/13 18:51:00', 'nothing'),
    ('2019/01/20 21:25:00', 'nothing'),
    ('2019/01/20 21:25:30', 'nothing'),
    ('2019/01/20 21:26:00', 'nothing'),
    ('2019/02/13 22:09:00', 'nothing'),
    ('2019/02/13 22:10:00', 'nothing'),
    ('2019/02/21 18:02:30', 'nothing'),
    ('2019/02/25 20:41:30', 'nothing'),
    ('2019/03/02 12:56:30', 'nothing'),

    # 28. iteration
    ('2019/01/13 18:51:00', 'nothing'),
    ('2019/01/16 11:37:00', 'nothing'),
    ('2019/01/21 21:45:30', 'nothing'),
    ('2019/02/21 18:02:30', 'nothing'),
    ('2019/02/26 12:59:30', 'nothing'),
    ('2019/02/26 13:00:00', 'nothing'),
    ('2019/02/26 13:00:30', 'nothing'),
    ('2019/02/26 13:01:00', 'nothing'),
    ('2019/03/02 12:56:30', 'nothing'),
    ('2019/03/08 17:27:30', 'nothing'),

    # 29. iteration
    ('2019/01/13 18:51:00', 'nothing'),
    ('2019/01/20 21:25:00', 'nothing'),
    ('2019/01/20 21:26:00', 'nothing'),
    ('2019/02/21 18:02:30', 'nothing'),
    ('2019/02/26 12:59:30', 'nothing'),
    ('2019/02/26 13:00:00', 'nothing'),
    ('2019/02/26 13:00:30', 'nothing'),
    ('2019/02/26 13:01:00', 'nothing'),
    ('2019/02/27 16:04:30', 'nothing'),
    ('2019/03/02 12:56:30', 'nothing'),

    # 30. iteration
    ('2018/12/24 15:22:30', 'nothing'),
    ('2019/01/19 21:13:00', 'nothing'),
    ('2019/01/20 21:26:00', 'nothing'),
    ('2019/02/21 18:02:30', 'nothing'),
    ('2019/02/26 12:59:30', 'nothing'),
    ('2019/02/26 13:00:00', 'nothing'),
    ('2019/02/26 13:00:30', 'nothing'),
    ('2019/03/02 12:16:00', 'nothing'),
    ('2019/03/02 12:17:00', 'nothing'),
    ('2019/03/02 12:56:30', 'nothing'),

    # 31. iteration
    ('2019/01/28 22:02:00', 'nothing'),
    ('2019/02/26 12:59:30', 'nothing'),
    ('2019/02/26 13:00:00', 'nothing'),
    ('2019/02/26 13:00:30', 'nothing'),
    ('2019/03/02 12:16:00', 'nothing'),
    ('2019/03/02 12:17:00', 'nothing'),
    ('2019/03/02 12:56:30', 'nothing'),
    ('2019/03/05 08:32:00', 'nothing'),
    ('2019/03/25 22:22:30', 'nothing'),

    # 32. iteration
    ('2019/01/20 21:26:00', 'nothing'),
    ('2019/02/26 13:00:00', 'nothing'),
    ('2019/02/26 13:00:30', 'nothing'),
    ('2019/03/02 12:17:00', 'nothing'),
    ('2019/03/02 12:56:30', 'nothing'),
    ('2019/03/07 21:01:00', 'nothing'),

    # 33. iteration
    ('2019/02/26 12:59:30', 'nothing'),
    ('2019/02/26 13:00:00', 'nothing'),
    ('2019/02/26 13:00:30', 'nothing'),
    ('2019/03/02 12:17:00', 'nothing'),
    ('2019/03/02 12:56:30', 'nothing'),

    # 34. iteration
    ('2018/12/03 16:00:00', 'nothing'),
    ('2019/02/26 13:00:00', 'nothing'),
    ('2019/02/26 13:00:30', 'nothing'),
    ('2019/03/25 19:22:30', 'nothing'),

    # 35. iteration
    ('2019/01/20 21:26:00', 'nothing'),
    ('2019/01/20 21:26:30', 'nothing'),
    ('2019/02/21 18:02:30', 'nothing'),
    ('2019/02/26 13:00:00', 'nothing'),
    ('2019/02/26 13:00:30', 'nothing'),
    ('2019/03/21 08:02:00', 'nothing'),

    # 36. iteration
    ('2019/02/26 12:59:30', 'nothing'),
    ('2019/02/26 13:00:00', 'nothing'),
    ('2019/02/26 13:00:30', 'nothing'),
    ('2019/03/05 08:32:00', 'nothing'),
    ('2019/03/21 08:02:30', 'nothing'),

    # 37. iteration
    ('2019/01/20 21:26:00', 'nothing'),
    ('2019/01/20 21:26:30', 'nothing'),
    ('2019/02/10 21:28:30', 'nothing'),
    ('2019/02/26 13:00:30', 'nothing'),
    ('2019/03/21 08:02:00', 'nothing'),

    # 38. iteration
    ('2018/12/26 04:36:00', 'nothing'),
    ('2019/02/03 08:20:30', 'nothing'),
    ('2019/02/21 18:02:30', 'nothing'),
    ('2019/02/26 12:59:30', 'nothing'),
    ('2019/02/26 13:00:00', 'nothing'),
    ('2019/03/02 12:17:00', 'nothing'),

    # 39. iteration
    ('2019/01/21 21:45:30', 'nothing'),

    # 40. iteration
    ('2019/01/16 11:29:30', 'nothing'),
    ('2019/02/26 13:00:00', 'nothing'),

    # 41. iteration
    ('2018/12/03 16:00:00', 'nothing'),
]


def func(con, table_name, timestamp, row_selector, interval_selector, end=None):
    attrs = []
    columns = [
        'rh_in2_specific_g_kg',
        'rh_in2_absolute_g_m3',
        'temperature_in2_celsius']
    precision = 5

    for column in columns:
        for normalize in [False]:
            intervals_before = [x for x in range(0, 601, 15)]
            intervals_after = [x for x in range(0, 181, 15)]

            op = FirstDifferenceAttrA(con, table_name, row_selector, interval_selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=intervals_before,
                              intervals_after=intervals_after,
                              normalize=normalize,
                              enable_count=True,
                              prefix='',
                              selected_before=[intervals_before],
                              selected_after=[intervals_after])
            attrs += a + b

            pr = ''
            be, af = op.geometric_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.arithmetic_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.variance(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.standard_deviation(column, precision, b, a, pr)
            attrs += be + af

            # linearni posun
            op = FirstDifferenceAttrB(con, table_name, row_selector, interval_selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=intervals_before,
                              intervals_after=intervals_after,
                              normalize=normalize,
                              enable_count=True,
                              prefix='',
                              selected_before=[intervals_before],
                              selected_after=[intervals_after])
            attrs += a + b

            pr = 'B_linearne'
            be, af = op.geometric_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.arithmetic_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.variance(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.standard_deviation(column, precision, b, a, pr)
            attrs += be + af

            op = SecondDifferenceAttr(con, table_name, row_selector, interval_selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=intervals_before,
                              intervals_after=intervals_after,
                              normalize=normalize,
                              enable_count=True,
                              prefix='',
                              selected_before=[intervals_before],
                              selected_after=[intervals_after])
            attrs += a + b

            op = DifferenceBetweenRealLinear(con, table_name, row_selector, interval_selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=intervals_before,
                              intervals_after=intervals_after,
                              window_size_before=15 * 60, window_size_after=3 * 60,
                              prefix='')
            attrs += a + b

            # x^2 posun
            op = FirstDifferenceAttrB(con, table_name, row_selector, interval_selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=[x * x for x in range(4, 25, 1)],
                              intervals_after=[x * x for x in range(4, 14, 1)],
                              normalize=normalize,
                              enable_count=True,
                              prefix='_x2',
                              selected_before=[[x * x for x in range(4, 25, 1)]],
                              selected_after=[[x * x for x in range(4, 14, 1)]])
            attrs += a + b

            pr = 'B_x2'
            be, af = op.geometric_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.arithmetic_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.variance(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.standard_deviation(column, precision, b, a, pr)
            attrs += be + af

            op = SecondDifferenceAttr(con, table_name, row_selector, interval_selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=[x * x for x in range(4, 25, 1)],
                              intervals_after=[x * x for x in range(4, 14, 1)],
                              normalize=normalize,
                              enable_count=True,
                              prefix='_x2',
                              selected_before=[[x * x for x in range(4, 25, 1)]],
                              selected_after=[[x * x for x in range(4, 14, 1)]])
            attrs += a + b

            op = DifferenceBetweenRealLinear(con, table_name, row_selector, interval_selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=intervals_before,
                              intervals_after=intervals_after,
                              window_size_before=15 * 60, window_size_after=3 * 60,
                              prefix='_x2')
            attrs += a + b

            # x^3 posun
            op = FirstDifferenceAttrB(con, table_name, row_selector, interval_selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=[x * x * x for x in range(3, 9, 1)],
                              intervals_after=[x * x * x for x in range(3, 6, 1)],
                              normalize=normalize,
                              enable_count=True,
                              prefix='_x3',
                              selected_before=[[x * x * x for x in range(3, 9, 1)]],
                              selected_after=[[x * x * x for x in range(3, 6, 1)]])
            attrs += a + b

            pr = 'B_x3'
            be, af = op.geometric_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.arithmetic_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.variance(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.standard_deviation(column, precision, b, a, pr)
            attrs += be + af

            op = SecondDifferenceAttr(con, table_name, row_selector, interval_selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=[x * x * x for x in range(3, 9, 1)],
                              intervals_after=[x * x * x for x in range(3, 6, 1)],
                              normalize=normalize,
                              enable_count=True,
                              prefix='_x3',
                              selected_before=[[x * x * x for x in range(3, 9, 1)]],
                              selected_after=[[x * x * x for x in range(3, 6, 1)]])
            attrs += a + b

            op = DifferenceBetweenRealLinear(con, table_name, row_selector, interval_selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=intervals_before,
                              intervals_after=intervals_after,
                              window_size_before=15 * 60, window_size_after=3 * 60,
                              prefix='_x3')
            attrs += a + b

        op = InOutDiff(con, table_name, row_selector, interval_selector)
        b, a = op.execute(timestamp=timestamp, column='temperature_in2_celsius_diff', precision=precision,
                          intervals_before=[0],
                          intervals_after=[],
                          prefix='')
        attrs += b + a

        op = InOutDiff(con, table_name, row_selector, interval_selector)
        b, a = op.execute(timestamp=timestamp, column='rh_in2_specific_g_kg_diff', precision=precision,
                          intervals_before=[0],
                          intervals_after=[],
                          prefix='')
        attrs += b + a

        op = InOutDiff(con, table_name, row_selector, interval_selector)
        b, a = op.execute(timestamp=timestamp, column='rh_in2_absolute_g_m3_diff', precision=precision,
                          intervals_before=[0],
                          intervals_after=[],
                          prefix='')
        attrs += b + a

    return attrs


def training_set(events_file: str, no_event_time_shift: int, table_name: str):
    logging.info('start')

    # stiahnutie dat
    con = ConnectionUtil.create_con()
    storage = Storage(events_file, no_event_time_shift, table_name)
    d = storage.load_data(con, 0, 0, 'rh_in2_specific_g_kg')
    logging.info('downloaded events: %d' % len(d))

    # aplikovanie filtrov na eventy
    filtered = FilterUtil.only_valid_events(d)
    # filtered = FilterUtil.temperature_diff(filtered, 5, 100)
    # filtered = FilterUtil.temperature_out_max(filtered, 15)
    # filtered = FilterUtil.humidity(filtered, 6, 1.6, 100)
    logging.info('events after applying the filter: %d' % len(filtered))

    # selector pre data
    row_selector = CachedDiffRowWithIntervalSelector(con, table_name, 0, 0)
    interval_selector = SimpleIntervalSelector(con, table_name)

    # trenovacia mnozina
    logging.info('start computing of training set')
    training, tr_events = AttributeUtil.training_data(con, table_name, filtered, func,
                                                      row_selector, interval_selector, 'open')
    count = len(training)
    logging.info('training set contains %d events (%d records)' % (count / 2, count))

    training2 = AttributeUtil.additional_training_set(con, table_name, no_events_records, func,
                                                      row_selector, interval_selector)
    count2 = len(training2)
    logging.info('additional training set contains %d records' % count2)

    logging.info('end computing of training set')

    logging.info('start preparing file of training set')
    balanced = AttributeUtil.balance_set(training, training2)
    CSVUtil.create_csv_file(balanced, 'training.csv')
    logging.info('end preparing file of training set')


def testing_set(table_name: str, start, end, filename):
    logging.info('start')

    con = ConnectionUtil.create_con()
    interval_selector = SimpleIntervalSelector(con, table_name)

    logging.info('start computing of testing set')
    length = AttributeUtil.testing_data_with_write(con, table_name, start, end, 30, func,
                                                   None, interval_selector, 'open', filename)
    logging.info('testing set contains %d records' % length)
    logging.info('end computing of testing set')

    logging.info('end')


def testing_month(table_name, start):
    mesiac = 30 * 24 * 3600

    file_names = [
        '1_listopad.csv',
        '2_prosinec.csv',
        '3_leden.csv',
        '4_unor.csv',
    ]

    for file_name in file_names:
        testing_set(table_name, start, start + mesiac, file_name)
        start += mesiac


def generic_testing(directory):
    end = int(DateTimeUtil.local_time_str_to_utc('2019/04/29 18:00:00').timestamp())

    # David
    start = int(DateTimeUtil.local_time_str_to_utc('2019/04/03 18:00:00').timestamp())
    testing_set('measured_david', start, end, '{0}/gt_david.csv'.format(directory))

    # Martin
    start = int(DateTimeUtil.local_time_str_to_utc('2019/04/01 18:00:00').timestamp())
    testing_set('measured_martin', start, end, '{0}/gt_martin.csv'.format(directory))

    # Peto , februar, marec, april
    start = int(DateTimeUtil.local_time_str_to_utc('2018/10/07 18:00:00').timestamp())
    testing_set('measured_peto', start, end, '{0}/gt_peto.csv'.format(directory))

    # Klarka
    start = int(DateTimeUtil.local_time_str_to_utc('2018/11/26 06:00:00').timestamp())
    testing_set('measured_klarka', start, end, '{0}/gt_klarka.csv'.format(directory))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    # tabulka s CO2, ktora neprekroci hranicu 2000ppm
    table_name = 'measured_klarka'

    training_set('examples/events_klarka.json', -500, table_name)

    start = int(DateTimeUtil.local_time_str_to_utc('2018/11/26 06:00:00').timestamp())
    testing_set(table_name, start, start + 100, 'testing.csv')
    # testing_month(table_name, start)
    # generic_testing(".")
