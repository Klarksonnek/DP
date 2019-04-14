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
    # 01 iteracia - RTree, 4 mesiace, 10;10
    ('2018/10/07 09:04:30', 'nothing'),
    ('2018/10/08 00:02:00', 'nothing'),
    ('2018/10/08 00:59:30', 'nothing'),
    ('2018/10/12 06:46:30', 'nothing'),
    ('2018/10/12 10:42:00', 'nothing'),
    ('2018/10/13 19:00:30', 'nothing'),
    ('2018/10/14 22:36:00', 'nothing'),
    ('2018/10/16 14:32:30', 'nothing'),
    ('2018/10/16 17:33:00', 'nothing'),
    ('2018/10/18 18:07:30', 'nothing'),

    # 02 iteracia - RTree, 4 mesiace, 10;10
    ('2018/10/09 14:30:00', 'nothing'),
    ('2018/10/14 18:47:30', 'nothing'),
    ('2018/10/15 18:25:00', 'nothing'),
    ('2018/10/15 19:25:00', 'nothing'),
    ('2018/10/17 12:43:00', 'nothing'),
    ('2018/10/18 07:20:30', 'nothing'),
    ('2018/10/23 01:03:00', 'nothing'),
    ('2018/10/23 09:17:00', 'nothing'),
    ('2018/10/23 18:50:30', 'nothing'),
    ('2018/10/26 15:11:30', 'nothing'),

    # 03 iteracia - RTree, 4 mesiace, 10;10
    ('2018/10/08 19:18:00', 'nothing'),
    ('2018/10/10 15:54:30', 'nothing'),
    ('2018/10/15 13:21:00', 'nothing'),
    ('2018/10/19 02:04:00', 'nothing'),
    ('2018/10/19 02:53:00', 'nothing'),
    ('2018/10/28 11:30:30', 'nothing'),
    ('2018/11/01 21:03:30', 'nothing'),
    ('2018/11/03 19:52:30', 'nothing'),
    ('2018/11/07 04:39:00', 'nothing'),
    ('2018/11/11 01:32:30', 'nothing'),

    # 04 iteracia - RTree, 4 mesiace, 10;10
    ('2018/10/08 00:59:30', 'nothing'),
    ('2018/10/09 14:30:00', 'nothing'),
    ('2018/10/09 22:49:30', 'nothing'),
    ('2018/10/10 21:00:00', 'nothing'),
    ('2018/10/10 21:24:30', 'nothing'),
    ('2018/10/10 22:55:00', 'nothing'),
    ('2018/10/11 18:55:30', 'nothing'),
    ('2018/10/12 15:55:30', 'nothing'),
    ('2018/10/13 01:56:30', 'nothing'),
    ('2018/10/13 18:35:30', 'nothing'),

    # 05 iteracia - RTree, 4 mesiace, 10;10
    ('2018/10/12 15:35:30', 'nothing'),
    ('2018/10/22 12:33:00', 'nothing'),
    ('2018/10/24 06:09:00', 'nothing'),
    ('2018/11/10 00:46:30', 'nothing'),
    ('2018/11/11 00:05:00', 'nothing'),
    ('2018/11/11 04:35:00', 'nothing'),
    ('2018/11/13 20:46:30', 'nothing'),
    ('2018/11/20 18:21:00', 'nothing'),
    ('2018/11/24 07:20:00', 'nothing'),
    ('2018/11/27 01:16:30', 'nothing'),

    # 06 iteracia - RTree, 4 mesiace, 10;10
    ('2018/10/17 23:51:00', 'nothing'),
    ('2018/11/20 18:22:00', 'nothing'),
    ('2018/11/24 02:54:30', 'nothing'),
    ('2018/12/16 06:00:00', 'nothing'),
    ('2019/01/08 05:37:30', 'nothing'),
    ('2018/10/10 13:41:00', 'nothing'),
    ('2018/10/10 13:41:30', 'nothing'),
    ('2018/10/10 16:23:30', 'nothing'),
    ('2018/10/10 16:24:00', 'nothing'),
    ('2018/10/10 16:24:30', 'nothing'),

    # 07 iteracia - RTree, 4 mesiace, 10;10
    ('2019/01/10 09:39:00', 'nothing'),
    ('2019/01/15 15:11:30', 'nothing'),
    ('2018/10/10 16:36:00', 'nothing'),
    ('2018/10/10 16:36:30', 'nothing'),
    ('2018/11/10 03:04:30', 'nothing'),
    ('2018/11/10 03:05:00', 'nothing'),
    ('2019/01/29 22:27:30', 'nothing'),
    ('2019/01/29 22:28:00', 'nothing'),
    ('2019/01/31 03:54:00', 'nothing'),
    ('2019/01/31 03:54:30', 'nothing'),

    # 08 iteracia - RTree, 4 mesiace, 10;10
    ('2018/10/31 07:17:00', 'nothing'),
    ('2018/11/09 23:06:30', 'nothing'),
    ('2019/01/29 23:03:00', 'nothing'),
    ('2018/10/24 03:21:30', 'nothing'),
    ('2018/10/24 03:22:00', 'nothing'),
    ('2018/11/11 01:07:00', 'nothing'),
    ('2018/11/11 01:07:30', 'nothing'),
    ('2018/11/11 01:08:00', 'nothing'),
    ('2019/01/28 04:27:30', 'nothing'),
    ('2019/01/28 04:28:00', 'nothing'),

    # 09 iteracia - Tree, 4 mesiace, 10;10
    ('2018/10/10 16:23:00', 'nothing'),
    ('2018/10/10 16:45:30', 'nothing'),
    ('2018/10/11 21:02:00', 'nothing'),
    ('2018/10/23 09:18:30', 'nothing'),
    ('2018/10/24 03:22:30', 'nothing'),
    ('2018/11/10 02:30:30', 'nothing'),
    ('2018/11/10 23:13:00', 'nothing'),
    ('2018/11/13 14:39:00', 'nothing'),
    ('2019/01/15 15:09:30', 'nothing'),
    ('2019/01/10 09:37:30', 'nothing'),

    # 10 iteracia - Tree, 4 mesiace, 10;10
    ('2018/10/31 07:18:00', 'nothing'),
    ('2018/11/10 23:13:30', 'nothing'),
    ('2019/01/10 09:38:00', 'nothing'),

    # 11 iteracia - Tree, 4 mesiace, 10;10
    ('2018/11/11 01:07:00', 'nothing'),

    # 12 iteracia - Tree, 4 mesiace, 10;10
    ('2018/10/15 13:22:00', 'nothing'),
    ('2018/10/31 07:17:30', 'nothing'),
    ('2019/01/28 04:28:30', 'nothing'),

    # 13 iteracia - Tree, 4 mesiace, 10;10
    ('2018/10/31 07:18:00', 'nothing'),

    # 14 iteracia - SVM, 4 mesiace, 10;10
    ('2018/10/07 23:56:30', 'nothing'),
    ('2018/10/08 19:11:30', 'nothing'),
    ('2018/10/08 20:52:00', 'nothing'),
    ('2018/10/10 17:03:30', 'nothing'),
    ('2018/10/11 18:59:00', 'nothing'),
    ('2018/10/15 08:37:00', 'nothing'),
    ('2018/10/15 20:16:00', 'nothing'),
    ('2018/10/17 19:15:30', 'nothing'),
    ('2018/10/17 23:51:30', 'nothing'),
    ('2018/10/18 17:28:00', 'nothing'),

    # 15 iteracia - SVM, 4 mesiace, 10;10
    ('2018/10/10 16:38:00', 'nothing'),
    ('2018/10/10 16:38:30', 'nothing'),
    ('2018/11/11 01:08:30', 'nothing'),
    ('2018/11/11 01:09:00', 'nothing'),
    ('2019/01/10 08:52:00', 'nothing'),
    ('2019/01/28 04:42:30', 'nothing'),
    ('2019/01/31 03:55:30', 'nothing'),

    # 16 iteracia - neural, 4 mesiace, 10;10
    ('2018/10/10 12:33:30', 'nothing'),
    ('2018/10/10 17:22:30', 'nothing'),
    ('2018/10/11 13:13:00', 'nothing'),
    ('2018/10/11 14:29:00', 'nothing'),
    ('2018/10/11 15:36:00', 'nothing'),
    ('2018/10/11 16:35:30', 'nothing'),
    ('2018/10/11 17:13:30', 'nothing'),
    ('2018/10/12 20:22:00', 'nothing'),
    ('2018/10/12 20:43:00', 'nothing'),
    ('2018/10/17 13:38:00', 'nothing'),

    # 17 iteracia - Neural, 4 mesiace, 10;10
    ('2018/10/09 10:52:00', 'nothing'),
    ('2018/10/09 13:29:30', 'nothing'),
    ('2018/10/09 18:12:30', 'nothing'),
    ('2018/10/31 07:16:00', 'nothing'),
    ('2018/11/02 11:33:30', 'nothing'),
    ('2018/11/02 20:35:30', 'nothing'),
    ('2018/11/04 10:40:30', 'nothing'),
    ('2018/11/09 22:23:00', 'nothing'),
    ('2018/11/09 23:06:00', 'nothing'),
    ('2018/11/10 06:37:30', 'nothing'),

    # 18 iteracia - Neural, 4 mesiace, 10;10
    ('2018/10/07 11:45:30', 'nothing'),
    ('2018/10/07 20:40:00', 'nothing'),
    ('2018/10/10 16:29:30', 'nothing'),
    ('2019/01/10 09:44:00', 'nothing'),
    ('2019/01/15 15:16:30', 'nothing'),
    ('2019/01/22 17:12:30', 'nothing'),
    ('2019/01/28 04:44:00', 'nothing'),
    ('2019/01/31 03:57:00', 'nothing'),
    ('2018/11/10 02:35:30', 'nothing'),
    ('2018/11/10 02:35:00', 'nothing'),

    # 19 iteracia - Neural, 4 mesiace, 10;10
    ('2018/10/17 09:18:30', 'nothing'),
    ('2018/10/18 17:27:30', 'nothing'),
    ('2018/10/18 22:27:30', 'nothing'),
    ('2018/10/27 20:25:30', 'nothing'),
    ('2018/10/29 06:44:30', 'nothing'),
    ('2018/11/02 22:59:30', 'nothing'),
    ('2018/11/08 07:38:00', 'nothing'),
    ('2018/11/09 22:16:00', 'nothing'),
    ('2018/11/19 17:49:00', 'nothing'),
    ('2018/11/25 19:36:30', 'nothing'),

    # 20 iteracia - Tree, 4 mesiace, 10;10
    ('2018/10/07 06:16:00', 'nothing'),
    ('2018/10/07 08:28:00', 'nothing'),
    ('2018/10/07 12:21:30', 'nothing'),
    ('2018/10/07 19:06:30', 'nothing'),
    ('2018/10/08 01:07:30', 'nothing'),
    ('2018/10/08 08:55:30', 'nothing'),
    ('2018/10/08 08:56:00', 'nothing'),
    ('2018/10/08 19:09:30', 'nothing'),
    ('2018/10/08 19:34:00', 'nothing'),
    ('2018/10/08 21:27:00', 'nothing'),

    # 21 iteracia - Tree, 4 mesiace, 10;10
    ('2018/10/07 07:50:30', 'nothing'),
    ('2018/10/09 01:50:00', 'nothing'),
    ('2018/10/11 21:03:00', 'nothing'),
    ('2018/10/12 21:24:00', 'nothing'),
    ('2018/10/15 13:21:30', 'nothing'),
    ('2018/10/17 23:50:00', 'nothing'),
    ('2018/10/18 00:02:30', 'nothing'),
    ('2018/10/19 03:35:00', 'nothing'),
    ('2018/10/08 23:09:30', 'nothing'),
    ('2018/10/08 23:10:00', 'nothing'),

    # 22 iteracia - Tree, 4 mesiace, 10;10
    ('2018/10/09 12:22:00', 'nothing'),
    ('2018/10/09 16:46:30', 'nothing'),
    ('2018/10/09 16:51:00', 'nothing'),
    ('2018/10/10 16:46:30', 'nothing'),
    ('2018/10/10 17:02:00', 'nothing'),
    ('2018/10/16 00:25:00', 'nothing'),
    ('2018/10/19 12:59:30', 'nothing'),
    ('2018/10/09 11:51:00', 'nothing'),
    ('2018/10/09 11:51:30', 'nothing'),
    ('2018/10/09 11:52:00', 'nothing'),

    # 23 iteracia - Tree, 4 mesiace, 10;10
    ('2018/10/07 11:41:00', 'nothing'),
    ('2018/10/07 11:44:30', 'nothing'),
    ('2018/10/10 13:46:00', 'nothing'),
    ('2018/10/10 15:54:00', 'nothing'),
    ('2018/10/10 16:05:30', 'nothing'),
    ('2018/10/10 16:22:30', 'nothing'),
    ('2018/10/10 16:30:00', 'nothing'),
    ('2018/10/10 16:35:30', 'nothing'),
    ('2018/10/10 16:57:00', 'nothing'),
    ('2018/10/10 17:00:30', 'nothing'),

    # 24 iteracia - Tree, 4 mesiace, 10;10
    ('2018/10/07 20:38:30', 'nothing'),
    ('2018/10/09 01:50:30', 'nothing'),
    ('2018/10/09 14:29:30', 'nothing'),
    ('2018/10/10 17:25:00', 'nothing'),
    ('2018/10/10 20:59:30', 'nothing'),
    ('2018/10/17 09:21:30', 'nothing'),
    ('2018/10/22 12:32:30', 'nothing'),
    ('2018/10/24 03:21:00', 'nothing'),
    ('2018/10/24 05:32:30', 'nothing'),
    ('2018/10/24 06:09:30', 'nothing'),

    # 25 iteracia - Tree, 4 mesiace, 10;10
    ('2018/10/09 11:29:30', 'nothing'),
    ('2018/10/09 11:30:00', 'nothing'),
    ('2018/10/09 11:30:30', 'nothing'),
    ('2018/10/10 15:55:30', 'nothing'),
    ('2018/10/10 16:24:00', 'nothing'),
    ('2018/10/10 16:24:30', 'nothing'),
    ('2018/10/10 16:35:00', 'nothing'),
    ('2018/10/10 16:46:00', 'nothing'),
    ('2018/10/10 17:03:00', 'nothing'),
    ('2018/10/10 19:50:00', 'nothing'),

    # 26 iteracia - Tree, 4 mesiace, 10;10
    ('2018/10/10 17:01:30', 'nothing'),
    ('2018/10/15 18:24:00', 'nothing'),
    ('2018/10/17 10:54:30', 'nothing'),
    ('2018/10/19 06:52:30', 'nothing'),
    ('2018/10/31 07:16:30', 'nothing'),
    ('2018/11/10 23:13:30', 'nothing'),
    ('2018/11/10 23:14:00', 'nothing'),
    ('2018/11/11 01:06:30', 'nothing'),
    ('2018/12/14 10:56:30', 'nothing'),
    ('2019/01/29 23:03:30', 'nothing'),

    # 27 iteracia - Tree, 4 mesiace, 10;10
    ('2018/10/15 21:56:30', 'nothing'),
    ('2018/10/22 15:10:00', 'nothing'),
    ('2018/10/31 07:17:30', 'nothing'),
    ('2018/11/03 11:35:30', 'nothing'),
    ('2018/12/04 22:17:00', 'nothing'),
    ('2018/12/04 22:17:30', 'nothing'),
    ('2019/01/10 09:41:30', 'nothing'),
    ('2019/01/15 15:10:00', 'nothing'),
    ('2019/01/28 04:29:00', 'nothing'),
    ('2019/01/28 04:39:30', 'nothing'),

    # 28 iteracia - Tree, 4 mesiace, 10;10
    ('2018/10/10 17:01:00', 'nothing'),
    ('2018/10/11 21:02:30', 'nothing'),
    ('2018/10/16 21:15:30', 'nothing'),
    ('2018/10/22 15:07:30', 'nothing'),
    ('2018/10/26 14:50:30', 'nothing'),
    ('2018/11/03 11:37:30', 'nothing'),
    ('2018/11/11 01:06:00', 'nothing'),
    ('2018/11/27 18:19:00', 'nothing'),
    ('2019/01/29 22:27:00', 'nothing'),
    ('2019/01/31 03:53:00', 'nothing'),

    # 29 iteracia - All, 4 mesiace, 8;8
    ('2018/10/15 18:20:00', 'nothing'),
    ('2018/10/22 12:16:00', 'nothing'),
    ('2018/10/24 07:39:30', 'nothing'),
    ('2018/10/11 21:00:00', 'nothing'),
    ('2018/10/11 21:00:30', 'nothing'),
    ('2018/10/13 11:10:30', 'nothing'),
    ('2018/10/14 18:45:30', 'nothing'),
    ('2018/11/01 19:05:00', 'nothing'),
    ('2018/11/01 19:05:30', 'nothing'),

    # 30 iteracia - All, 4 mesiace, 7;7
    ('2018/10/23 09:14:00', 'nothing'),
    ('2018/10/24 07:38:30', 'nothing'),
    ('2019/01/12 13:58:00', 'nothing'),
    ('2018/10/15 18:19:00', 'nothing'),
    ('2018/10/22 16:43:30', 'nothing'),
    ('2018/10/23 09:14:00', 'nothing'),
    ('2018/10/23 18:27:30', 'nothing'),
    ('2018/10/24 07:38:30', 'nothing'),

    # 31 iteracia - All, 4 mesiace, 7;7
    ('2018/10/13 16:08:30', 'nothing'),
    ('2018/10/13 18:32:30', 'nothing'),
    ('2018/10/14 18:46:30', 'nothing'),
    ('2018/10/16 19:01:00', 'nothing'),
    ('2018/10/18 12:13:00', 'nothing'),
    ('2018/11/01 19:04:30', 'nothing'),
    ('2019/01/12 13:58:00', 'nothing'),
    ('2019/01/12 13:58:30', 'nothing'),
    ('2019/01/12 13:59:00', 'nothing'),
    ('2019/01/12 13:59:30', 'nothing'),

    # 32 iteracia - All, 4 mesiace, 7;7
    ('2018/11/11 01:07:00', 'nothing'),
    ('2018/11/11 01:07:30', 'nothing'),
    ('2018/11/11 01:08:00', 'nothing'),
    ('2018/10/07 20:34:00', 'nothing'),
    ('2018/10/07 23:52:00', 'nothing'),
    ('2018/10/08 19:03:30', 'nothing'),
    ('2018/10/11 18:51:30', 'nothing'),
    ('2018/10/11 20:59:30', 'nothing'),
    ('2018/10/14 22:33:00', 'nothing'),
    ('2018/10/15 21:56:00', 'nothing'),

    # 33 iteracia - All, 4 mesiace, 6;6
    ('2018/10/14 10:57:30', 'nothing'),
    ('2018/10/14 12:55:30', 'nothing'),
    ('2018/10/15 18:18:00', 'nothing'),
    ('2018/10/18 12:12:00', 'nothing'),
    ('2018/10/23 09:13:00', 'nothing'),
    ('2018/10/23 09:13:30', 'nothing'),
    ('2018/10/23 18:26:30', 'nothing'),
    ('2018/10/24 07:37:30', 'nothing'),
    ('2018/10/25 17:44:30', 'nothing'),
    ('2018/10/25 19:34:30', 'nothing'),

    # 34 iteracia - All, 4 mesiace, 5;5
    ('2018/10/16 21:08:30', 'nothing'),
    ('2018/10/24 07:36:30', 'nothing'),
    ('2018/10/13 13:25:00', 'nothing'),
    ('2018/10/14 12:54:30', 'nothing'),
    ('2018/10/14 12:55:00', 'nothing'),
    ('2018/10/14 15:00:30', 'nothing'),
    ('2018/10/14 20:43:30', 'nothing'),
    ('2019/01/18 11:27:30', 'nothing'),
    ('2019/01/24 12:02:30', 'nothing'),
    ('2019/01/24 19:27:00', 'nothing'),

    # 35 iteracia - All, 4 mesiace, 5;5
    ('2018/10/13 16:06:30', 'nothing'),
    ('2018/10/17 12:38:00', 'nothing'),
    ('2018/11/09 23:28:30', 'nothing'),
    ('2019/01/17 20:58:00', 'nothing'),
    ('2019/01/17 20:59:00', 'nothing'),

    # 36 iteracia - All, 4 mesiace, 5;5
    ('2018/10/19 10:54:30', 'nothing'),

    # 37 iteracia - All, 4 mesiace, 5;5
    ('2018/10/09 14:29:30', 'nothing'),
    ('2018/10/10 16:23:00', 'nothing'),
    ('2018/10/12 11:36:00', 'nothing'),
    ('2018/10/12 21:45:30', 'nothing'),
    ('2018/10/17 07:06:00', 'nothing'),
    ('2018/10/17 15:55:00', 'nothing'),
    ('2018/10/19 10:54:30', 'nothing'),
    ('2018/10/24 03:22:00', 'nothing'),
    ('2018/10/26 06:59:00', 'nothing'),
    ('2018/10/26 21:09:30', 'nothing'),

    # 38 iteracia - All, 4 mesiace, 5;5
    ('2018/10/12 14:01:00', 'nothing'),
    ('2018/10/17 23:51:30', 'nothing'),
    ('2018/10/17 23:52:00', 'nothing'),
    ('2018/10/31 07:16:00', 'nothing'),
    ('2018/11/07 07:22:30', 'nothing'),
    ('2018/12/06 17:45:00', 'nothing'),
    ('2018/12/06 17:45:30', 'nothing'),
    ('2018/12/06 17:46:00', 'nothing'),

    # 39 iteracia - All, 4 mesiace, 5;5
    ('2018/10/09 15:33:00', 'nothing'),
    ('2018/10/11 13:48:30', 'nothing'),
    ('2018/10/12 14:01:00', 'nothing'),
    ('2018/10/16 07:14:30', 'nothing'),
    ('2018/10/17 12:38:30', 'nothing'),
    ('2018/10/19 10:54:30', 'nothing'),
    ('2018/10/20 02:35:00', 'nothing'),
    ('2018/10/20 06:25:30', 'nothing'),
    ('2018/10/20 16:46:30', 'nothing'),
    ('2018/10/20 23:04:00', 'nothing'),

    # 40 iteracia - All, 4 mesiace, 4;4
    ('2018/10/24 07:36:00', 'nothing'),
    ('2018/11/04 09:45:30', 'nothing'),
    ('2018/10/16 21:07:30', 'nothing'),
    ('2018/10/16 21:08:00', 'nothing'),
    ('2018/10/17 12:37:00', 'nothing'),
    ('2018/10/17 12:37:30', 'nothing'),
    ('2018/10/22 12:12:30', 'nothing'),
    ('2018/10/22 16:40:30', 'nothing'),
    ('2018/10/23 18:24:30', 'nothing'),
    ('2018/11/26 12:14:30', 'nothing'),

    # 41 iteracia - All, 4 mesiace, 4;4
    ('2019/01/31 03:53:30', 'nothing'),

    # 42 iteracia - All, 4 mesiace, 4;3
    ('2018/10/14 14:58:30', 'nothing'),
    ('2018/10/22 16:39:30', 'nothing'),
    ('2018/11/04 09:45:00', 'nothing'),
    ('2018/10/10 20:30:30', 'nothing'),
    ('2018/10/14 14:58:30', 'nothing'),
    ('2018/10/17 12:36:00', 'nothing'),
    ('2018/10/17 12:36:30', 'nothing'),
    ('2018/10/19 10:52:30', 'nothing'),
    ('2018/10/21 20:28:00', 'nothing'),
    ('2018/10/22 16:39:30', 'nothing'),

    # 43 iteracia - All, 4 mesiace, 4;3
    ('2018/10/22 16:39:30', 'nothing'),
    ('2019/01/28 04:40:00', 'nothing'),
    ('2019/01/31 03:53:00', 'nothing'),
    ('2019/01/31 03:53:30', 'nothing'),
    ('2018/10/17 12:36:00', 'nothing'),

    # 44 iteracia - All, 4 mesiace, 4;3
    ('2018/11/10 23:14:30', 'nothing'),
    ('2019/01/15 15:10:30', 'nothing'),

    # final 4 mesiace, 3;3
]


def func(con, table_name, timestamp, row_selector, interval_selector):
    attrs = []
    columns = [
        'co2_in_ppm'
    ]
    precision = 2

    for column in columns:
        for normalize in [False]:
            intervals_before = [x for x in range(5, 901, 10)]
            intervals_after = [x for x in range(5, 181, 10)]

            #
            # linearny posun
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

            pr = ''
            be, af = op.geometric_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.arithmetic_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.variance(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.standard_deviation(column, precision, b, a, pr)
            attrs += be + af

            #
            # linearny posun
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

            pr = 'B_linearne'
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

            pr = 'B_x2'
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
                              intervals_before=[x * x for x in range(2, 31, 1)],
                              intervals_after=[x * x for x in range(2, 14, 1)],
                              window_size_before=20 * 60, window_size_after=3 * 60,
                              prefix='_x2')
            attrs += b + a

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

            pr = 'B_x3'
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
                              intervals_before=[x * x * x for x in range(2, 10, 1)],
                              intervals_after=[x * x * x for x in range(2, 6, 1)],
                              window_size_before=20 * 60, window_size_after=3 * 60,
                              prefix='_x3')
            attrs += b + a

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

    # selector pre data
    row_selector = CachedDiffRowWithIntervalSelector(con, table_name, 0, 0)
    interval_selector = None

    # trenovacia mnozina
    logging.info('start computing of training set')
    training, tr_events = AttributeUtil.training_data(con, table_name, filtered, func,
                                                      row_selector, interval_selector, 'open')
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

    file_names = [
        'co2_1_oktober.csv',
        'co2_2_november.csv',
        'co2_3_december.csv',
        'co2_4_januar.csv',
        'co2_5_februar.csv',
        'co2_6_marec.csv',
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
