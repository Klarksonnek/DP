from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

from dm.FilterUtil import FilterUtil
from dm.ConnectionUtil import ConnectionUtil
from dm.CSVUtil import CSVUtil
from dm.Attributes import *
from dm.GraphUtil import GraphUtil


no_events_records = [
    # 01 iteracia - SVM, 4 mesiace, 2;3
    ('2018/10/07 13:45:00', 'nothing'),
    ('2018/10/09 09:14:30', 'nothing'),
    ('2018/10/11 19:08:30', 'nothing'),
    ('2018/10/13 07:28:00', 'nothing'),
    ('2018/10/15 13:21:30', 'nothing'),
    ('2018/10/15 20:11:30', 'nothing'),
    ('2018/10/30 18:00:30', 'nothing'),
    ('2018/11/06 23:15:30', 'nothing'),
    ('2018/11/07 23:11:30', 'nothing'),
    ('2018/11/30 16:28:00', 'nothing'),

    # 02 iteracia - SVM, 4 mesiace, 2;3
    ('2018/10/10 20:32:00', 'nothing'),
    ('2018/10/10 23:24:00', 'nothing'),
    ('2018/10/14 18:40:30', 'nothing'),
    ('2018/10/16 19:00:00', 'nothing'),
    ('2018/10/25 17:42:00', 'nothing'),
    ('2018/10/31 23:36:00', 'nothing'),
    ('2018/11/11 00:55:30', 'nothing'),
    ('2018/11/16 15:46:00', 'nothing'),
    ('2018/11/20 10:20:00', 'nothing'),
    ('2018/11/27 21:56:00', 'nothing'),

    # 03 iteracia - SVM, 4 mesiace, 2;3
    ('2018/10/11 22:43:30', 'nothing'),
    ('2018/10/21 19:48:00', 'nothing'),
    ('2018/10/24 07:35:00', 'nothing'),
    ('2018/11/14 10:04:00', 'nothing'),
    ('2018/12/07 10:14:00', 'nothing'),
    ('2019/01/13 01:19:30', 'nothing'),
    ('2019/01/28 04:38:30', 'nothing'),
    ('2019/01/30 09:07:30', 'nothing'),
    ('2019/01/27 12:20:00', 'nothing'),
    ('2019/01/23 15:13:00', 'nothing'),

    # 04 iteracia - SVM, 4 mesiace, 2;3
    ('2018/10/16 17:02:30', 'nothing'),
    ('2018/10/17 23:54:00', 'nothing'),
    ('2018/10/21 19:48:00', 'nothing'),
    ('2018/10/27 18:23:00', 'nothing'),
    ('2018/10/30 14:23:00', 'nothing'),
    ('2018/11/04 09:45:00', 'nothing'),
    ('2018/11/09 23:02:30', 'nothing'),
    ('2018/11/10 03:07:30', 'nothing'),
    ('2018/11/15 21:43:30', 'nothing'),
    ('2018/11/19 11:33:30', 'nothing'),

    # 05 iteracia - SVM, 4 mesiace, 2;3
    ('2018/10/22 16:39:30', 'nothing'),
    ('2018/11/02 20:30:00', 'nothing'),
    ('2018/11/07 07:00:00', 'nothing'),
    ('2018/11/10 03:41:00', 'nothing'),
    ('2018/11/17 23:59:30', 'nothing'),
    ('2018/11/30 18:37:00', 'nothing'),
    ('2018/12/02 21:14:00', 'nothing'),
    ('2018/12/16 17:31:00', 'nothing'),
    ('2019/01/07 13:53:30', 'nothing'),
    ('2019/01/28 14:40:30', 'nothing'),

    # 06 iteracia - SVM, 4 mesiace, 2;3
    ('2018/10/10 19:49:30', 'nothing'),
    ('2018/10/14 10:56:30', 'nothing'),
    ('2018/10/16 14:27:30', 'nothing'),
    ('2018/10/17 23:51:00', 'nothing'),
    ('2018/10/26 15:17:30', 'nothing'),
    ('2018/11/10 03:10:30', 'nothing'),
    ('2018/11/10 04:31:00', 'nothing'),
    ('2018/11/21 08:01:30', 'nothing'),
    ('2018/11/30 11:15:30', 'nothing'),
    ('2019/01/10 08:51:00', 'nothing'),

    # 07 iteracia - SVM, 4 mesiace, 2;3
    ('2018/11/10 02:29:30', 'nothing'),
    ('2018/11/10 23:26:00', 'nothing'),
    ('2018/12/07 23:17:30', 'nothing'),
    ('2019/01/10 08:49:30', 'nothing'),
    ('2019/01/15 15:11:00', 'nothing'),
    ('2019/01/29 22:37:00', 'nothing'),
    ('2018/10/14 14:58:30', 'nothing'),
    ('2018/10/14 14:59:00', 'nothing'),
    ('2018/11/11 01:06:30', 'nothing'),
    ('2018/11/11 01:07:00', 'nothing'),

    # 08 iteracia - SVM, 4 mesiace, 2;3
    ('2018/10/22 16:39:30', 'nothing'),
    ('2018/11/10 02:31:00', 'nothing'),
    ('2018/11/10 02:36:30', 'nothing'),
    ('2018/11/10 04:13:30', 'nothing'),
    ('2018/11/11 01:08:00', 'nothing'),
    ('2019/01/15 15:12:00', 'nothing'),
    ('2019/01/28 04:39:00', 'nothing'),
    ('2019/01/31 03:53:00', 'nothing'),
    ('2018/11/10 23:15:00', 'nothing'),
    ('2018/11/10 23:25:00', 'nothing'),

    # 09 iteracia - SVM, 4 mesiace, 2;3
    ('2018/10/31 07:17:30', 'nothing'),
    ('2018/11/15 21:43:00', 'nothing'),
    ('2019/01/28 14:49:00', 'nothing'),

    # 10 iteracia - RTree, 4 mesiace, 2;3
    ('2018/10/24 03:21:30', 'nothing'),
    ('2018/11/09 23:06:30', 'nothing'),
    ('2019/01/08 05:37:30', 'nothing'),
    ('2019/01/15 15:10:00', 'nothing'),

    # 11 iteracia - DTree, 4 mesiace, 2;3
    ('2018/10/09 10:44:00', 'nothing'),
    ('2018/10/10 20:31:00', 'nothing'),
    ('2018/10/14 09:09:30', 'nothing'),
    ('2018/10/22 16:40:00', 'nothing'),
    ('2018/10/24 06:55:30', 'nothing'),
    ('2018/11/03 12:29:00', 'nothing'),
    ('2018/11/10 00:46:30', 'nothing'),
    ('2018/11/10 07:30:00', 'nothing'),
    ('2018/11/30 22:48:30', 'nothing'),
    ('2018/12/05 00:59:00', 'nothing'),

    # 12 iteracia - DTree, 4 mesiace, 2;3
    ('2018/10/07 11:36:30', 'nothing'),
    ('2018/10/13 11:10:30', 'nothing'),
    ('2018/10/14 14:59:30', 'nothing'),
    ('2018/10/15 18:15:30', 'nothing'),
    ('2018/10/24 05:02:00', 'nothing'),
    ('2018/11/10 06:38:00', 'nothing'),
    ('2018/11/24 07:20:00', 'nothing'),
    ('2018/12/16 06:00:00', 'nothing'),
    ('2019/01/27 12:20:30', 'nothing'),
    ('2019/01/31 04:02:30', 'nothing'),

    # 13 iteracia - DTree, 4 mesiace, 2;3
    ('2018/10/11 10:21:00', 'nothing'),
    ('2018/10/11 14:03:00', 'nothing'),
    ('2018/10/15 13:20:00', 'nothing'),
    ('2018/10/19 10:52:30', 'nothing'),
    ('2018/11/05 18:01:00', 'nothing'),
    ('2018/11/24 04:01:00', 'nothing'),
    ('2018/11/29 17:17:30', 'nothing'),
    ('2018/12/08 06:11:30', 'nothing'),
    ('2019/01/24 19:28:30', 'nothing'),
    ('2019/01/28 05:13:00', 'nothing'),

    # 14 iteracia - DTree, 4 mesiace, 2;3
    ('2018/10/07 17:43:00', 'nothing'),
    ('2018/10/11 11:36:00', 'nothing'),
    ('2018/10/16 16:37:30', 'nothing'),
    ('2018/11/01 17:37:00', 'nothing'),
    ('2018/11/18 13:33:00', 'nothing'),
    ('2018/11/24 09:56:30', 'nothing'),
    ('2018/11/28 11:06:30', 'nothing'),
    ('2018/12/01 12:28:30', 'nothing'),
    ('2018/12/19 10:33:00', 'nothing'),
    ('2019/01/19 14:31:30', 'nothing'),

    # 15 iteracia - DTree, 4 mesiace, 2;3
    ('2018/10/07 23:38:30', 'nothing'),
    ('2018/10/11 18:50:00', 'nothing'),
    ('2018/10/15 13:18:30', 'nothing'),
    ('2018/10/31 07:17:00', 'nothing'),
    ('2018/11/06 14:21:30', 'nothing'),
    ('2018/11/18 07:36:30', 'nothing'),
    ('2018/12/08 11:03:30', 'nothing'),
    ('2019/01/12 13:54:30', 'nothing'),
    ('2019/01/24 09:31:00', 'nothing'),
    ('2019/01/27 20:51:30', 'nothing'),

    # 16 iteracia - DTree, 4 mesiace, 2;3
    ('2018/10/24 03:21:00', 'nothing'),
    ('2018/10/24 03:21:30', 'nothing'),
    ('2018/10/31 07:17:00', 'nothing'),
    ('2019/01/26 04:57:00', 'nothing'),
    ('2019/01/26 04:57:30', 'nothing'),
    ('2019/01/28 04:27:30', 'nothing'),
    ('2019/01/28 04:28:00', 'nothing'),

    # 17 iteracia - DTree, 4 mesiace, 2;3
    ('2018/10/07 08:58:00', 'nothing'),
    ('2018/10/11 18:51:30', 'nothing'),
    ('2018/10/14 12:47:00', 'nothing'),
    ('2018/10/15 21:49:30', 'nothing'),
    ('2018/10/24 07:36:30', 'nothing'),
    ('2018/10/28 19:58:30', 'nothing'),
    ('2018/11/05 21:38:00', 'nothing'),
    ('2018/11/16 10:51:00', 'nothing'),
    ('2018/11/25 21:56:30', 'nothing'),
    ('2018/12/15 13:51:00', 'nothing'),

    # 18 iteracia - DTree, 4 mesiace, 2;3
    ('2018/10/13 16:07:30', 'nothing'),
    ('2018/10/16 09:04:00', 'nothing'),
    ('2018/10/27 21:47:00', 'nothing'),
    ('2018/11/01 18:54:30', 'nothing'),
    ('2018/11/06 08:55:00', 'nothing'),
    ('2018/11/18 17:04:30', 'nothing'),
    ('2018/11/24 09:38:30', 'nothing'),
    ('2018/11/30 18:42:00', 'nothing'),
    ('2018/12/09 01:42:30', 'nothing'),
    ('2019/01/23 13:25:00', 'nothing'),

    # 19 iteracia - DTree, 4 mesiace, 2;3
    ('2018/10/07 13:58:00', 'nothing'),
    ('2018/10/12 00:15:00', 'nothing'),
    ('2018/10/15 09:17:30', 'nothing'),
    ('2018/10/16 07:37:30', 'nothing'),
    ('2018/10/17 21:08:30', 'nothing'),
    ('2018/10/21 03:11:00', 'nothing'),
    ('2018/10/24 22:37:30', 'nothing'),
    ('2018/10/28 08:04:30', 'nothing'),
    ('2018/10/30 14:59:30', 'nothing'),
    ('2018/11/01 17:40:00', 'nothing'),

    # 20 iteracia - DTree, 4 mesiace, 2;3
    ('2018/10/10 19:47:30', 'nothing'),
    ('2018/10/24 05:32:00', 'nothing'),
    ('2018/11/05 20:21:30', 'nothing'),
    ('2018/11/10 04:12:00', 'nothing'),
    ('2018/11/13 20:45:30', 'nothing'),
    ('2018/12/01 23:12:30', 'nothing'),
    ('2018/12/05 20:42:30', 'nothing'),
    ('2019/01/15 15:09:30', 'nothing'),
    ('2019/01/23 21:09:00', 'nothing'),
    ('2019/01/27 16:19:30', 'nothing'),

    # 21 iteracia - DTree, 4 mesiace, 2;3
    ('2018/10/13 16:07:00', 'nothing'),
    ('2018/10/15 13:20:30', 'nothing'),
    ('2018/10/27 16:33:00', 'nothing'),
    ('2018/10/29 14:23:30', 'nothing'),
    ('2018/11/18 17:04:00', 'nothing'),
    ('2019/01/16 10:57:00', 'nothing'),
    ('2019/01/23 13:24:30', 'nothing'),
    ('2019/01/29 22:23:30', 'nothing'),
    ('2019/01/29 22:24:00', 'nothing'),
    ('2019/01/29 22:24:30', 'nothing'),

    # 22 iteracia - DTree, 4 mesiace, 2;3
    ('2018/10/31 07:16:30', 'nothing'),
    ('2018/11/10 04:57:00', 'nothing'),
    ('2018/11/10 06:37:30', 'nothing'),
    ('2018/11/24 00:23:00', 'nothing'),
    ('2018/12/01 04:32:30', 'nothing'),
    ('2019/01/10 08:47:30', 'nothing'),
    ('2019/01/10 09:39:00', 'nothing'),
    ('2019/01/28 04:38:00', 'nothing'),
    ('2019/01/29 23:06:00', 'nothing'),
    ('2019/01/31 03:51:00', 'nothing'),

    # 23 iteracia - DTree, 4 mesiace, 2;3
    ('2018/10/07 08:57:00', 'nothing'),
    ('2018/10/14 20:43:30', 'nothing'),
    ('2018/10/16 14:26:30', 'nothing'),
    ('2018/10/17 09:04:30', 'nothing'),
    ('2018/10/25 19:32:00', 'nothing'),
    ('2018/10/31 22:06:00', 'nothing'),
    ('2018/11/04 09:44:30', 'nothing'),
    ('2018/11/06 23:09:30', 'nothing'),
    ('2018/11/18 17:03:30', 'nothing'),
    ('2018/12/08 08:09:00', 'nothing'),

    # 24 iteracia - DTree, 4 mesiace, 2;3
    ('2018/10/24 07:36:00', 'nothing'),

    # 25 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/09 15:33:00', 'nothing'),
    ('2018/10/10 23:05:00', 'nothing'),
    ('2018/10/31 22:41:00', 'nothing'),
    ('2018/11/10 01:27:00', 'nothing'),
    ('2018/11/14 01:04:00', 'nothing'),
    ('2018/11/24 00:25:30', 'nothing'),
    ('2018/11/29 15:32:00', 'nothing'),
    ('2018/12/02 07:59:30', 'nothing'),
    ('2018/12/02 19:04:30', 'nothing'),
    ('2018/12/08 11:11:00', 'nothing'),

    # 26 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/07 06:39:30', 'nothing'),
    ('2018/10/07 16:54:30', 'nothing'),
    ('2018/10/09 00:51:30', 'nothing'),
    ('2018/10/09 14:45:00', 'nothing'),
    ('2018/10/12 01:11:00', 'nothing'),
    ('2018/10/16 13:39:00', 'nothing'),
    ('2018/10/19 03:32:30', 'nothing'),
    ('2018/10/29 17:57:30', 'nothing'),
    ('2018/11/01 13:57:30', 'nothing'),
    ('2018/11/04 02:29:30', 'nothing'),

    # 27 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/07 07:53:30', 'nothing'),
    ('2018/10/09 01:03:00', 'nothing'),
    ('2018/10/10 21:55:30', 'nothing'),
    ('2018/10/11 15:02:30', 'nothing'),
    ('2018/10/13 21:59:30', 'nothing'),
    ('2018/10/14 11:20:00', 'nothing'),
    ('2018/10/15 19:56:00', 'nothing'),
    ('2018/10/24 02:47:00', 'nothing'),
    ('2018/10/27 19:38:00', 'nothing'),
    ('2018/10/30 14:11:00', 'nothing'),

    # 28 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/07 09:40:30', 'nothing'),
    ('2018/10/10 10:59:00', 'nothing'),
    ('2018/10/11 17:25:30', 'nothing'),
    ('2018/10/13 10:46:00', 'nothing'),
    ('2018/10/21 03:57:00', 'nothing'),
    ('2018/10/24 00:11:30', 'nothing'),
    ('2018/10/27 09:08:30', 'nothing'),
    ('2018/11/04 00:16:00', 'nothing'),
    ('2018/11/12 15:41:30', 'nothing'),
    ('2018/11/20 08:34:30', 'nothing'),

    # 29 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/09 14:30:00', 'nothing'),
    ('2018/10/11 15:31:30', 'nothing'),
    ('2018/10/17 16:32:00', 'nothing'),
    ('2018/10/28 08:10:30', 'nothing'),
    ('2018/11/04 10:46:30', 'nothing'),
    ('2018/11/13 20:29:00', 'nothing'),
    ('2018/11/29 15:05:00', 'nothing'),
    ('2018/12/03 23:19:00', 'nothing'),
    ('2018/12/18 23:16:00', 'nothing'),
    ('2019/01/14 07:08:30', 'nothing'),

    # 30 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/07 13:38:00', 'nothing'),
    ('2018/10/09 16:09:00', 'nothing'),
    ('2018/10/10 22:30:00', 'nothing'),
    ('2018/10/11 12:44:30', 'nothing'),
    ('2018/10/12 00:31:00', 'nothing'),
    ('2018/10/15 09:28:30', 'nothing'),
    ('2018/10/21 01:45:30', 'nothing'),
    ('2018/10/24 00:59:30', 'nothing'),
    ('2018/11/01 14:36:30', 'nothing'),
    ('2018/11/08 00:52:00', 'nothing'),

    # 31 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/13 13:50:30', 'nothing'),
    ('2018/11/10 03:54:30', 'nothing'),
    ('2018/11/10 04:15:00', 'nothing'),
    ('2018/11/15 21:44:00', 'nothing'),
    ('2018/11/24 18:33:00', 'nothing'),
    ('2018/12/01 09:59:30', 'nothing'),
    ('2018/12/19 10:42:30', 'nothing'),
    ('2019/01/09 01:01:30', 'nothing'),
    ('2019/01/22 17:10:00', 'nothing'),
    ('2019/01/29 22:26:00', 'nothing'),

    # 32 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/09 08:19:00', 'nothing'),
    ('2018/10/09 15:19:00', 'nothing'),
    ('2018/10/11 13:52:00', 'nothing'),
    ('2018/10/13 14:14:30', 'nothing'),
    ('2018/10/20 04:12:30', 'nothing'),
    ('2018/10/27 23:09:00', 'nothing'),
    ('2018/11/05 20:02:00', 'nothing'),
    ('2018/11/10 23:22:00', 'nothing'),
    ('2018/11/11 20:57:00', 'nothing'),
    ('2018/11/13 20:58:30', 'nothing'),

    # 33 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/07 11:47:00', 'nothing'),
    ('2018/10/11 00:58:00', 'nothing'),
    ('2018/10/11 23:55:30', 'nothing'),
    ('2018/10/15 00:28:00', 'nothing'),
    ('2018/10/15 23:57:30', 'nothing'),
    ('2018/10/16 18:30:30', 'nothing'),
    ('2018/10/17 19:16:00', 'nothing'),
    ('2018/10/22 19:13:30', 'nothing'),
    ('2018/11/07 20:58:00', 'nothing'),
    ('2018/11/11 01:07:30', 'nothing'),

    # 34 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/15 18:53:00', 'nothing'),
    ('2018/11/04 08:14:30', 'nothing'),
    ('2018/11/10 01:24:30', 'nothing'),
    ('2018/11/10 04:20:00', 'nothing'),
    ('2018/11/24 18:32:30', 'nothing'),
    ('2018/12/02 19:09:00', 'nothing'),
    ('2019/01/10 08:51:30', 'nothing'),
    ('2019/01/10 20:18:00', 'nothing'),
    ('2019/01/14 09:50:30', 'nothing'),
    ('2019/01/18 09:58:30', 'nothing'),

    # 35 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/09 14:44:30', 'nothing'),
    ('2018/10/17 15:36:30', 'nothing'),
    ('2018/10/17 21:43:00', 'nothing'),
    ('2018/11/03 00:28:00', 'nothing'),
    ('2018/11/10 04:21:00', 'nothing'),
    ('2018/11/10 05:25:30', 'nothing'),
    ('2018/11/14 02:32:30', 'nothing'),
    ('2018/11/24 18:49:00', 'nothing'),
    ('2018/12/12 18:21:00', 'nothing'),
    ('2018/12/14 11:02:30', 'nothing'),

    # 36 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/11 00:39:00', 'nothing'),
    ('2018/10/16 08:01:30', 'nothing'),
    ('2018/10/21 19:47:00', 'nothing'),
    ('2018/10/28 13:32:30', 'nothing'),
    ('2018/11/07 07:24:00', 'nothing'),
    ('2018/11/10 02:37:00', 'nothing'),
    ('2018/11/10 18:20:00', 'nothing'),
    ('2018/11/19 02:30:00', 'nothing'),
    ('2018/11/21 08:11:30', 'nothing'),
    ('2019/01/08 01:11:30', 'nothing'),

    # 37 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/13 11:49:30', 'nothing'),
    ('2018/10/22 15:43:00', 'nothing'),
    ('2018/10/23 00:59:30', 'nothing'),
    ('2018/11/10 23:18:00', 'nothing'),
    ('2018/11/11 00:56:00', 'nothing'),
    ('2018/11/21 18:39:30', 'nothing'),
    ('2018/11/26 19:31:30', 'nothing'),
    ('2018/11/29 17:37:30', 'nothing'),
    ('2018/12/01 04:33:30', 'nothing'),
    ('2018/12/03 22:20:30', 'nothing'),

    # 38 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/16 07:14:30', 'nothing'),
    ('2018/11/10 02:50:30', 'nothing'),
    ('2018/11/10 03:40:30', 'nothing'),
    ('2018/11/30 11:34:00', 'nothing'),
    ('2018/12/02 19:10:00', 'nothing'),
    ('2019/01/12 02:41:00', 'nothing'),
    ('2019/01/15 15:10:30', 'nothing'),
    ('2019/01/22 17:15:00', 'nothing'),
    ('2018/11/09 23:02:00', 'nothing'),
    ('2018/11/09 23:49:30', 'nothing'),

    # 39 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/21 19:47:30', 'nothing'),
    ('2018/10/28 15:39:00', 'nothing'),
    ('2018/10/31 22:41:30', 'nothing'),
    ('2018/11/02 20:29:00', 'nothing'),
    ('2018/11/05 18:34:30', 'nothing'),
    ('2018/11/09 23:50:00', 'nothing'),
    ('2018/11/10 00:29:30', 'nothing'),
    ('2018/11/10 03:41:30', 'nothing'),
    ('2018/11/11 02:39:00', 'nothing'),
    ('2018/11/21 08:03:00', 'nothing'),

    # 40 iteracia - Deep, 4 mesiace, 2;3
    ('2018/11/10 18:08:00', 'nothing'),
    ('2018/11/22 17:50:00', 'nothing'),

    # 41 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/13 14:15:00', 'nothing'),
    ('2018/11/03 00:35:30', 'nothing'),
    ('2018/11/09 23:01:30', 'nothing'),
    ('2018/11/09 23:27:00', 'nothing'),
    ('2018/11/10 04:02:30', 'nothing'),
    ('2018/11/16 11:53:30', 'nothing'),
    ('2018/11/21 08:02:30', 'nothing'),
    ('2018/11/22 17:49:30', 'nothing'),
    ('2018/11/24 18:36:30', 'nothing'),
    ('2019/01/17 20:58:30', 'nothing'),

    # 42 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/29 20:18:00', 'nothing'),
    ('2019/01/10 09:45:30', 'nothing'),
    ('2019/01/10 09:46:30', 'nothing'),
]


def func(con, table_name, timestamp, row_selector, interval_selector):
    attrs = []
    columns = [
        'co2_in_ppm',
        'temperature_in_celsius',
        'rh_in_specific_g_kg',
    ]
    precision = 2

    for column in columns:
        for normalize in [False]:
            intervals_before = [x for x in range(20, 901, 20)]
            intervals_after = [x for x in range(15, 181, 15)]

            #
            # linearny posun DifferenceA
            op = FirstDifferenceAttrA(con, table_name, row_selector, interval_selector)
            b, a = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=intervals_before,
                              intervals_after=intervals_after,
                              normalize=normalize,
                              enable_count=True,
                              prefix='',
                              selected_before=[intervals_before],
                              selected_after=[intervals_after])
            attrs += b + a

            pr = '_linear'
            be, af = op.geometric_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.arithmetic_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.variance(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.standard_deviation(column, precision, b, a, pr)
            attrs += be + af

            #
            # linearny posun DifferenceB
            op = FirstDifferenceAttrB(con, table_name, row_selector, interval_selector)
            b, a = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=intervals_before,
                              intervals_after=intervals_after,
                              normalize=normalize,
                              enable_count=True,
                              prefix='',
                              selected_before=[intervals_before],
                              selected_after=[intervals_after])
            attrs += b + a

            pr = '_linear'
            be, af = op.geometric_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.arithmetic_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.variance(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.standard_deviation(column, precision, b, a, pr)
            attrs += be + af

            op = DifferenceBetweenRealLinear(con, table_name, row_selector, interval_selector)
            b, a = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=intervals_before,
                              intervals_after=intervals_after,
                              window_size_before=20*60, window_size_after=3*60,
                              prefix='')
            attrs += b + a

            pr = '_linear'
            be, af = op.geometric_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.arithmetic_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.variance(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.standard_deviation(column, precision, b, a, pr)
            attrs += be + af

            #
            # x^2 posun
            op = FirstDifferenceAttrB(con, table_name, row_selector, interval_selector)
            b, a = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=[x * x for x in range(2, 31, 1)],
                              intervals_after=[x * x for x in range(2, 14, 1)],
                              normalize=normalize,
                              enable_count=True,
                              prefix='_x2',
                              selected_before=[[x * x for x in range(2, 31, 1)]],
                              selected_after=[[x * x for x in range(2, 14, 1)]])
            attrs += b + a

            pr = '_x2'
            be, af = op.geometric_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.arithmetic_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.variance(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.standard_deviation(column, precision, b, a, pr)
            attrs += be + af

            #
            # x^3 posun
            op = FirstDifferenceAttrB(con, table_name, row_selector, interval_selector)
            b, a = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=[x * x * x for x in range(2, 10, 1)],
                              intervals_after=[x * x * x for x in range(2, 6, 1)],
                              normalize=normalize,
                              enable_count=True,
                              prefix='_x3',
                              selected_before=[[x * x * x for x in range(2, 10, 1)]],
                              selected_after=[[x * x * x for x in range(2, 6, 1)]])
            attrs += b + a

            pr = '_x3'
            be, af = op.geometric_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.arithmetic_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.variance(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.standard_deviation(column, precision, b, a, pr)
            attrs += be + af

            #
            # GrowRate - linearne
            op = GrowthRate(con, table_name, row_selector, interval_selector)
            b, a = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=[x for x in range(5, 901, 15)],
                              intervals_after=[x for x in range(5, 181, 15)],
                              value_delay=15, prefix='_step20')
            attrs += b + a
            be, af = op.arithmetic_mean(column, precision, b, a, 'G_linear_step_15')
            attrs += be + af

            # GrowRate - linearne
            op = GrowthRate(con, table_name, row_selector, interval_selector)
            b, a = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=[x for x in range(5, 901, 30)],
                              intervals_after=[x for x in range(5, 181, 30)],
                              value_delay=30, prefix='_step_30')
            attrs += b + a
            be, af = op.arithmetic_mean(column, precision, b, a, 'G_linear_step_30')
            attrs += be + af

            # GrowRate - x^2
            op = GrowthRate(con, table_name, row_selector, interval_selector)
            b, a = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=[x * x for x in range(2, 31, 1)],
                              intervals_after=[x * x for x in range(2, 14, 1)],
                              value_delay=30, prefix='_x2')
            attrs += b + a
            be, af = op.arithmetic_mean(column, precision, b, a, 'Grow_x2')
            attrs += be + af

            # GrowRate - x^3
            op = GrowthRate(con, table_name, row_selector, interval_selector)
            b, a = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=[x * x * x for x in range(2, 10, 1)],
                              intervals_after=[x * x * x for x in range(2, 6, 1)],
                              value_delay=30, prefix='_x3')
            attrs += b + a
            be, af = op.arithmetic_mean(column, precision, b, a, 'Grow_x3')
            attrs += be + af

        op = InOutDiff(con, table_name, row_selector, interval_selector)
        b, a = op.execute(timestamp=timestamp, column='co2_in_ppm_diff', precision=precision,
                          intervals_before=[1],
                          intervals_after=[],
                          prefix='')
        attrs += b + a

    return attrs


def training_set(events_file: str, no_event_time_shift: int, table_name: str):
    logging.info('start')

    # stiahnutie dat
    con = ConnectionUtil.create_con()
    storage = Storage(events_file, no_event_time_shift, table_name)
    d = storage.load_data(con, 0, 0, 'co2_in_ppm')
    logging.info('downloaded events: %d' % len(d))

    # aplikovanie filtrov na eventy
    filtered = FilterUtil.only_valid_events(d)
    logging.info('events after applying the filter: %d' % len(filtered))

    if ConnectionUtil.is_testable_system():
        filtered = filtered[:10]

    # selector pre data
    row_selector = CachedDiffRowWithIntervalSelector(con, table_name, 0, 0)
    interval_selector = None

    # trenovacia mnozina
    logging.info('start computing of training set')
    training, tr_events = AttributeUtil.cached_training_data(con, table_name, filtered, func,
                                                             row_selector, interval_selector,
                                                             'open', 'testing_cached.csv')
    count = len(training)
    logging.info('training set contains %d events (%d records)' % (count / 2, count))

    GraphUtil.gen_duration_histogram(tr_events, 'save', ['png'], 'Histogram dlzok vetrania',
                                     [x for x in range(5, 60, 5)], 1)

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

    logging.info('start computing of testing set')
    length = AttributeUtil.testing_data_with_write(con, table_name, start, end, 30, func,
                                                   None, None, 'open', filename)
    logging.info('testing set contains %d records' % length)
    logging.info('end computing of testing set')

    logging.info('end')


def testing_month(table_name, start):
    mesiac = 30 * 24 * 3600

    directory = 'co2_t_h'
    if not os.path.isdir(directory):
        os.mkdir(directory)

    file_names = [
        '{0}/1_oktober.csv'.format(directory),
        '{0}/2_november.csv'.format(directory),
        '{0}/3_december.csv'.format(directory),
        '{0}/4_januar.csv'.format(directory),
        '{0}/5_februar.csv'.format(directory),
        '{0}/6_marec.csv'.format(directory),
    ]

    for file_name in file_names:
        testing_set(table_name, start, start + mesiac, file_name)
        start += mesiac


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    # tabulka s CO2, ktora neprekroci hranicu 2000ppm
    table_name = 'measured_filtered_peto'

    training_set('examples/events_peto.json', -500, table_name)

    start = int(DateTimeUtil.local_time_str_to_utc('2018/10/07 06:00:00').timestamp())
    testing_set(table_name, start, start + 100, 'testing.csv')
    # testing_month(table_name, start)
