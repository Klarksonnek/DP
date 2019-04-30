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
    ('2018/10/08 00:07:30', 'nothing'),
    ('2018/10/08 00:55:30', 'nothing'),
    ('2018/10/08 23:20:30', 'nothing'),
    ('2018/10/09 10:21:30', 'nothing'),
    ('2018/10/09 11:10:00', 'nothing'),
    ('2018/10/09 14:13:00', 'nothing'),
    ('2018/10/09 22:51:00', 'nothing'),
    ('2018/10/09 22:55:30', 'nothing'),
    ('2018/10/11 13:48:30', 'nothing'),
    ('2018/10/11 19:07:30', 'nothing'),

    # 02 iteracia - SVM, 4 mesiace, 2;3
    ('2018/10/07 09:01:00', 'nothing'),
    ('2018/10/07 16:18:30', 'nothing'),
    ('2018/10/08 20:41:30', 'nothing'),
    ('2018/10/08 20:57:00', 'nothing'),
    ('2018/10/10 22:58:30', 'nothing'),
    ('2018/10/10 23:13:00', 'nothing'),
    ('2018/10/11 13:47:30', 'nothing'),
    ('2018/10/16 17:02:30', 'nothing'),
    ('2018/10/17 10:51:30', 'nothing'),
    ('2018/10/18 19:56:30', 'nothing'),

    # 03 iteracia - SVM, 4 mesiace, 2;3
    ('2018/10/07 08:58:00', 'nothing'),
    ('2018/10/07 11:36:00', 'nothing'),
    ('2018/10/08 19:20:00', 'nothing'),
    ('2018/10/09 22:28:00', 'nothing'),
    ('2018/10/11 18:51:30', 'nothing'),
    ('2018/10/13 13:25:30', 'nothing'),
    ('2018/10/13 18:31:30', 'nothing'),
    ('2018/10/14 00:40:00', 'nothing'),
    ('2018/10/14 09:08:30', 'nothing'),
    ('2018/10/14 18:41:30', 'nothing'),

    # 04 iteracia - SVM, 4 mesiace, 2;3
    ('2018/10/09 10:44:30', 'nothing'),
    ('2018/10/14 22:28:00', 'nothing'),
    ('2018/10/16 21:08:00', 'nothing'),
    ('2018/10/17 10:47:30', 'nothing'),
    ('2018/10/17 23:51:00', 'nothing'),
    ('2018/10/18 20:07:00', 'nothing'),
    ('2018/10/19 07:04:30', 'nothing'),
    ('2018/10/19 10:52:30', 'nothing'),
    ('2018/10/21 20:28:00', 'nothing'),
    ('2018/10/22 15:00:30', 'nothing'),

    # 05 iteracia - SVM, 4 mesiace, 2;3
    ('2018/10/09 10:45:30', 'nothing'),
    ('2018/10/15 00:26:00', 'nothing'),
    ('2018/10/19 07:06:00', 'nothing'),
    ('2018/10/22 12:33:00', 'nothing'),
    ('2018/10/22 16:39:30', 'nothing'),
    ('2018/10/28 08:04:00', 'nothing'),
    ('2018/10/28 15:39:30', 'nothing'),
    ('2018/10/31 00:15:00', 'nothing'),
    ('2018/10/31 23:35:00', 'nothing'),
    ('2018/11/02 20:30:00', 'nothing'),

    # 06 iteracia - SVM, 4 mesiace, 2;3
    ('2018/10/07 11:42:00', 'nothing'),
    ('2018/10/15 23:49:30', 'nothing'),
    ('2018/10/16 21:16:00', 'nothing'),
    ('2018/10/18 20:08:00', 'nothing'),
    ('2018/10/24 05:33:00', 'nothing'),
    ('2018/10/31 07:24:30', 'nothing'),
    ('2018/11/10 05:04:00', 'nothing'),
    ('2018/11/10 06:37:30', 'nothing'),
    ('2018/11/10 23:22:00', 'nothing'),
    ('2019/01/29 23:06:00', 'nothing'),

    # 07 iteracia - SVM, 4 mesiace, 2;3
    ('2018/10/17 12:36:30', 'nothing'),
    ('2018/10/19 10:52:30', 'nothing'),
    ('2018/11/10 03:05:30', 'nothing'),
    ('2018/11/10 06:38:00', 'nothing'),
    ('2018/11/20 18:23:00', 'nothing'),
    ('2018/11/24 07:35:00', 'nothing'),
    ('2018/12/01 04:33:00', 'nothing'),
    ('2019/01/08 03:18:30', 'nothing'),
    ('2019/01/08 14:42:30', 'nothing'),
    ('2019/01/09 15:47:30', 'nothing'),

    # 08 iteracia - SVM, 4 mesiace, 2;3
    ('2018/10/18 20:06:00', 'nothing'),
    ('2018/10/22 16:39:30', 'nothing'),
    ('2018/10/24 05:32:30', 'nothing'),
    ('2018/11/05 18:02:30', 'nothing'),
    ('2018/11/10 03:04:30', 'nothing'),
    ('2018/11/10 03:59:30', 'nothing'),
    ('2018/11/10 04:12:00', 'nothing'),
    ('2018/11/10 04:56:30', 'nothing'),
    ('2018/11/10 05:03:30', 'nothing'),
    ('2018/11/10 06:37:00', 'nothing'),

    # 09 iteracia - SVM, 4 mesiace, 2;3
    ('2018/10/14 00:01:30', 'nothing'),
    ('2018/10/14 14:59:00', 'nothing'),
    ('2018/10/21 20:27:30', 'nothing'),
    ('2018/10/23 18:24:30', 'nothing'),
    ('2018/10/31 07:16:30', 'nothing'),
    ('2018/11/08 12:23:30', 'nothing'),
    ('2018/11/09 23:29:30', 'nothing'),
    ('2018/11/10 03:08:30', 'nothing'),
    ('2018/11/10 23:25:00', 'nothing'),
    ('2018/11/16 11:54:00', 'nothing'),

    # 10 iteracia - SVM, 4 mesiace, 2;3
    ('2018/11/10 02:30:30', 'nothing'),
    ('2019/01/10 09:38:00', 'nothing'),
    ('2019/01/15 15:10:30', 'nothing'),
    ('2019/01/18 09:59:00', 'nothing'),
    ('2019/01/28 04:39:30', 'nothing'),
    ('2018/10/17 12:36:00', 'nothing'),
    ('2018/10/17 12:36:30', 'nothing'),
    ('2018/10/31 07:17:00', 'nothing'),
    ('2018/10/31 07:17:30', 'nothing'),
    ('2018/11/09 23:27:30', 'nothing'),

    # 11 iteracia - SVM, 4 mesiace, 2;3
    ('2018/10/14 18:47:00', 'nothing'),
    ('2018/10/17 12:36:00', 'nothing'),
    ('2018/11/09 23:28:30', 'nothing'),
    ('2018/11/11 01:07:00', 'nothing'),
    ('2018/11/11 01:07:30', 'nothing'),
    ('2018/11/11 01:08:00', 'nothing'),

    # 12 iteracia - SVM, 4 mesiace, 2;3
    ('2018/11/10 04:23:00', 'nothing'),
    ('2019/01/18 09:59:00', 'nothing'),
    ('2019/01/31 03:53:00', 'nothing'),

    # 13 iteracia - SVM, 4 mesiace, 2;3
    ('2018/10/31 07:16:30', 'nothing'),
    ('2018/11/10 23:14:00', 'nothing'),

    # 14 iteracia - SVM, 4 mesiace, 2;3
    ('2019/01/18 09:59:00', 'nothing'),

    # 15 iteracia - Neural, 4 mesiace, 2;3
    ('2018/10/10 20:59:30', 'nothing'),
    ('2018/10/14 22:55:30', 'nothing'),
    ('2018/10/15 13:53:30', 'nothing'),
    ('2018/10/16 21:33:30', 'nothing'),
    ('2018/10/17 15:18:30', 'nothing'),
    ('2018/10/19 13:51:00', 'nothing'),
    ('2018/10/20 16:40:30', 'nothing'),
    ('2018/10/20 19:09:30', 'nothing'),
    ('2018/10/21 02:55:30', 'nothing'),
    ('2018/10/21 04:44:30', 'nothing'),

    # 16 iteracia - Neural, 4 mesiace, 2;3
    ('2018/10/22 16:39:30', 'nothing'),
    ('2018/10/24 21:52:00', 'nothing'),
    ('2018/11/10 02:02:30', 'nothing'),
    ('2018/11/10 04:26:00', 'nothing'),
    ('2018/11/11 23:13:00', 'nothing'),
    ('2018/12/01 23:26:30', 'nothing'),
    ('2019/01/10 08:51:30', 'nothing'),
    ('2019/01/12 10:45:00', 'nothing'),
    ('2019/01/24 12:30:30', 'nothing'),
    ('2019/01/26 15:36:30', 'nothing'),

    # 17 iteracia - Neural, 4 mesiace, 2;3
    ('2018/10/24 03:21:30', 'nothing'),
    ('2018/10/24 03:22:00', 'nothing'),
    ('2018/12/02 21:14:00', 'nothing'),
    ('2018/12/06 17:45:00', 'nothing'),
    ('2019/01/15 15:11:00', 'nothing'),
    ('2019/01/28 04:27:30', 'nothing'),

    # 18 iteracia - Neural, 4 mesiace, 2;3
    ('2018/10/08 02:17:30', 'nothing'),
    ('2018/10/09 01:28:30', 'nothing'),
    ('2018/10/09 23:40:30', 'nothing'),
    ('2018/10/13 17:27:00', 'nothing'),
    ('2018/10/18 07:17:30', 'nothing'),
    ('2018/10/19 01:51:30', 'nothing'),
    ('2018/10/19 02:53:00', 'nothing'),
    ('2018/10/19 05:26:30', 'nothing'),
    ('2018/10/22 12:40:00', 'nothing'),
    ('2018/10/24 01:16:00', 'nothing'),

    # 19 iteracia - Neural, 4 mesiace, 2;3
    ('2018/10/24 04:25:00', 'nothing'),
    ('2018/10/24 04:57:30', 'nothing'),
    ('2018/10/24 06:55:30', 'nothing'),
    ('2018/10/27 13:23:00', 'nothing'),
    ('2018/11/01 19:35:00', 'nothing'),
    ('2018/11/03 12:29:00', 'nothing'),
    ('2018/11/10 00:46:30', 'nothing'),
    ('2018/11/10 05:01:00', 'nothing'),
    ('2018/11/14 02:25:00', 'nothing'),
    ('2018/11/23 13:49:30', 'nothing'),

    # 20 iteracia - Neural, 4 mesiace, 2;3
    ('2018/10/09 09:17:00', 'nothing'),
    ('2018/10/10 11:56:00', 'nothing'),
    ('2018/10/15 13:20:00', 'nothing'),
    ('2018/10/24 03:21:30', 'nothing'),
    ('2018/10/31 07:17:00', 'nothing'),
    ('2018/11/03 01:26:30', 'nothing'),
    ('2018/11/08 19:15:00', 'nothing'),
    ('2018/11/11 01:06:30', 'nothing'),
    ('2018/11/24 02:54:30', 'nothing'),
    ('2018/11/24 07:20:30', 'nothing'),

    # 21 iteracia - Neural, 4 mesiace, 2;3
    ('2018/10/07 09:00:30', 'nothing'),
    ('2018/10/07 11:36:30', 'nothing'),
    ('2018/10/11 18:47:30', 'nothing'),
    ('2018/10/11 20:56:30', 'nothing'),
    ('2018/10/11 21:00:00', 'nothing'),
    ('2018/10/13 11:11:00', 'nothing'),
    ('2018/10/13 13:32:00', 'nothing'),
    ('2018/10/14 10:54:30', 'nothing'),
    ('2018/10/14 15:01:30', 'nothing'),
    ('2018/10/14 18:45:30', 'nothing'),

    # 22 iteracia - Neural, 4 mesiace, 2;3
    ('2018/10/22 16:40:00', 'nothing'),
    ('2018/10/24 03:21:00', 'nothing'),
    ('2018/10/24 05:02:00', 'nothing'),
    ('2018/10/28 09:39:30', 'nothing'),
    ('2018/10/28 13:02:30', 'nothing'),
    ('2018/11/09 23:06:30', 'nothing'),
    ('2018/11/24 04:01:00', 'nothing'),
    ('2018/11/24 07:20:00', 'nothing'),
    ('2018/12/08 06:11:30', 'nothing'),
    ('2018/12/09 04:44:30', 'nothing'),

    # 23 iteracia - Neural, 4 mesiace, 2;3
    ('2018/10/07 11:35:30', 'nothing'),
    ('2018/10/15 13:14:30', 'nothing'),
    ('2018/10/19 06:52:00', 'nothing'),
    ('2018/10/31 07:16:00', 'nothing'),
    ('2018/11/09 22:01:30', 'nothing'),
    ('2018/11/09 23:14:30', 'nothing'),
    ('2018/11/10 02:28:30', 'nothing'),
    ('2018/11/10 03:04:00', 'nothing'),
    ('2018/11/13 14:39:00', 'nothing'),
    ('2018/11/24 04:02:30', 'nothing'),

    # 24 iteracia - Neural, 4 mesiace, 2;3
    ('2018/10/15 13:14:00', 'nothing'),
    ('2018/10/15 13:20:30', 'nothing'),
    ('2018/10/19 14:40:30', 'nothing'),
    ('2018/10/19 17:54:00', 'nothing'),
    ('2018/10/19 18:39:30', 'nothing'),
    ('2018/10/19 21:47:30', 'nothing'),
    ('2018/10/19 22:20:30', 'nothing'),
    ('2018/10/20 07:13:00', 'nothing'),
    ('2018/10/20 15:40:00', 'nothing'),
    ('2018/10/20 18:33:00', 'nothing'),

    # 25 iteracia - Tree, 4 mesiace, 2;3
    ('2019/01/10 09:39:00', 'nothing'),

    # 26 iteracia - RTree, 4 mesiace, 2;3
    ('2019/01/28 04:28:00', 'nothing'),
    ('2019/01/28 04:28:30', 'nothing'),

    # 27 iteracia - RTree, 4 mesiace, 2;3
    ('2018/10/31 07:14:30', 'nothing'),
    ('2018/11/10 01:47:00', 'nothing'),
    ('2018/11/11 04:34:00', 'nothing'),
    ('2018/11/24 07:32:00', 'nothing'),
    ('2018/11/28 03:33:30', 'nothing'),
    ('2018/12/01 04:31:00', 'nothing'),
    ('2018/12/01 17:57:30', 'nothing'),
    ('2018/12/02 00:06:00', 'nothing'),
    ('2018/12/16 05:55:00', 'nothing'),
    ('2019/01/14 07:12:30', 'nothing'),

    # 28 iteracia - RTree, 4 mesiace, 2;3
    ('2018/10/24 03:21:30', 'nothing'),
    ('2018/10/24 05:31:00', 'nothing'),
    ('2018/10/24 05:31:30', 'nothing'),
    ('2018/11/10 04:55:30', 'nothing'),
    ('2019/01/29 23:04:00', 'nothing'),
    ('2019/01/29 23:04:30', 'nothing'),

    # 29 iteracia - All, 4 mesiace, 2;3
    ('2018/10/08 00:07:30', 'nothing'),
    ('2018/10/08 00:55:30', 'nothing'),
    ('2018/10/08 19:09:30', 'nothing'),
    ('2018/10/09 10:21:30', 'nothing'),
    ('2018/10/09 10:52:30', 'nothing'),
    ('2018/10/09 11:10:00', 'nothing'),
    ('2018/10/09 14:13:00', 'nothing'),
    ('2018/10/11 13:48:30', 'nothing'),
    ('2018/10/11 19:07:30', 'nothing'),
    ('2018/10/13 01:58:00', 'nothing'),

    # 30 iteracia - All, 4 mesiace, 2;3
    ('2019/01/17 20:58:00', 'nothing'),
    ('2019/01/17 20:58:30', 'nothing'),
    ('2019/01/17 20:59:00', 'nothing'),
    ('2018/10/21 05:25:00', 'nothing'),
    ('2018/11/29 12:29:00', 'nothing'),
    ('2018/12/17 08:03:00', 'nothing'),
    ('2018/12/18 12:57:30', 'nothing'),
    ('2018/12/21 12:41:00', 'nothing'),
    ('2018/12/21 23:33:30', 'nothing'),
    ('2018/12/23 16:38:30', 'nothing'),

    # 31 iteracia - All, 4 mesiace, 2;3
    ('2018/10/09 15:32:30', 'nothing'),
    ('2018/10/07 16:35:30', 'nothing'),
    ('2018/10/07 20:57:30', 'nothing'),
    ('2018/10/13 07:34:30', 'nothing'),
    ('2018/10/11 19:06:30', 'nothing'),
    ('2018/10/16 00:29:30', 'nothing'),
    ('2018/10/16 21:31:00', 'nothing'),
    ('2018/10/16 23:55:00', 'nothing'),
    ('2018/10/31 17:06:30', 'nothing'),
    ('2018/10/31 23:10:00', 'nothing'),

    # 32 iteracia - All, 4 mesiace, 2;3
    ('2018/10/07 16:36:00', 'nothing'),
    ('2018/10/10 20:02:00', 'nothing'),
    ('2018/10/15 00:16:30', 'nothing'),
    ('2018/10/15 18:52:30', 'nothing'),
    ('2018/10/23 19:03:00', 'nothing'),
    ('2018/11/03 13:20:30', 'nothing'),
    ('2018/11/03 21:06:30', 'nothing'),
    ('2018/11/06 09:39:00', 'nothing'),
    ('2018/11/05 22:05:30', 'nothing'),
    ('2018/12/01 04:32:30', 'nothing'),

    # 33 iteracia - All, 4 mesiace, 2;3
    ('2018/10/09 17:26:30', 'nothing'),
    ('2018/10/09 11:21:00', 'nothing'),
    ('2018/10/11 14:30:00', 'nothing'),
    ('2018/10/15 09:02:00', 'nothing'),
    ('2018/10/20 19:11:00', 'nothing'),
    ('2018/10/29 19:56:00', 'nothing'),
    ('2018/11/02 15:23:00', 'nothing'),
    ('2018/11/06 21:46:00', 'nothing'),
    ('2018/11/10 06:11:30', 'nothing'),
    ('2018/11/22 18:12:00', 'nothing'),

    # 34 iteracia - , 4 mesiace, 2;3
    ('2018/10/07 20:56:30', 'nothing'),
    ('2018/10/09 23:02:00', 'nothing'),
    ('2018/10/13 12:38:30', 'nothing'),
    ('2018/10/17 21:47:30', 'nothing'),
    ('2018/10/21 19:29:30', 'nothing'),
    ('2018/11/04 08:34:00', 'nothing'),
    ('2018/11/18 23:55:00', 'nothing'),
    ('2018/11/28 07:30:00', 'nothing'),
    ('2018/12/24 05:55:00', 'nothing'),
    ('2019/01/02 02:07:00', 'nothing'),

    # 35 iteracia - All, 4 mesiace, 2;3
    ('2018/10/11 10:49:30', 'nothing'),
    ('2018/10/28 11:49:00', 'nothing'),
    ('2018/10/31 07:30:30', 'nothing'),
    ('2018/11/04 08:22:30', 'nothing'),
    ('2018/11/10 01:23:00', 'nothing'),
    ('2018/11/13 20:14:00', 'nothing'),
    ('2018/11/18 20:23:00', 'nothing'),
    ('2018/11/20 19:59:30', 'nothing'),
    ('2018/12/02 04:30:30', 'nothing'),
    ('2019/01/08 00:10:30', 'nothing'),

    # 36 iteracia - All, 4 mesiace, 2;3
    ('2018/10/11 12:44:30', 'nothing'),
    ('2018/10/17 16:59:30', 'nothing'),
    ('2018/10/29 23:47:30', 'nothing'),
    ('2018/11/06 23:35:00', 'nothing'),
    ('2018/11/11 00:07:00', 'nothing'),
    ('2018/11/24 16:58:00', 'nothing'),
    ('2018/12/08 11:25:00', 'nothing'),
    ('2019/01/10 11:03:30', 'nothing'),
    ('2019/01/26 00:02:30', 'nothing'),
    ('2019/01/27 12:50:30', 'nothing'),

    # 37 iteracia - All, 4 mesiace, 2;3
    ('2018/10/09 10:52:00', 'nothing'),
    ('2018/10/17 19:22:00', 'nothing'),
    ('2018/11/07 16:49:30', 'nothing'),
    ('2018/11/10 00:58:00', 'nothing'),
    ('2018/11/10 04:09:30', 'nothing'),
    ('2018/11/13 14:54:00', 'nothing'),
    ('2018/12/05 17:57:00', 'nothing'),
    ('2019/01/09 16:01:00', 'nothing'),
    ('2019/01/29 23:15:30', 'nothing'),
    ('2018/10/28 13:32:30', 'nothing'),

    # 38 iteracia - All, 4 mesiace, 2;3
    ('2018/10/09 16:49:30', 'nothing'),
    ('2018/10/13 14:14:30', 'nothing'),
    ('2018/10/16 14:55:00', 'nothing'),
    ('2018/10/24 06:09:30', 'nothing'),
    ('2018/10/29 23:49:30', 'nothing'),
    ('2018/11/03 01:26:00', 'nothing'),
    ('2018/11/20 20:03:30', 'nothing'),
    ('2018/11/29 17:40:00', 'nothing'),
    ('2018/12/12 08:36:30', 'nothing'),
    ('2019/01/28 04:38:00', 'nothing'),

    # 39 iteracia - All, 4 mesiace, 2;3
    ('2018/10/09 17:26:00', 'nothing'),
    ('2018/10/15 11:49:30', 'nothing'),
    ('2018/10/28 08:10:30', 'nothing'),
    ('2018/11/07 04:38:00', 'nothing'),
    ('2018/11/10 00:47:30', 'nothing'),
    ('2018/11/10 04:09:00', 'nothing'),
    ('2018/11/13 11:19:30', 'nothing'),
    ('2018/11/24 00:40:30', 'nothing'),
    ('2018/12/06 13:17:30', 'nothing'),
    ('2019/01/26 00:01:30', 'nothing'),

    # 40 iteracia - All, 4 mesiace, 2;3
    ('2018/10/07 13:54:30', 'nothing'),
    ('2018/10/11 14:55:30', 'nothing'),
    ('2018/10/15 18:35:00', 'nothing'),
    ('2018/10/18 20:11:00', 'nothing'),
    ('2018/10/22 11:48:30', 'nothing'),
    ('2018/11/07 09:52:00', 'nothing'),
    ('2018/11/13 17:03:30', 'nothing'),
    ('2018/12/03 22:20:30', 'nothing'),
    ('2018/12/22 19:01:30', 'nothing'),
    ('2019/01/17 18:17:30', 'nothing'),

    # 41 iteracia - All, 4 mesiace, 2;3
    ('2018/10/07 18:34:30', 'nothing'),
    ('2018/10/18 01:44:00', 'nothing'),
    ('2018/10/23 01:04:00', 'nothing'),
    ('2018/10/26 10:46:00', 'nothing'),
    ('2018/10/27 01:15:30', 'nothing'),
    ('2018/10/28 07:24:00', 'nothing'),
    ('2018/11/01 19:34:30', 'nothing'),
    ('2018/11/10 02:14:00', 'nothing'),
    ('2018/11/13 15:01:30', 'nothing'),
    ('2018/11/23 11:51:30', 'nothing'),

    # 42 iteracia - All, 4 mesiace, 2;3
    ('2018/10/07 12:00:00', 'nothing'),
    ('2018/10/11 17:26:00', 'nothing'),
    ('2018/10/21 10:01:30', 'nothing'),
    ('2018/10/31 22:51:30', 'nothing'),
    ('2018/11/20 20:01:00', 'nothing'),
    ('2018/12/07 10:28:30', 'nothing'),
    ('2019/01/11 15:20:00', 'nothing'),
    ('2019/01/29 22:49:30', 'nothing'),
    ('2019/01/29 06:41:30', 'nothing'),
    ('2018/11/13 20:14:30', 'nothing'),

    # 43 iteracia - All, 4 mesiace, 2;3
    ('2018/10/09 13:30:30', 'nothing'),
    ('2018/10/15 08:57:00', 'nothing'),
    ('2018/10/21 03:22:00', 'nothing'),
    ('2018/10/30 18:22:00', 'nothing'),
    ('2018/11/13 20:03:30', 'nothing'),
    ('2018/12/06 17:45:30', 'nothing'),
    ('2018/12/25 02:11:30', 'nothing'),
    ('2019/01/31 19:22:00', 'nothing'),
    ('2019/01/22 17:08:30', 'nothing'),
    ('2018/11/20 20:29:00', 'nothing'),

    # 44 iteracia - All, 4 mesiace, 2;3
    ('2018/10/09 10:20:30', 'nothing'),
    ('2018/10/17 23:51:30', 'nothing'),
    ('2018/10/27 13:23:30', 'nothing'),
    ('2018/11/03 19:53:00', 'nothing'),
    ('2018/11/07 16:32:00', 'nothing'),
    ('2018/11/11 11:37:30', 'nothing'),
    ('2018/11/24 18:27:30', 'nothing'),
    ('2018/12/01 21:11:00', 'nothing'),
    ('2018/12/09 02:11:30', 'nothing'),
    ('2019/01/30 05:33:30', 'nothing'),

    # 45 iteracia - All, 4 mesiace, 2;3
    ('2018/10/09 10:21:00', 'nothing'),
    ('2018/10/17 16:31:00', 'nothing'),
    ('2018/10/28 15:38:30', 'nothing'),
    ('2018/11/09 22:46:00', 'nothing'),
    ('2018/11/10 01:56:00', 'nothing'),
    ('2018/11/10 04:57:00', 'nothing'),
    ('2018/11/18 13:47:00', 'nothing'),
    ('2019/01/15 15:10:00', 'nothing'),
    ('2019/01/18 10:14:30', 'nothing'),
    ('2019/01/30 13:27:00', 'nothing'),

    # 46 iteracia - All, 4 mesiace, 2;3
    ('2018/10/14 22:56:00', 'nothing'),
    ('2018/10/15 13:22:00', 'nothing'),
    ('2018/10/16 07:16:00', 'nothing'),
    ('2018/10/16 21:34:00', 'nothing'),
    ('2018/10/18 07:11:30', 'nothing'),
    ('2018/10/29 12:45:00', 'nothing'),
    ('2019/01/30 05:34:00', 'nothing'),
    ('2019/01/10 08:49:00', 'nothing'),
    ('2018/11/10 05:25:00', 'nothing'),
    ('2018/11/10 04:02:30', 'nothing'),

    # 47 iteracia - All, 4 mesiace, 2;3
    ('2018/10/09 17:25:30', 'nothing'),
    ('2018/10/17 14:33:30', 'nothing'),
    ('2018/10/18 17:40:00', 'nothing'),
    ('2018/11/03 17:26:30', 'nothing'),
    ('2018/11/10 00:47:00', 'nothing'),
    ('2018/11/10 03:06:00', 'nothing'),
    ('2018/11/20 10:36:00', 'nothing'),
    ('2018/11/26 11:51:30', 'nothing'),
    ('2018/12/24 20:36:30', 'nothing'),
    ('2019/01/15 00:03:00', 'nothing'),

    # 48 iteracia - All, 4 mesiace, 2;3
    ('2018/10/11 14:29:00', 'nothing'),
    ('2018/11/02 18:33:30', 'nothing'),
    ('2018/10/09 18:57:30', 'nothing'),
    ('2018/11/09 22:23:00', 'nothing'),
    ('2018/11/09 23:26:00', 'nothing'),
    ('2018/11/10 00:30:00', 'nothing'),
    ('2018/12/29 02:13:00', 'nothing'),
    ('2019/01/08 14:41:30', 'nothing'),
    ('2019/01/09 16:45:00', 'nothing'),
    ('2019/01/26 15:17:00', 'nothing'),

    # 49 iteracia - All, 4 mesiace, 2;3
    ('2018/10/14 00:39:00', 'nothing'),
    ('2018/10/16 07:14:30', 'nothing'),
    ('2018/10/31 22:41:00', 'nothing'),
    ('2018/11/10 01:27:00', 'nothing'),
    ('2018/11/11 22:47:00', 'nothing'),
    ('2018/12/01 20:48:00', 'nothing'),
    ('2018/12/15 22:13:30', 'nothing'),
    ('2018/12/19 10:45:30', 'nothing'),
    ('2018/12/23 18:05:00', 'nothing'),
    ('2019/01/24 17:35:30', 'nothing'),

    # 50 iteracia - All, 4 mesiace, 2;3
    ('2018/11/09 23:28:00', 'nothing'),
    ('2018/11/30 23:05:00', 'nothing'),
    ('2018/12/07 23:17:30', 'nothing'),

    # 51 iteracia - All, 4 mesiace, 2;3
    ('2018/10/11 14:28:00', 'nothing'),
    ('2018/10/17 19:18:30', 'nothing'),
    ('2018/10/27 16:49:00', 'nothing'),
    ('2018/11/03 16:49:30', 'nothing'),
    ('2018/11/04 10:04:30', 'nothing'),
    ('2018/11/04 19:37:00', 'nothing'),
    ('2018/11/07 07:23:00', 'nothing'),
    ('2018/11/12 11:58:00', 'nothing'),
    ('2018/12/08 11:11:00', 'nothing'),
    ('2018/12/26 01:29:00', 'nothing'),

    # 52 iteracia - All, 4 mesiace, 2;3
    ('2018/10/15 01:23:30', 'nothing'),
    ('2018/11/09 22:50:00', 'nothing'),
    ('2018/11/09 23:51:30', 'nothing'),
    ('2019/01/17 20:57:30', 'nothing'),
]


def func(con, table_name, timestamp, row_selector, interval_selector):
    attrs = []
    columns = [
        'co2_in_ppm'
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


def training_set(events_file: str, no_event_time_shift: int, table_name: str, directory):
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
    training, tr_events = AttributeUtil.cached_training_data(con, table_name, filtered, func,
                                                             row_selector, interval_selector,
                                                             'open',
                                                             '{0}/testing_cached.csv'.format(directory))
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
    CSVUtil.create_csv_file(balanced, '{0}/training.csv'.format(directory))
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


def testing_month(table_name, start, directory):
    mesiac = 30 * 24 * 3600

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


def generic_testing(directory):
    end = int(DateTimeUtil.local_time_str_to_utc('2019/04/29 15:00:00').timestamp())

    # Peto , februar, marec, april
    start = int(DateTimeUtil.local_time_str_to_utc('2019/02/04 06:00:00').timestamp())
    testing_set('measured_filtered_peto', start, end, '{0}/gt_peto.csv'.format(directory))

    # David
    start = int(DateTimeUtil.local_time_str_to_utc('2019/04/03 16:00:00').timestamp())
    testing_set('measured_david', start, end, '{0}/gt_david.csv'.format(directory))

    # Martin
    start = int(DateTimeUtil.local_time_str_to_utc('2019/04/01 15:00:00').timestamp())
    testing_set('measured_martin', start, end, '{0}/gt_martin.csv'.format(directory))

    # Klarka
    start = int(DateTimeUtil.local_time_str_to_utc('2018/12/18 12:00:00').timestamp())
    testing_set('measured_klarka', start, end, '{0}/gt_klarka.csv'.format(directory))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    # tabulka s CO2, ktora neprekroci hranicu 2000ppm
    table_name = 'measured_filtered_peto'

    directory = 'co2'
    if not os.path.isdir(directory):
        os.mkdir(directory)

    training_set('examples/events_peto.json', -500, table_name, directory)

    start = int(DateTimeUtil.local_time_str_to_utc('2018/10/07 06:00:00').timestamp())
    testing_set(table_name, start, start + 100, '{0}/testing.csv'.format(directory))

    # testing_month(table_name, start)
    # generic_testing(directory)
