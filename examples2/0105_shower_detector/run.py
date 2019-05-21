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
from dm.attrs.SecondDifferenceAttr import SecondDifferenceAttr
from dm.selectors.interval.SimpleIntervalSelector import SimpleIntervalSelector
from dm.selectors.row.CachedDiffRowWithIntervalSelector import CachedDiffRowWithIntervalSelector
import logging


no_events_records = [
    # 1. iteration
    ('2018/11/01 05:56:00', 'nothing'),
    ('2018/11/07 00:56:00', 'nothing'),
    ('2018/11/13 07:25:00', 'nothing'),
    ('2018/11/19 16:04:00', 'nothing'),
    ('2018/11/24 05:22:00', 'nothing'),
    ('2018/12/01 12:43:30', 'nothing'),
    ('2018/12/07 05:56:00', 'nothing'),
    ('2018/12/14 06:26:30', 'nothing'),
    ('2018/12/20 15:06:00', 'nothing'),
    ('2018/12/25 14:24:00', 'nothing'),

    # 2. iteration
    ('2018/11/01 18:41:00', 'nothing'),
    ('2018/11/07 17:26:30', 'nothing'),
    ('2018/11/14 22:54:00', 'nothing'),
    ('2018/11/19 13:37:30', 'nothing'),
    ('2018/11/26 18:13:00', 'nothing'),
    ('2018/12/01 11:14:30', 'nothing'),
    ('2018/12/07 05:56:00', 'nothing'),
    ('2018/12/14 06:26:30', 'nothing'),
    ('2018/12/19 20:59:00', 'nothing'),
    ('2018/12/25 12:12:00', 'nothing'),

    # 3. iteration
    ('2018/11/02 01:15:00', 'nothing'),
    ('2018/11/08 12:50:00', 'nothing'),
    ('2018/11/13 22:27:30', 'nothing'),
    ('2018/11/19 16:05:00', 'nothing'),
    ('2018/11/25 19:45:00', 'nothing'),
    ('2018/12/01 11:40:30', 'nothing'),
    ('2018/12/08 06:56:30', 'nothing'),
    ('2018/12/14 15:08:00', 'nothing'),
    ('2018/12/20 22:04:30', 'nothing'),
    ('2018/12/25 18:45:00', 'nothing'),

    # 4. iteration
    ('2018/11/03 09:26:30', 'nothing'),
    ('2018/11/08 23:15:30', 'nothing'),
    ('2018/11/13 22:27:30', 'nothing'),
    ('2018/11/19 05:02:30', 'nothing'),
    ('2018/11/27 14:11:30', 'nothing'),
    ('2018/12/02 14:51:30', 'nothing'),
    ('2018/12/06 23:18:30', 'nothing'),
    ('2018/12/14 06:26:30', 'nothing'),
    ('2018/12/21 17:01:00', 'nothing'),
    ('2018/12/27 05:54:30', 'nothing'),

    # 5. iteration
    ('2018/11/04 18:26:30', 'nothing'),
    ('2018/11/09 21:15:30', 'nothing'),
    ('2018/11/13 22:27:30', 'nothing'),
    ('2018/11/19 16:17:30', 'nothing'),
    ('2018/11/27 06:27:30', 'nothing'),
    ('2018/12/01 14:19:00', 'nothing'),
    ('2018/12/06 16:49:30', 'nothing'),
    ('2018/12/14 06:26:30', 'nothing'),
    ('2018/12/20 22:36:00', 'nothing'),
    ('2018/12/27 22:49:00', 'nothing'),

    # 6. iteration
    ('2018/11/03 15:12:00', 'nothing'),
    ('2018/11/07 05:36:30', 'nothing'),
    ('2018/11/12 06:45:30', 'nothing'),
    ('2018/11/19 05:00:30', 'nothing'),
    ('2018/11/25 09:21:00', 'nothing'),
    ('2018/12/04 10:15:30', 'nothing'),
    ('2018/12/06 20:47:30', 'nothing'),
    ('2018/12/14 06:26:30', 'nothing'),
    ('2018/12/19 18:09:00', 'nothing'),
    ('2018/12/30 08:01:00', 'nothing'),

    # 7. iteration
    ('2018/11/05 23:10:30', 'nothing'),
    ('2018/11/12 18:39:30', 'nothing'),
    ('2018/11/17 12:23:00', 'nothing'),
    ('2018/11/21 18:28:30', 'nothing'),
    ('2018/11/28 06:09:30', 'nothing'),
    ('2018/12/04 10:15:30', 'nothing'),
    ('2018/12/18 18:13:00', 'nothing'),
    ('2018/12/19 18:09:30', 'nothing'),
    ('2018/12/24 08:02:30', 'nothing'),
    ('2018/12/30 08:16:00', 'nothing'),

    # 8. iteration
    ('2018/11/08 22:53:30', 'nothing'),
    ('2018/11/13 06:44:30', 'nothing'),
    ('2018/11/17 19:56:00', 'nothing'),
    ('2018/12/01 11:00:30', 'nothing'),
    ('2018/12/05 09:13:00', 'nothing'),
    ('2018/12/15 15:30:30', 'nothing'),
    ('2018/12/20 18:54:30', 'nothing'),
    ('2018/12/22 06:36:30', 'nothing'),
    ('2018/12/27 05:54:30', 'nothing'),
    ('2018/12/30 08:16:30', 'nothing'),

    # 9. iteration
    ('2018/11/08 22:53:00', 'nothing'),
    ('2018/11/13 05:56:30', 'nothing'),
    ('2018/11/18 15:55:30', 'nothing'),
    ('2018/11/24 16:12:30', 'nothing'),
    ('2018/11/28 22:56:00', 'nothing'),
    ('2018/12/03 05:59:00', 'nothing'),
    ('2018/12/05 05:31:00', 'nothing'),
    ('2018/12/14 06:26:30', 'nothing'),
    ('2018/12/25 18:45:00', 'nothing'),
    ('2018/12/30 08:08:30', 'nothing'),

    # 10. iteration
    ('2018/11/04 18:26:00', 'nothing'),
    ('2018/11/08 22:52:30', 'nothing'),
    ('2018/11/13 05:56:30', 'nothing'),
    ('2018/11/22 05:08:30', 'nothing'),
    ('2018/11/25 09:20:00', 'nothing'),
    ('2018/12/01 09:48:30', 'nothing'),
    ('2018/12/06 22:55:00', 'nothing'),
    ('2018/12/15 15:55:00', 'nothing'),
    ('2018/12/20 22:40:30', 'nothing'),
    ('2018/12/27 19:47:00', 'nothing'),

    # 11. iteration
    ('2018/11/01 18:33:30', 'nothing'),
    ('2018/11/06 02:30:00', 'nothing'),
    ('2018/11/13 05:56:30', 'nothing'),
    ('2018/11/25 19:45:30', 'nothing'),
    ('2018/11/28 23:20:00', 'nothing'),
    ('2018/12/05 05:31:00', 'nothing'),
    ('2018/12/06 20:46:00', 'nothing'),
    ('2018/12/19 18:09:00', 'nothing'),
    ('2018/12/20 22:36:00', 'nothing'),
    ('2018/12/30 08:01:00', 'nothing'),

    # 12. iteration
    ('2018/11/02 19:16:00', 'nothing'),
    ('2018/11/09 19:23:00', 'nothing'),
    ('2018/11/18 15:55:00', 'nothing'),
    ('2018/11/21 22:17:30', 'nothing'),
    ('2018/12/05 05:31:00', 'nothing'),
    ('2018/12/06 20:47:30', 'nothing'),
    ('2018/12/14 06:26:30', 'nothing'),
    ('2018/12/15 15:54:30', 'nothing'),
    ('2018/12/19 18:46:30', 'nothing'),
    ('2018/12/28 06:03:00', 'nothing'),

    # 13. iteration
    ('2018/11/01 18:21:00', 'nothing'),
    ('2018/11/07 22:14:30', 'nothing'),
    ('2018/11/13 18:55:30', 'nothing'),
    ('2018/11/19 21:31:30', 'nothing'),
    ('2018/11/25 17:12:30', 'nothing'),
    ('2018/12/01 06:11:00', 'nothing'),
    ('2018/12/07 20:35:00', 'nothing'),
    ('2018/12/13 20:58:00', 'nothing'),
    ('2018/12/19 18:08:00', 'nothing'),
    ('2018/12/25 18:33:00', 'nothing'),

    # 14. iteration
    ('2018/11/01 18:21:00', 'nothing'),
    ('2018/11/07 22:15:00', 'nothing'),
    ('2018/11/13 18:55:00', 'nothing'),
    ('2018/11/19 06:10:00', 'nothing'),
    ('2018/11/25 09:21:00', 'nothing'),
    ('2018/12/01 22:52:30', 'nothing'),
    ('2018/12/07 20:34:30', 'nothing'),
    ('2018/12/13 19:46:00', 'nothing'),
    ('2018/12/19 06:02:00', 'nothing'),
    ('2018/12/25 18:33:00', 'nothing'),

    # 15. iteration
    ('2018/11/01 23:09:00', 'nothing'),
    ('2018/11/07 22:15:00', 'nothing'),
    ('2018/11/13 18:55:00', 'nothing'),
    ('2018/11/19 07:32:30', 'nothing'),
    ('2018/11/25 17:12:00', 'nothing'),
    ('2018/12/01 14:19:00', 'nothing'),
    ('2018/12/07 20:44:30', 'nothing'),
    ('2018/12/13 20:58:00', 'nothing'),
    ('2018/12/19 18:08:00', 'nothing'),
    ('2018/12/25 18:33:30', 'nothing'),

    # 16. iteration
    ('2018/11/01 23:08:00', 'nothing'),
    ('2018/11/07 22:14:30', 'nothing'),
    ('2018/11/13 18:55:00', 'nothing'),
    ('2018/11/18 15:56:00', 'nothing'),
    ('2018/11/25 17:12:00', 'nothing'),
    ('2018/12/01 14:19:00', 'nothing'),
    ('2018/12/07 18:40:00', 'nothing'),
    ('2018/12/13 19:47:30', 'nothing'),
    ('2018/12/19 16:27:30', 'nothing'),
    ('2018/12/25 18:33:30', 'nothing'),

    # 17. iteration
    ('2018/11/01 18:53:00', 'nothing'),
    ('2018/11/07 22:14:30', 'nothing'),
    ('2018/11/13 18:54:30', 'nothing'),
    ('2018/11/19 16:14:30', 'nothing'),
    ('2018/11/25 09:19:00', 'nothing'),
    ('2018/12/01 14:19:30', 'nothing'),
    ('2018/12/07 10:57:00', 'nothing'),
    ('2018/12/13 19:45:30', 'nothing'),
    ('2018/12/19 18:27:30', 'nothing'),
    ('2018/12/26 06:15:00', 'nothing'),

    # 18. iteration
    ('2018/11/01 18:53:30', 'nothing'),
    ('2018/11/07 22:15:00', 'nothing'),
    ('2018/11/13 06:45:00', 'nothing'),
    ('2018/11/19 16:21:00', 'nothing'),
    ('2018/11/25 17:12:30', 'nothing'),
    ('2018/12/01 09:50:00', 'nothing'),
    ('2018/12/06 20:45:30', 'nothing'),
    ('2018/12/14 05:46:30', 'nothing'),
    ('2018/12/19 17:42:30', 'nothing'),
    ('2018/12/25 18:33:00', 'nothing'),

    # 19. iteration
    ('2018/11/01 18:54:00', 'nothing'),
    ('2018/11/07 17:26:30', 'nothing'),
    ('2018/11/13 00:54:30', 'nothing'),
    ('2018/11/19 06:16:30', 'nothing'),
    ('2018/11/26 18:29:30', 'nothing'),
    ('2018/12/01 10:58:30', 'nothing'),
    ('2018/12/07 18:38:00', 'nothing'),
    ('2018/12/13 19:45:30', 'nothing'),
    ('2018/12/19 18:29:30', 'nothing'),
    ('2018/12/25 10:12:00', 'nothing'),

    # 20. iteration
    ('2018/11/01 18:53:30', 'nothing'),
    ('2018/11/07 22:15:00', 'nothing'),
    ('2018/11/13 07:25:00', 'nothing'),
    ('2018/11/19 06:16:30', 'nothing'),
    ('2018/11/25 09:21:30', 'nothing'),
    ('2018/12/01 14:19:00', 'nothing'),
    ('2018/12/07 20:35:00', 'nothing'),
    ('2018/12/13 19:46:00', 'nothing'),
    ('2018/12/19 16:27:30', 'nothing'),
    ('2018/12/25 10:11:30', 'nothing'),

    # 21. iteration
    ('2018/11/01 18:20:30', 'nothing'),
    ('2018/11/07 22:13:00', 'nothing'),
    ('2018/11/13 19:17:00', 'nothing'),
    ('2018/11/17 09:51:30', 'nothing'),
    ('2018/11/25 17:14:00', 'nothing'),
    ('2018/12/01 14:25:00', 'nothing'),
    ('2018/12/07 20:35:00', 'nothing'),
    ('2018/12/13 20:58:00', 'nothing'),
    ('2018/12/19 17:42:30', 'nothing'),
    ('2018/12/25 10:12:00', 'nothing'),

    # 22. iteration
    ('2018/11/01 18:53:30', 'nothing'),
    ('2018/11/07 17:26:30', 'nothing'),
    ('2018/11/13 18:54:00', 'nothing'),
    ('2018/11/19 21:31:00', 'nothing'),
    ('2018/11/26 18:29:00', 'nothing'),
    ('2018/12/01 09:48:30', 'nothing'),
    ('2018/12/07 20:35:30', 'nothing'),
    ('2018/12/13 20:58:30', 'nothing'),
    ('2018/12/19 18:45:30', 'nothing'),
    ('2018/12/26 06:15:00', 'nothing'),

    # 23. iteration
    ('2018/11/01 18:53:30', 'nothing'),
    ('2018/11/07 17:26:30', 'nothing'),
    ('2018/11/13 07:25:00', 'nothing'),
    ('2018/11/19 21:32:30', 'nothing'),
    ('2018/11/25 22:19:30', 'nothing'),
    ('2018/12/01 22:53:00', 'nothing'),
    ('2018/12/07 20:34:30', 'nothing'),
    ('2018/12/13 20:58:00', 'nothing'),
    ('2018/12/19 09:30:00', 'nothing'),
    ('2018/12/25 18:33:00', 'nothing'),

    # 24. iteration
    ('2018/11/01 18:20:00', 'nothing'),
    ('2018/11/07 22:15:30', 'nothing'),
    ('2018/11/13 19:16:30', 'nothing'),
    ('2018/11/19 06:16:30', 'nothing'),
    ('2018/11/25 09:14:30', 'nothing'),
    ('2018/12/01 09:48:00', 'nothing'),
    ('2018/12/07 20:34:30', 'nothing'),
    ('2018/12/13 20:58:30', 'nothing'),
    ('2018/12/16 15:08:30', 'nothing'),
    ('2018/12/25 18:33:00', 'nothing'),

    # 25. iteration
    ('2018/11/01 18:20:30', 'nothing'),
    ('2018/11/07 17:26:30', 'nothing'),
    ('2018/11/13 19:18:00', 'nothing'),
    ('2018/11/19 21:18:30', 'nothing'),
    ('2018/11/26 19:58:30', 'nothing'),
    ('2018/12/01 06:37:30', 'nothing'),
    ('2018/12/07 20:34:30', 'nothing'),
    ('2018/12/13 20:58:30', 'nothing'),
    ('2018/12/19 21:38:00', 'nothing'),
    ('2018/12/25 18:33:30', 'nothing'),

    # 26. iteration
    ('2018/11/01 18:20:00', 'nothing'),
    ('2018/11/07 17:26:30', 'nothing'),
    ('2018/11/15 09:56:30', 'nothing'),
    ('2018/11/19 18:15:00', 'nothing'),
    ('2018/11/25 19:04:30', 'nothing'),
    ('2018/12/01 10:57:00', 'nothing'),
    ('2018/12/07 20:35:00', 'nothing'),
    ('2018/12/13 21:08:30', 'nothing'),
    ('2018/12/19 18:08:30', 'nothing'),
    ('2018/12/25 08:47:00', 'nothing'),

    # 27. iteration
    ('2018/11/01 18:20:00', 'nothing'),
    ('2018/11/07 22:14:00', 'nothing'),
    ('2018/11/13 18:53:30', 'nothing'),
    ('2018/11/17 12:23:30', 'nothing'),
    ('2018/11/26 19:59:30', 'nothing'),
    ('2018/12/01 10:57:30', 'nothing'),
    ('2018/12/07 20:34:30', 'nothing'),
    ('2018/12/14 23:03:00', 'nothing'),
    ('2018/12/19 18:09:00', 'nothing'),
    ('2018/12/25 18:33:00', 'nothing'),

    # 28. iteration
    ('2018/11/01 18:20:00', 'nothing'),
    ('2018/11/07 17:26:30', 'nothing'),
    ('2018/11/12 20:12:00', 'nothing'),
    ('2018/11/19 16:16:30', 'nothing'),
    ('2018/11/26 06:41:30', 'nothing'),
    ('2018/12/01 06:37:30', 'nothing'),
    ('2018/12/07 20:35:00', 'nothing'),
    ('2018/12/14 07:01:00', 'nothing'),
    ('2018/12/19 17:42:00', 'nothing'),
    ('2018/12/24 18:51:00', 'nothing'),

    # 29. iteration
    ('2018/11/01 18:20:00', 'nothing'),
    ('2018/11/07 17:26:30', 'nothing'),
    ('2018/11/13 19:17:00', 'nothing'),
    ('2018/11/19 21:30:30', 'nothing'),
    ('2018/11/26 19:58:30', 'nothing'),
    ('2018/12/01 14:18:30', 'nothing'),
    ('2018/12/07 20:34:30', 'nothing'),
    ('2018/12/13 20:58:00', 'nothing'),
    ('2018/12/19 16:27:30', 'nothing'),
    ('2018/12/25 08:00:30', 'nothing'),

    # 30. iteration
    ('2018/11/01 18:20:00', 'nothing'),
    ('2018/11/07 17:26:30', 'nothing'),
    ('2018/11/13 18:53:00', 'nothing'),
    ('2018/11/19 06:09:30', 'nothing'),
    ('2018/11/25 09:17:30', 'nothing'),
    ('2018/12/01 12:31:30', 'nothing'),
    ('2018/12/08 19:04:30', 'nothing'),
    ('2018/12/13 20:58:00', 'nothing'),
    ('2018/12/19 17:42:00', 'nothing'),
    ('2018/12/25 08:00:00', 'nothing'),

    # 31. iteration
    ('2018/11/01 18:42:00', 'nothing'),
    ('2018/11/06 11:24:30', 'nothing'),
    ('2018/11/13 18:53:00', 'nothing'),
    ('2018/11/19 06:10:00', 'nothing'),
    ('2018/11/23 17:12:30', 'nothing'),
    ('2018/12/01 16:50:00', 'nothing'),
    ('2018/12/07 18:50:00', 'nothing'),
    ('2018/12/13 21:08:30', 'nothing'),
    ('2018/12/20 18:37:30', 'nothing'),
    ('2018/12/24 19:00:30', 'nothing'),

    # 32. iteration
    ('2018/11/01 18:20:00', 'nothing'),
    ('2018/11/09 19:14:00', 'nothing'),
    ('2018/11/12 20:12:00', 'nothing'),
    ('2018/11/19 21:31:00', 'nothing'),
    ('2018/11/26 19:58:30', 'nothing'),
    ('2018/12/01 14:19:00', 'nothing'),
    ('2018/12/07 20:35:00', 'nothing'),
    ('2018/12/14 06:26:30', 'nothing'),
    ('2018/12/20 22:03:30', 'nothing'),
    ('2018/12/27 23:54:30', 'nothing'),

    # 33. iteration
    ('2018/11/04 13:25:30', 'nothing'),
    ('2018/11/09 19:22:30', 'nothing'),
    ('2018/11/14 20:52:00', 'nothing'),
    ('2018/11/19 21:32:00', 'nothing'),
    ('2018/11/26 06:41:30', 'nothing'),
    ('2018/12/02 06:20:30', 'nothing'),
    ('2018/12/08 19:15:00', 'nothing'),
    ('2018/12/14 17:58:30', 'nothing'),
    ('2018/12/19 18:29:00', 'nothing'),
    ('2018/12/26 21:50:30', 'nothing'),

    # 34. iteration
    ('2018/11/01 18:52:30', 'nothing'),
    ('2018/11/08 04:08:00', 'nothing'),
    ('2018/11/12 20:12:00', 'nothing'),
    ('2018/11/21 22:01:30', 'nothing'),
    ('2018/11/26 18:31:30', 'nothing'),
    ('2018/12/02 06:49:30', 'nothing'),
    ('2018/12/08 21:31:30', 'nothing'),
    ('2018/12/14 23:03:00', 'nothing'),
    ('2018/12/19 17:42:00', 'nothing'),
    ('2018/12/26 19:18:30', 'nothing'),

    # 35. iteration
    ('2018/11/04 13:25:30', 'nothing'),
    ('2018/11/08 18:57:30', 'nothing'),
    ('2018/11/15 06:49:00', 'nothing'),
    ('2018/11/19 18:21:30', 'nothing'),
    ('2018/11/26 06:41:30', 'nothing'),
    ('2018/12/01 06:37:00', 'nothing'),
    ('2018/12/07 18:37:30', 'nothing'),
    ('2018/12/13 19:45:00', 'nothing'),
    ('2018/12/19 17:42:30', 'nothing'),
    ('2018/12/26 06:37:00', 'nothing'),

    # 36. iteration
    ('2018/11/01 18:52:30', 'nothing'),
    ('2018/11/09 19:14:00', 'nothing'),
    ('2018/11/17 12:23:30', 'nothing'),
    ('2018/11/21 19:12:00', 'nothing'),
    ('2018/11/26 18:31:00', 'nothing'),
    ('2018/12/03 22:19:00', 'nothing'),
    ('2018/12/14 06:26:30', 'nothing'),
    ('2018/12/21 11:06:00', 'nothing'),
    ('2018/12/26 19:18:00', 'nothing'),
    ('2018/12/30 08:19:30', 'nothing'),

    # 37. iteration
    ('2018/11/01 18:54:00', 'nothing'),
    ('2018/11/09 21:17:00', 'nothing'),
    ('2018/11/12 20:12:00', 'nothing'),
    ('2018/11/19 21:31:30', 'nothing'),
    ('2018/11/24 15:55:30', 'nothing'),
    ('2018/12/01 06:37:30', 'nothing'),
    ('2018/12/07 18:37:30', 'nothing'),
    ('2018/12/13 19:45:00', 'nothing'),
    ('2018/12/18 20:17:30', 'nothing'),
    ('2018/12/26 06:37:00', 'nothing'),

    # 38. iteration
    ('2018/11/01 18:53:30', 'nothing'),
    ('2018/11/08 22:53:30', 'nothing'),
    ('2018/11/12 20:12:00', 'nothing'),
    ('2018/11/21 22:17:30', 'nothing'),
    ('2018/11/27 19:06:00', 'nothing'),
    ('2018/12/01 12:31:30', 'nothing'),
    ('2018/12/05 23:16:30', 'nothing'),
    ('2018/12/14 06:26:30', 'nothing'),
    ('2018/12/18 20:17:30', 'nothing'),
    ('2018/12/27 23:54:30', 'nothing'),

    # 39. iteration
    ('2018/11/01 18:54:00', 'nothing'),
    ('2018/11/08 18:57:30', 'nothing'),
    ('2018/11/15 06:49:00', 'nothing'),
    ('2018/11/21 19:12:00', 'nothing'),
    ('2018/11/25 09:19:30', 'nothing'),
    ('2018/12/01 22:52:30', 'nothing'),
    ('2018/12/07 18:37:00', 'nothing'),
    ('2018/12/13 19:45:00', 'nothing'),
    ('2018/12/19 17:42:00', 'nothing'),
    ('2018/12/27 23:54:30', 'nothing'),

    # 40. iteration
    ('2018/11/04 02:34:30', 'nothing'),
    ('2018/11/07 09:21:00', 'nothing'),
    ('2018/11/13 06:44:30', 'nothing'),
    ('2018/11/19 21:32:30', 'nothing'),
    ('2018/11/25 09:16:30', 'nothing'),
    ('2018/12/01 22:52:00', 'nothing'),
    ('2018/12/06 20:46:00', 'nothing'),
    ('2018/12/14 23:03:00', 'nothing'),
    ('2018/12/20 18:27:30', 'nothing'),
    ('2018/12/28 20:25:30', 'nothing'),

    # 41. iteration
    ('2018/11/01 18:53:30', 'nothing'),
    ('2018/11/08 18:57:30', 'nothing'),
    ('2018/11/12 20:12:00', 'nothing'),
    ('2018/11/22 17:59:00', 'nothing'),
    ('2018/11/26 06:40:30', 'nothing'),
    ('2018/12/01 06:37:30', 'nothing'),
    ('2018/12/06 20:46:30', 'nothing'),
    ('2018/12/13 19:44:30', 'nothing'),
    ('2018/12/19 17:42:00', 'nothing'),
    ('2018/12/27 23:54:30', 'nothing'),

    # 42. iteration
    ('2018/11/05 18:43:30', 'nothing'),
    ('2018/11/11 22:40:00', 'nothing'),
    ('2018/11/15 06:40:30', 'nothing'),
    ('2018/11/21 22:02:00', 'nothing'),
    ('2018/11/28 06:09:00', 'nothing'),
    ('2018/12/01 06:37:30', 'nothing'),
    ('2018/12/05 23:29:00', 'nothing'),
    ('2018/12/14 18:00:00', 'nothing'),
    ('2018/12/19 17:42:00', 'nothing'),
    ('2018/12/28 20:26:00', 'nothing'),

    # 43. iteration
    ('2018/11/05 18:43:30', 'nothing'),
    ('2018/11/12 20:12:00', 'nothing'),
    ('2018/11/22 17:59:00', 'nothing'),
    ('2018/11/26 06:41:00', 'nothing'),
    ('2018/11/30 19:15:00', 'nothing'),
    ('2018/12/03 22:18:30', 'nothing'),
    ('2018/12/09 18:48:00', 'nothing'),
    ('2018/12/18 19:41:00', 'nothing'),
    ('2018/12/26 19:18:00', 'nothing'),
    ('2018/12/30 21:36:30', 'nothing'),

    # 44. iteration
    ('2018/11/02 05:12:30', 'nothing'),
    ('2018/11/09 21:16:30', 'nothing'),
    ('2018/11/17 12:22:30', 'nothing'),
    ('2018/11/22 05:08:00', 'nothing'),
    ('2018/11/28 23:19:30', 'nothing'),
    ('2018/12/02 06:55:00', 'nothing'),
    ('2018/12/07 18:37:00', 'nothing'),
    ('2018/12/16 14:16:00', 'nothing'),
    ('2018/12/21 11:06:00', 'nothing'),
    ('2018/12/27 23:54:30', 'nothing'),

    # 45. iteration
    ('2018/11/05 18:43:30', 'nothing'),
    ('2018/11/15 06:49:0', 'nothing'),
    ('2018/11/21 19:12:00', 'nothing'),
    ('2018/11/24 15:55:30', 'nothing'),
    ('2018/11/27 18:47:30', 'nothing'),
    ('2018/12/06 20:46:30', 'nothing'),
    ('2018/12/09 18:48:00', 'nothing'),
    ('2018/12/19 17:42:00', 'nothing'),
    ('2018/12/20 18:54:00', 'nothing'),
    ('2018/12/27 19:57:00', 'nothing'),

    # 46. iteration
    ('2018/11/05 18:43:30', 'nothing'),
    ('2018/11/19 21:31:30', 'nothing'),
    ('2018/11/21 07:34:00', 'nothing'),
    ('2018/11/27 06:27:30', 'nothing'),
    ('2018/11/28 22:44:00', 'nothing'),
    ('2018/12/02 06:49:30', 'nothing'),
    ('2018/12/07 18:38:00', 'nothing'),
    ('2018/12/09 19:00:30', 'nothing'),
    ('2018/12/20 18:27:30', 'nothing'),
    ('2018/12/27 08:16:30', 'nothing'),

    # 47. iteration
    ('2018/11/04 13:25:30', 'nothing'),
    ('2018/11/05 23:11:00', 'nothing'),
    ('2018/11/21 07:34:30', 'nothing'),
    ('2018/11/27 18:47:30', 'nothing'),
    ('2018/11/28 22:45:00', 'nothing'),
    ('2018/12/01 06:00:30', 'nothing'),
    ('2018/12/05 09:13:00', 'nothing'),
    ('2018/12/19 17:42:00', 'nothing'),
    ('2018/12/20 18:27:30', 'nothing'),
    ('2018/12/27 08:17:00', 'nothing'),

    # 48. iteration
    ('2018/11/05 18:43:30', 'nothing'),
    ('2018/11/08 18:57:30', 'nothing'),
    ('2018/11/13 19:17:30', 'nothing'),
    ('2018/11/21 06:04:30', 'nothing'),
    ('2018/11/27 14:12:30', 'nothing'),
    ('2018/12/01 06:00:30', 'nothing'),
    ('2018/12/04 22:51:00', 'nothing'),
    ('2018/12/14 06:26:30', 'nothing'),
    ('2018/12/23 11:54:30', 'nothing'),
    ('2018/12/27 19:57:00', 'nothing'),

    # 49. iteration
    ('2018/11/02 05:12:30', 'nothing'),
    ('2018/11/05 18:43:30', 'nothing'),
    ('2018/11/15 06:40:30', 'nothing'),
    ('2018/11/21 07:34:30', 'nothing'),
    ('2018/11/28 23:20:00', 'nothing'),
    ('2018/12/03 22:18:00', 'nothing'),
    ('2018/12/09 19:00:30', 'nothing'),
    ('2018/12/18 19:41:00', 'nothing'),
    ('2018/12/21 10:51:00', 'nothing'),
    ('2018/12/28 20:26:00', 'nothing'),

    # 50. iteration
    ('2018/11/04 17:22:00', 'nothing'),
    ('2018/11/22 17:59:00', 'nothing'),
    ('2018/11/27 18:46:00', 'nothing'),
    ('2018/11/30 21:23:00', 'nothing'),
    ('2018/12/04 06:48:00', 'nothing'),
    ('2018/12/05 23:17:00', 'nothing'),
    ('2018/12/06 20:47:00', 'nothing'),
    ('2018/12/19 17:42:00', 'nothing'),
    ('2018/12/21 18:35:30', 'nothing'),
    ('2018/12/27 08:17:00', 'nothing'),

    # 51. iteration
    ('2018/11/05 18:43:30', 'nothing'),
    ('2018/11/13 19:18:00', 'nothing'),
    ('2018/11/21 07:34:00', 'nothing'),
    ('2018/11/28 23:19:30', 'nothing'),
    ('2018/11/30 21:23:00', 'nothing'),
    ('2018/12/05 09:12:30', 'nothing'),
    ('2018/12/09 22:26:00', 'nothing'),
    ('2018/12/19 18:44:30', 'nothing'),
    ('2018/12/26 06:36:00', 'nothing'),
    ('2018/12/27 19:57:30', 'nothing'),

    # 52. iteration
    ('2018/11/02 05:12:30', 'nothing'),
    ('2018/11/05 18:43:30', 'nothing'),
    ('2018/11/21 07:34:00', 'nothing'),
    ('2018/11/27 06:26:30', 'nothing'),
    ('2018/11/28 23:19:30', 'nothing'),
    ('2018/12/05 09:12:30', 'nothing'),
    ('2018/12/09 22:26:00', 'nothing'),
    ('2018/12/21 10:50:30', 'nothing'),
    ('2018/12/26 06:36:00', 'nothing'),
    ('2018/12/27 19:57:00', 'nothing'),

    # 53. iteration
    ('2018/11/02 05:12:00', 'nothing'),
    ('2018/11/21 06:53:00', 'nothing'),
    ('2018/11/27 06:27:30', 'nothing'),
    ('2018/11/28 22:44:00', 'nothing'),
    ('2018/12/01 22:52:00', 'nothing'),
    ('2018/12/03 22:19:00', 'nothing'),
    ('2018/12/08 21:31:30', 'nothing'),
    ('2018/12/20 18:27:00', 'nothing'),
    ('2018/12/26 21:50:30', 'nothing'),
    ('2018/12/28 23:26:30', 'nothing'),

    # 54. iteration
    ('2018/11/02 05:12:00', 'nothing'),
    ('2018/11/13 19:17:00', 'nothing'),
    ('2018/11/21 06:53:30', 'nothing'),
    ('2018/11/27 18:50:30', 'nothing'),
    ('2018/11/30 21:23:00', 'nothing'),
    ('2018/12/01 22:53:00', 'nothing'),
    ('2018/12/07 18:38:00', 'nothing'),
    ('2018/12/09 22:26:30', 'nothing'),
    ('2018/12/13 19:43:00', 'nothing'),
    ('2018/12/27 19:57:00', 'nothing'),

    # 55. iteration
    ('2018/11/04 17:22:30', 'nothing'),
    ('2018/11/21 06:53:00', 'nothing'),
    ('2018/11/26 06:41:30', 'nothing'),
    ('2018/11/28 22:55:00', 'nothing'),
    ('2018/12/01 22:53:00', 'nothing'),
    ('2018/12/04 20:51:00', 'nothing'),
    ('2018/12/09 19:02:00', 'nothing'),
    ('2018/12/14 18:10:30', 'nothing'),
    ('2018/12/21 10:50:30', 'nothing'),
    ('2018/12/27 19:57:00', 'nothing'),

    # 56. iteration
    ('2018/11/02 05:12:30', 'nothing'),
    ('2018/11/04 17:23:00', 'nothing'),
    ('2018/11/15 06:40:30', 'nothing'),
    ('2018/11/21 06:53:00', 'nothing'),
    ('2018/11/27 18:51:00', 'nothing'),
    ('2018/11/28 22:56:00', 'nothing'),
    ('2018/12/04 06:48:30', 'nothing'),
    ('2018/12/06 20:47:30', 'nothing'),
    ('2018/12/09 22:26:30', 'nothing'),
    ('2018/12/27 08:17:00', 'nothing'),

    # 57. iteration
    ('2018/11/01 18:53:00', 'nothing'),
    ('2018/11/06 19:11:00', 'nothing'),
    ('2018/11/22 20:40:00', 'nothing'),
    ('2018/11/27 18:51:30', 'nothing'),
    ('2018/12/01 19:12:00', 'nothing'),
    ('2018/12/05 23:16:30', 'nothing'),
    ('2018/12/09 22:26:30', 'nothing'),
    ('2018/12/18 20:17:30', 'nothing'),
    ('2018/12/19 17:42:00', 'nothing'),
    ('2018/12/27 08:16:30', 'nothing'),

    # 58. iteration
    ('2018/11/02 05:12:00', 'nothing'),
    ('2018/11/06 07:03:30', 'nothing'),
    ('2018/11/11 11:32:30', 'nothing'),
    ('2018/11/15 09:53:00', 'nothing'),
    ('2018/11/22 05:00:00', 'nothing'),
    ('2018/11/30 21:22:30', 'nothing'),
    ('2018/12/02 07:00:30', 'nothing'),
    ('2018/12/08 21:32:00', 'nothing'),
    ('2018/12/13 19:45:00', 'nothing'),
    ('2018/12/27 19:57:00', 'nothing'),

    # 59. iteration
    ('2018/11/02 05:12:00', 'nothing'),
    ('2018/11/06 19:10:30', 'nothing'),
    ('2018/11/21 06:53:30', 'nothing'),
    ('2018/11/28 22:44:00', 'nothing'),
    ('2018/12/01 22:52:00', 'nothing'),
    ('2018/12/09 22:26:30', 'nothing'),
    ('2018/12/16 16:45:30', 'nothing'),
    ('2018/12/18 18:50:30', 'nothing'),
    ('2018/12/21 10:51:00', 'nothing'),
    ('2018/12/28 20:25:30', 'nothing'),

    # 60. iteration
    ('2018/11/02 05:12:30', 'nothing'),
    ('2018/11/06 19:10:30', 'nothing'),
    ('2018/11/22 20:40:30', 'nothing'),
    ('2018/11/27 18:51:00', 'nothing'),
    ('2018/11/28 06:38:30', 'nothing'),
    ('2018/12/02 07:00:30', 'nothing'),
    ('2018/12/09 22:26:30', 'nothing'),
    ('2018/12/14 18:10:00', 'nothing'),
    ('2018/12/19 18:45:30', 'nothing'),
    ('2018/12/21 10:51:30', 'nothing'),

    # 61. iteration
    ('2018/11/01 18:53:00', 'nothing'),
    ('2018/11/02 05:12:30', 'nothing'),
    ('2018/11/06 19:10:30', 'nothing'),
    ('2018/11/22 20:40:00', 'nothing'),
    ('2018/11/27 18:48:00', 'nothing'),
    ('2018/12/01 19:11:30', 'nothing'),
    ('2018/12/04 20:51:00', 'nothing'),
    ('2018/12/21 10:50:30', 'nothing'),
    ('2018/12/14 18:09:30', 'nothing'),
    ('2018/12/19 18:46:00', 'nothing'),
]


def func(con, table_name, timestamp, row_selector, interval_selector, end=None):
    attrs = []
    columns = [
        'rh_in_specific_g_kg',
        'rh_in_absolute_g_m3',
        'temperature_in_celsius']
    precision = 5

    for column in columns:
        for normalize in [False]:
            intervals_before = [x for x in range(0, 601, 15)]
            intervals_after = [x for x in range(0, 301, 15)]

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

    return attrs


def training_set(events_file: str, no_event_time_shift: int, table_name: str):
    logging.info('start')

    # stiahnutie dat
    con = ConnectionUtil.create_con()
    storage = Storage(events_file, no_event_time_shift, table_name)
    d = storage.load_data(con, 0, 0, 'rh_in_specific_g_kg')
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
    training, tr_events = AttributeUtil.cached_training_data(con, table_name, filtered, func,
                                                             row_selector, interval_selector,
                                                             'open', 'testing_cached.csv')
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


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    # tabulka s CO2, ktora neprekroci hranicu 2000ppm
    table_name = 'measured_klarka_shower'

    training_set('examples/events_klarka_shower.json', -500, table_name)

    start = int(DateTimeUtil.local_time_str_to_utc('2018/11/01 05:30:00').timestamp())
    testing_set(table_name, start, start + 100, 'testing.csv')
    # testing_month(table_name, start)
