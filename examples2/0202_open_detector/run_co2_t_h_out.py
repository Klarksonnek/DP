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
    ('2018/10/09 14:45:30', 'nothing'),
    ('2018/10/11 11:32:00', 'nothing'),
    ('2018/10/13 07:28:00', 'nothing'),
    ('2018/10/16 07:16:30', 'nothing'),
    ('2018/10/17 16:32:00', 'nothing'),
    ('2018/10/24 05:33:30', 'nothing'),
    ('2018/11/02 06:15:00', 'nothing'),
    ('2018/11/02 14:46:30', 'nothing'),
    ('2018/11/07 11:00:00', 'nothing'),
    ('2018/11/26 22:18:00', 'nothing'),

    # 02 iteracia - SVM, 4 mesiace, 2;3
    ('2018/10/07 15:56:30', 'nothing'),
    ('2018/10/08 22:44:30', 'nothing'),
    ('2018/10/11 10:55:30', 'nothing'),
    ('2018/10/15 13:21:30', 'nothing'),
    ('2018/10/16 11:05:30', 'nothing'),
    ('2018/10/29 07:39:30', 'nothing'),
    ('2018/11/02 16:59:00', 'nothing'),
    ('2018/11/03 11:29:00', 'nothing'),
    ('2018/11/10 00:47:30', 'nothing'),
    ('2018/11/10 04:58:00', 'nothing'),

    # 03 iteracia - SVM, 4 mesiace, 2;3
    ('2018/10/07 15:55:30', 'nothing'),
    ('2018/10/14 10:57:00', 'nothing'),
    ('2018/10/15 15:59:30', 'nothing'),
    ('2018/10/16 14:27:00', 'nothing'),
    ('2018/10/16 18:59:00', 'nothing'),
    ('2018/11/10 23:14:00', 'nothing'),
    ('2018/11/15 17:20:30', 'nothing'),
    ('2018/11/17 15:17:30', 'nothing'),
    ('2018/11/18 13:32:30', 'nothing'),
    ('2018/11/18 18:25:30', 'nothing'),

    # 04 iteracia - SVM, 4 mesiace, 2;3
    ('2018/10/08 19:14:00', 'nothing'),
    ('2018/10/14 14:58:30', 'nothing'),
    ('2018/10/18 22:27:30', 'nothing'),
    ('2018/10/22 16:39:30', 'nothing'),
    ('2018/11/02 12:36:30', 'nothing'),
    ('2018/11/09 23:03:00', 'nothing'),
    ('2018/11/10 03:07:30', 'nothing'),
    ('2018/11/15 21:43:30', 'nothing'),
    ('2018/11/20 19:40:00', 'nothing'),
    ('2018/12/01 17:57:30', 'nothing'),

    # 05 iteracia - SVM, 4 mesiace, 2;3
    ('2018/10/13 08:07:30', 'nothing'),
    ('2018/10/19 09:31:00', 'nothing'),
    ('2018/11/04 08:13:30', 'nothing'),
    ('2018/11/04 08:17:30', 'nothing'),
    ('2018/11/06 09:29:00', 'nothing'),
    ('2018/11/11 00:56:30', 'nothing'),
    ('2018/11/16 11:53:30', 'nothing'),
    ('2018/11/18 07:44:00', 'nothing'),
    ('2018/11/30 11:01:30', 'nothing'),
    ('2018/12/07 23:17:30', 'nothing'),

    # 06 iteracia - SVM, 4 mesiace, 2;3
    ('2018/10/15 13:20:00', 'nothing'),
    ('2018/10/21 19:48:00', 'nothing'),
    ('2018/10/22 12:33:30', 'nothing'),
    ('2018/11/09 23:02:30', 'nothing'),
    ('2018/11/10 02:13:30', 'nothing'),
    ('2018/11/10 02:29:30', 'nothing'),
    ('2018/11/11 01:07:00', 'nothing'),
    ('2019/01/15 15:11:00', 'nothing'),
    ('2018/11/10 23:14:30', 'nothing'),
    ('2018/11/10 23:15:00', 'nothing'),

    # 07 iteracia - SVM, 4 mesiace, 2;3
    ('2018/10/22 16:39:30', 'nothing'),
    ('2018/10/25 18:01:00', 'nothing'),
    ('2018/10/25 18:03:30', 'nothing'),
    ('2018/10/31 07:18:00', 'nothing'),
    ('2018/11/10 02:31:00', 'nothing'),
    ('2018/11/10 03:10:30', 'nothing'),
    ('2018/11/10 23:16:00', 'nothing'),
    ('2018/11/30 18:37:00', 'nothing'),
    ('2019/01/07 13:53:30', 'nothing'),

    # 08 iteracia - SVM, 4 mesiace, 2;3
    ('2018/10/31 07:16:30', 'nothing'),
    ('2019/01/18 09:59:00', 'nothing'),

    # 09 iteracia - SVM, 4 mesiace, 2;3
    ('2018/10/24 03:21:00', 'nothing'),
    ('2018/10/24 03:21:30', 'nothing'),
    ('2018/10/31 07:17:00', 'nothing'),
    ('2018/11/09 23:06:30', 'nothing'),
    ('2018/11/10 06:38:00', 'nothing'),
    ('2018/11/11 01:07:30', 'nothing'),
    ('2018/11/11 01:08:00', 'nothing'),
    ('2019/01/15 15:10:00', 'nothing'),
    ('2019/01/28 04:28:00', 'nothing'),

    # 10 iteracia - DTree, 4 mesiace, 2;3
    ('2018/10/07 12:13:30', 'nothing'),
    ('2018/10/07 19:30:30', 'nothing'),
    ('2018/10/08 01:00:30', 'nothing'),
    ('2018/10/08 12:33:30', 'nothing'),
    ('2018/10/08 23:19:30', 'nothing'),
    ('2018/10/09 10:51:00', 'nothing'),
    ('2018/10/10 12:18:00', 'nothing'),
    ('2018/10/11 11:02:00', 'nothing'),
    ('2018/10/11 20:05:30', 'nothing'),
    ('2018/10/13 11:05:30', 'nothing'),

    # 11 iteracia - DTree, 4 mesiace, 2;3
    ('2018/10/08 00:02:00', 'nothing'),
    ('2018/10/08 11:56:30', 'nothing'),
    ('2018/10/10 23:12:30', 'nothing'),
    ('2018/10/12 00:58:00', 'nothing'),
    ('2018/10/13 16:12:30', 'nothing'),
    ('2018/10/14 00:10:00', 'nothing'),
    ('2018/10/14 13:01:30', 'nothing'),
    ('2018/10/14 17:25:30', 'nothing'),
    ('2018/10/15 00:24:30', 'nothing'),
    ('2018/10/15 13:20:30', 'nothing'),

    # 12 iteracia - DTree, 4 mesiace, 2;3
    ('2018/10/07 13:39:30', 'nothing'),
    ('2018/10/11 13:47:00', 'nothing'),
    ('2018/10/14 12:47:00', 'nothing'),
    ('2018/10/14 22:49:00', 'nothing'),
    ('2018/10/26 10:47:00', 'nothing'),
    ('2018/11/05 21:38:00', 'nothing'),
    ('2018/11/24 00:08:30', 'nothing'),
    ('2018/12/12 18:21:00', 'nothing'),
    ('2019/01/11 23:00:00', 'nothing'),
    ('2019/01/23 00:17:30', 'nothing'),

    # 13 iteracia - DTree, 4 mesiace, 2;3
    ('2018/10/08 01:26:00', 'nothing'),
    ('2018/10/11 13:48:30', 'nothing'),
    ('2018/10/11 19:05:00', 'nothing'),
    ('2018/10/14 22:54:30', 'nothing'),
    ('2018/10/15 16:19:00', 'nothing'),
    ('2018/10/16 07:00:30', 'nothing'),
    ('2018/10/17 12:36:00', 'nothing'),
    ('2018/10/30 18:21:30', 'nothing'),
    ('2018/11/11 02:31:30', 'nothing'),
    ('2018/11/26 00:15:30', 'nothing'),

    # 14 iteracia - DTree, 4 mesiace, 2;3
    ('2018/10/08 02:17:30', 'nothing'),
    ('2018/10/10 22:58:00', 'nothing'),
    ('2018/10/14 01:32:00', 'nothing'),
    ('2018/10/15 07:30:30', 'nothing'),
    ('2018/10/24 01:16:00', 'nothing'),
    ('2018/10/27 23:09:30', 'nothing'),
    ('2018/10/31 00:13:00', 'nothing'),
    ('2018/11/04 09:45:00', 'nothing'),
    ('2018/11/11 23:22:00', 'nothing'),
    ('2018/11/24 05:51:30', 'nothing'),

    # 15 iteracia - DTree, 4 mesiace, 2;3
    ('2018/10/07 11:35:30', 'nothing'),
    ('2018/10/07 23:51:30', 'nothing'),
    ('2018/10/13 11:10:00', 'nothing'),
    ('2018/10/14 12:52:30', 'nothing'),
    ('2018/10/15 13:53:30', 'nothing'),
    ('2018/10/15 21:55:30', 'nothing'),
    ('2018/10/16 18:57:00', 'nothing'),
    ('2018/10/16 23:01:30', 'nothing'),
    ('2018/10/17 10:54:00', 'nothing'),
    ('2018/10/27 16:33:30', 'nothing'),

    # 16 iteracia - DTree, 4 mesiace, 2;3
    ('2018/10/10 20:46:00', 'nothing'),
    ('2018/10/14 09:08:30', 'nothing'),
    ('2018/10/16 09:09:30', 'nothing'),
    ('2018/10/27 21:47:00', 'nothing'),
    ('2018/11/11 04:29:00', 'nothing'),
    ('2018/11/24 18:32:30', 'nothing'),
    ('2019/01/23 13:25:00', 'nothing'),
    ('2019/01/13 07:35:30', 'nothing'),
    ('2018/12/02 18:58:30', 'nothing'),
    ('2018/11/26 17:04:30', 'nothing'),

    # 17 iteracia - DTree, 4 mesiace, 2;3
    ('2018/10/10 22:16:30', 'nothing'),
    ('2018/10/11 14:03:30', 'nothing'),
    ('2018/10/16 09:10:00', 'nothing'),
    ('2018/10/24 07:36:30', 'nothing'),
    ('2018/11/06 23:10:00', 'nothing'),
    ('2018/11/07 15:35:00', 'nothing'),
    ('2018/11/07 20:42:30', 'nothing'),
    ('2018/12/08 08:09:00', 'nothing'),
    ('2018/12/19 10:33:30', 'nothing'),
    ('2019/01/12 13:55:30', 'nothing'),

    # 18 iteracia - DTree, 4 mesiace, 2;3
    ('2018/10/10 10:06:30', 'nothing'),
    ('2018/10/14 15:00:00', 'nothing'),
    ('2018/11/03 16:29:00', 'nothing'),
    ('2018/11/06 14:18:30', 'nothing'),
    ('2018/11/18 17:04:00', 'nothing'),
    ('2018/12/07 19:19:00', 'nothing'),
    ('2018/12/09 07:59:00', 'nothing'),
    ('2019/01/10 00:40:00', 'nothing'),
    ('2019/01/16 00:23:30', 'nothing'),
    ('2019/01/24 09:32:00', 'nothing'),

    # 19 iteracia - DTree, 4 mesiace, 2;3
    ('2018/10/21 19:47:00', 'nothing'),
    ('2018/10/29 14:23:30', 'nothing'),
    ('2018/12/19 11:16:00', 'nothing'),

    # 20 iteracia - DTree, 4 mesiace, 2;3
    ('2018/10/10 22:16:00', 'nothing'),
    ('2018/10/16 14:26:30', 'nothing'),
    ('2019/01/12 13:55:00', 'nothing'),

    # 21 iteracia - DTree, 4 mesiace, 2;3
    ('2018/10/09 22:48:00', 'nothing'),
    ('2018/10/10 19:47:30', 'nothing'),
    ('2018/10/15 01:03:30', 'nothing'),
    ('2018/10/23 00:54:00', 'nothing'),
    ('2018/10/24 05:32:00', 'nothing'),
    ('2018/11/05 20:21:30', 'nothing'),
    ('2018/11/07 23:29:30', 'nothing'),
    ('2018/11/10 23:13:00', 'nothing'),
    ('2018/11/13 20:45:30', 'nothing'),
    ('2018/11/24 00:20:30', 'nothing'),

    # 22 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/07 07:51:30', 'nothing'),
    ('2018/10/07 18:29:00', 'nothing'),
    ('2018/10/07 22:47:00', 'nothing'),
    ('2018/10/08 01:27:30', 'nothing'),
    ('2018/10/08 20:12:00', 'nothing'),
    ('2018/10/09 18:10:00', 'nothing'),
    ('2018/10/11 22:26:00', 'nothing'),
    ('2018/10/13 01:01:00', 'nothing'),
    ('2018/10/13 13:32:30', 'nothing'),
    ('2018/10/14 11:43:00', 'nothing'),

    # 23 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/07 13:15:00', 'nothing'),
    ('2018/10/11 11:13:30', 'nothing'),
    ('2018/10/13 18:54:00', 'nothing'),
    ('2018/10/14 22:49:30', 'nothing'),
    ('2018/10/17 00:29:00', 'nothing'),
    ('2018/10/19 15:26:30', 'nothing'),
    ('2018/10/23 10:02:30', 'nothing'),
    ('2018/10/29 09:34:30', 'nothing'),
    ('2018/11/03 02:22:30', 'nothing'),
    ('2018/11/09 16:44:00', 'nothing'),

    # 24 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/07 17:05:30', 'nothing'),
    ('2018/10/09 18:12:00', 'nothing'),
    ('2018/10/10 09:49:00', 'nothing'),
    ('2018/10/13 14:14:30', 'nothing'),
    ('2018/10/15 23:58:00', 'nothing'),
    ('2018/11/02 09:49:00', 'nothing'),
    ('2018/11/06 07:40:00', 'nothing'),
    ('2018/11/10 06:06:30', 'nothing'),
    ('2018/11/11 02:42:30', 'nothing'),
    ('2018/11/16 02:37:30', 'nothing'),

    # 25 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/07 16:54:00', 'nothing'),
    ('2018/10/09 14:08:30', 'nothing'),
    ('2018/10/11 08:16:00', 'nothing'),
    ('2018/10/12 00:24:00', 'nothing'),
    ('2018/10/13 12:19:00', 'nothing'),
    ('2018/10/15 23:55:00', 'nothing'),
    ('2018/10/17 07:54:00', 'nothing'),
    ('2018/10/19 17:25:30', 'nothing'),
    ('2018/10/21 10:23:00', 'nothing'),
    ('2018/10/23 00:56:00', 'nothing'),

    # 26 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/07 16:08:00', 'nothing'),
    ('2018/10/10 10:55:00', 'nothing'),
    ('2018/10/12 08:36:00', 'nothing'),
    ('2018/10/15 07:33:00', 'nothing'),
    ('2018/10/18 18:29:00', 'nothing'),
    ('2018/10/28 13:32:30', 'nothing'),
    ('2018/10/31 10:57:00', 'nothing'),
    ('2018/11/06 20:59:30', 'nothing'),
    ('2018/11/10 05:09:00', 'nothing'),
    ('2018/11/15 10:42:30', 'nothing'),

    # 27 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/09 10:28:00', 'nothing'),
    ('2018/10/10 13:08:30', 'nothing'),
    ('2018/10/11 09:46:00', 'nothing'),
    ('2018/10/13 11:49:30', 'nothing'),
    ('2018/10/16 18:30:30', 'nothing'),
    ('2018/10/19 10:46:30', 'nothing'),
    ('2018/10/22 08:28:30', 'nothing'),
    ('2018/10/25 18:02:30', 'nothing'),
    ('2018/10/31 08:11:30', 'nothing'),
    ('2018/11/04 00:17:30', 'nothing'),

    # 28 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/07 19:04:30', 'nothing'),
    ('2018/10/09 10:52:00', 'nothing'),
    ('2018/10/11 12:44:30', 'nothing'),
    ('2018/10/16 14:54:00', 'nothing'),
    ('2018/10/24 23:17:00', 'nothing'),
    ('2018/10/31 17:00:30', 'nothing'),
    ('2018/11/07 16:15:30', 'nothing'),
    ('2018/11/11 00:55:00', 'nothing'),
    ('2018/11/17 11:48:00', 'nothing'),
    ('2018/11/28 09:53:00', 'nothing'),

    # 29 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/08 01:26:30', 'nothing'),
    ('2018/10/09 14:45:00', 'nothing'),
    ('2018/10/10 20:45:30', 'nothing'),
    ('2018/10/12 08:52:30', 'nothing'),
    ('2018/10/15 11:06:00', 'nothing'),
    ('2018/10/15 18:53:00', 'nothing'),
    ('2018/10/17 16:08:30', 'nothing'),
    ('2018/10/23 23:54:30', 'nothing'),
    ('2018/10/30 09:56:30', 'nothing'),
    ('2018/11/05 20:02:00', 'nothing'),

    # 30 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/07 17:50:00', 'nothing'),
    ('2018/10/11 07:58:30', 'nothing'),
    ('2018/10/11 12:16:00', 'nothing'),
    ('2018/10/14 07:45:00', 'nothing'),
    ('2018/10/15 23:58:30', 'nothing'),
    ('2018/10/16 07:42:00', 'nothing'),
    ('2018/10/21 03:57:00', 'nothing'),
    ('2018/10/22 12:41:30', 'nothing'),
    ('2018/10/26 17:33:30', 'nothing'),
    ('2018/10/30 16:34:00', 'nothing'),

    # 31 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/09 08:57:00', 'nothing'),
    ('2018/10/10 18:44:30', 'nothing'),
    ('2018/10/11 10:46:30', 'nothing'),
    ('2018/10/14 10:25:00', 'nothing'),
    ('2018/10/16 09:03:30', 'nothing'),
    ('2018/10/18 20:06:30', 'nothing'),
    ('2018/10/24 01:30:00', 'nothing'),
    ('2018/10/28 15:39:00', 'nothing'),
    ('2018/10/30 20:02:30', 'nothing'),
    ('2018/11/02 20:30:30', 'nothing'),

    # 32 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/07 18:36:00', 'nothing'),
    ('2018/10/10 10:59:00', 'nothing'),
    ('2018/10/11 08:29:00', 'nothing'),
    ('2018/10/11 17:31:30', 'nothing'),
    ('2018/10/14 11:15:30', 'nothing'),
    ('2018/10/16 17:16:00', 'nothing'),
    ('2018/10/21 11:11:00', 'nothing'),
    ('2018/10/22 13:53:30', 'nothing'),
    ('2018/10/27 21:04:00', 'nothing'),
    ('2018/10/31 10:02:00', 'nothing'),

    # 33 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/09 10:29:30', 'nothing'),
    ('2018/10/11 08:55:30', 'nothing'),
    ('2018/10/13 07:56:30', 'nothing'),
    ('2018/10/13 14:08:30', 'nothing'),
    ('2018/10/15 08:20:30', 'nothing'),
    ('2018/10/15 14:17:30', 'nothing'),
    ('2018/10/16 09:58:00', 'nothing'),
    ('2018/10/20 10:23:30', 'nothing'),
    ('2018/10/21 10:56:30', 'nothing'),
    ('2018/10/23 10:58:30', 'nothing'),

    # 34 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/07 16:07:30', 'nothing'),
    ('2018/10/11 01:32:30', 'nothing'),
    ('2018/10/13 18:52:30', 'nothing'),
    ('2018/10/15 14:26:00', 'nothing'),
    ('2018/10/20 11:15:30', 'nothing'),
    ('2018/10/30 18:04:00', 'nothing'),
    ('2018/11/06 22:47:30', 'nothing'),
    ('2018/11/09 22:23:30', 'nothing'),
    ('2018/11/10 02:51:00', 'nothing'),
    ('2018/11/13 08:00:30', 'nothing'),

    # 35 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/10 11:30:30', 'nothing'),
    ('2018/10/14 10:26:00', 'nothing'),
    ('2018/10/19 17:08:00', 'nothing'),
    ('2018/11/07 09:18:30', 'nothing'),
    ('2018/11/19 11:33:30', 'nothing'),
    ('2018/11/24 06:53:30', 'nothing'),
    ('2018/11/30 16:48:00', 'nothing'),
    ('2018/12/25 04:58:30', 'nothing'),
    ('2018/12/25 23:47:30', 'nothing'),
    ('2019/01/25 07:02:30', 'nothing'),

    # 36 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/08 20:11:00', 'nothing'),
    ('2018/10/09 10:20:30', 'nothing'),
    ('2018/10/15 11:25:30', 'nothing'),
    ('2018/10/20 14:55:30', 'nothing'),
    ('2018/10/22 07:57:00', 'nothing'),
    ('2018/10/28 15:40:30', 'nothing'),
    ('2018/10/29 09:29:00', 'nothing'),
    ('2018/11/04 00:16:00', 'nothing'),
    ('2018/11/06 14:49:30', 'nothing'),
    ('2018/11/07 05:37:00', 'nothing'),

    # 37 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/09 20:51:00', 'nothing'),
    ('2018/10/10 20:02:30', 'nothing'),
    ('2018/10/11 09:44:30', 'nothing'),
    ('2018/10/12 08:35:00', 'nothing'),
    ('2018/10/13 13:50:30', 'nothing'),
    ('2018/10/14 16:14:30', 'nothing'),
    ('2018/10/15 11:09:00', 'nothing'),
    ('2018/10/16 08:57:00', 'nothing'),
    ('2018/10/20 09:30:00', 'nothing'),
    ('2018/10/23 08:30:00', 'nothing'),

    # 38 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/08 19:04:00', 'nothing'),
    ('2018/10/11 09:45:30', 'nothing'),
    ('2018/10/12 00:25:00', 'nothing'),
    ('2018/10/13 10:51:00', 'nothing'),
    ('2018/10/14 14:33:30', 'nothing'),
    ('2018/10/15 18:52:00', 'nothing'),
    ('2018/10/20 10:55:00', 'nothing'),
    ('2018/10/23 10:56:30', 'nothing'),
    ('2018/10/26 15:19:00', 'nothing'),
    ('2018/10/28 19:41:30', 'nothing'),

    # 39 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/09 09:06:30', 'nothing'),
    ('2018/10/10 23:26:00', 'nothing'),
    ('2018/10/15 11:09:30', 'nothing'),
    ('2018/10/16 07:44:30', 'nothing'),
    ('2018/10/17 15:37:00', 'nothing'),
    ('2018/10/19 07:59:30', 'nothing'),
    ('2018/10/20 12:14:30', 'nothing'),
    ('2018/10/24 06:32:30', 'nothing'),
    ('2018/10/24 21:53:00', 'nothing'),
    ('2018/10/26 07:27:00', 'nothing'),

    # 40 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/07 16:54:30', 'nothing'),
    ('2018/10/08 23:02:00', 'nothing'),
    ('2018/10/09 10:29:00', 'nothing'),
    ('2018/10/09 18:08:30', 'nothing'),
    ('2018/10/10 00:11:30', 'nothing'),
    ('2019/01/28 19:39:00', 'nothing'),
    ('2019/01/28 08:12:30', 'nothing'),
    ('2019/01/27 18:26:30', 'nothing'),
    ('2019/01/26 10:02:30', 'nothing'),
    ('2019/01/24 17:40:00', 'nothing'),

    # 41 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/09 08:22:30', 'nothing'),
    ('2018/10/09 14:28:00', 'nothing'),
    ('2018/10/16 00:01:30', 'nothing'),
    ('2018/10/21 19:48:30', 'nothing'),
    ('2018/10/22 11:05:30', 'nothing'),
    ('2018/10/28 13:31:00', 'nothing'),
    ('2018/11/10 00:31:00', 'nothing'),
    ('2018/11/13 20:02:00', 'nothing'),
    ('2018/11/24 06:47:00', 'nothing'),
    ('2018/11/24 09:21:30', 'nothing'),

    # 42 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/10 23:34:30', 'nothing'),
    ('2018/10/13 10:23:30', 'nothing'),
    ('2018/10/16 00:26:30', 'nothing'),
    ('2018/10/18 09:12:00', 'nothing'),
    ('2018/10/22 11:06:00', 'nothing'),
    ('2018/10/27 21:02:30', 'nothing'),
    ('2018/11/03 09:36:30', 'nothing'),
    ('2018/11/18 09:54:00', 'nothing'),
    ('2018/12/04 09:24:00', 'nothing'),
    ('2018/12/07 23:20:00', 'nothing'),

    # 43 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/09 08:52:30', 'nothing'),
    ('2018/10/11 10:50:00', 'nothing'),
    ('2018/10/11 16:34:30', 'nothing'),
    ('2018/10/12 00:15:30', 'nothing'),
    ('2018/10/17 10:12:30', 'nothing'),
    ('2018/10/23 07:57:00', 'nothing'),
    ('2018/11/01 18:54:30', 'nothing'),
    ('2018/11/10 18:18:00', 'nothing'),
    ('2018/11/11 01:06:30', 'nothing'),
    ('2018/11/21 02:18:00', 'nothing'),

    # 44 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/09 08:19:00', 'nothing'),
    ('2018/10/15 00:27:00', 'nothing'),
    ('2018/10/18 09:14:30', 'nothing'),
    ('2018/10/27 20:51:30', 'nothing'),
    ('2018/11/09 23:26:00', 'nothing'),
    ('2018/11/10 23:25:00', 'nothing'),
    ('2018/11/24 07:34:00', 'nothing'),
    ('2018/11/30 22:43:00', 'nothing'),
    ('2018/12/14 08:40:00', 'nothing'),
    ('2019/01/08 14:41:30', 'nothing'),

    # 45 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/10 00:10:00', 'nothing'),
    ('2018/10/15 10:43:00', 'nothing'),
    ('2018/10/18 20:07:00', 'nothing'),
    ('2018/10/26 17:06:30', 'nothing'),
    ('2018/11/09 23:01:30', 'nothing'),
    ('2018/11/10 04:02:30', 'nothing'),
    ('2018/11/10 23:13:30', 'nothing'),
    ('2018/11/24 06:52:30', 'nothing'),
    ('2018/11/30 11:15:00', 'nothing'),
    ('2019/01/14 23:58:00', 'nothing'),

    # 46 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/07 17:39:30', 'nothing'),
    ('2018/10/09 15:08:30', 'nothing'),
    ('2018/10/14 08:17:00', 'nothing'),
    ('2018/10/21 10:56:00', 'nothing'),
    ('2018/10/30 18:22:00', 'nothing'),
    ('2018/11/02 13:52:30', 'nothing'),
    ('2018/11/07 18:15:30', 'nothing'),
    ('2018/11/10 00:30:30', 'nothing'),
    ('2018/12/02 19:10:00', 'nothing'),
    ('2018/12/03 23:19:00', 'nothing'),

    # 47 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/09 10:55:00', 'nothing'),
    ('2018/10/10 22:28:30', 'nothing'),
    ('2018/10/14 14:19:00', 'nothing'),
    ('2018/10/16 07:14:30', 'nothing'),
    ('2018/10/16 16:50:00', 'nothing'),
    ('2018/11/02 15:33:30', 'nothing'),
    ('2018/11/02 17:37:00', 'nothing'),
    ('2018/11/02 20:22:00', 'nothing'),
    ('2018/11/03 16:41:30', 'nothing'),
    ('2018/11/04 12:17:30', 'nothing'),

    # 48 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/07 11:42:30', 'nothing'),
    ('2018/10/11 09:23:30', 'nothing'),
    ('2018/10/14 17:53:00', 'nothing'),
    ('2018/10/15 18:52:30', 'nothing'),
    ('2018/10/20 10:27:00', 'nothing'),
    ('2018/11/08 00:52:00', 'nothing'),
    ('2018/11/10 02:29:00', 'nothing'),
    ('2018/11/13 17:04:00', 'nothing'),
    ('2018/11/21 22:29:00', 'nothing'),
    ('2018/12/06 14:19:30', 'nothing'),

    # 49 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/09 08:22:00', 'nothing'),
    ('2018/10/13 00:41:30', 'nothing'),
    ('2018/10/15 14:18:00', 'nothing'),
    ('2018/10/16 08:54:00', 'nothing'),
    ('2018/11/10 06:05:30', 'nothing'),
    ('2018/11/10 18:06:00', 'nothing'),
    ('2018/11/10 18:12:00', 'nothing'),
    ('2018/12/01 21:11:00', 'nothing'),
    ('2018/12/06 12:30:00', 'nothing'),
    ('2018/12/14 00:28:30', 'nothing'),

    # 50 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/14 10:14:30', 'nothing'),
    ('2018/10/15 09:36:00', 'nothing'),
    ('2018/10/31 07:17:30', 'nothing'),
    ('2018/11/06 21:13:00', 'nothing'),
    ('2018/11/10 00:29:30', 'nothing'),
    ('2018/11/10 02:36:00', 'nothing'),
    ('2018/11/24 09:20:30', 'nothing'),
    ('2019/01/22 08:52:00', 'nothing'),
    ('2019/01/23 01:36:30', 'nothing'),
    ('2019/01/28 04:39:00', 'nothing'),

    # 51 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/09 08:58:30', 'nothing'),
    ('2018/10/09 16:49:30', 'nothing'),
    ('2018/10/10 23:24:30', 'nothing'),
    ('2018/10/13 10:18:30', 'nothing'),
    ('2018/10/14 09:02:30', 'nothing'),
    ('2018/10/16 18:31:00', 'nothing'),
    ('2018/10/17 11:15:00', 'nothing'),
    ('2018/10/21 11:02:00', 'nothing'),
    ('2018/10/27 09:00:00', 'nothing'),
    ('2018/10/27 23:22:30', 'nothing'),

    # 52 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/10 11:34:30', 'nothing'),
    ('2018/10/16 08:14:00', 'nothing'),
    ('2018/10/15 22:24:00', 'nothing'),
    ('2018/10/16 21:28:30', 'nothing'),
    ('2018/10/17 11:31:00', 'nothing'),
    ('2018/11/10 01:52:30', 'nothing'),
    ('2018/11/10 02:38:00', 'nothing'),
    ('2018/11/13 13:03:00', 'nothing'),
    ('2018/12/03 09:29:30', 'nothing'),
    ('2018/12/27 02:35:30', 'nothing'),

    # 53 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/11 11:30:30', 'nothing'),
    ('2018/10/14 11:19:30', 'nothing'),
    ('2018/10/21 19:46:30', 'nothing'),
    ('2018/10/23 13:43:30', 'nothing'),
    ('2018/11/10 04:03:00', 'nothing'),
    ('2018/11/10 18:05:30', 'nothing'),
    ('2018/11/17 10:03:30', 'nothing'),
    ('2018/11/17 15:32:30', 'nothing'),
    ('2018/11/24 09:23:00', 'nothing'),
    ('2018/12/19 17:06:30', 'nothing'),

    # 54 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/11 10:10:30', 'nothing'),
    ('2018/10/13 10:20:00', 'nothing'),
    ('2018/10/15 23:50:30', 'nothing'),
    ('2018/10/16 08:15:30', 'nothing'),
    ('2018/10/18 18:17:30', 'nothing'),
    ('2018/11/07 06:59:30', 'nothing'),
    ('2018/11/09 16:43:30', 'nothing'),
    ('2018/11/09 23:49:30', 'nothing'),
    ('2018/11/10 03:30:00', 'nothing'),
    ('2018/11/10 18:04:30', 'nothing'),

    # 55 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/11 16:40:00', 'nothing'),
    ('2018/10/13 10:46:30', 'nothing'),
    ('2018/11/02 20:28:30', 'nothing'),
    ('2018/11/06 09:37:30', 'nothing'),
    ('2018/11/09 23:02:00', 'nothing'),
    ('2018/11/10 00:31:30', 'nothing'),
    ('2018/11/10 01:34:30', 'nothing'),
    ('2018/11/24 06:34:30', 'nothing'),
    ('2018/11/24 06:45:30', 'nothing'),
    ('2019/01/15 07:15:30', 'nothing'),

    # 56 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/22 11:47:30', 'nothing'),
    ('2018/10/28 21:07:30', 'nothing'),
    ('2018/11/09 23:27:00', 'nothing'),
    ('2018/11/10 03:40:30', 'nothing'),
    ('2018/11/11 01:32:30', 'nothing'),
    ('2019/01/26 08:29:30', 'nothing'),
    ('2019/01/26 05:07:00', 'nothing'),
    ('2019/01/21 23:30:00', 'nothing'),
    ('2018/12/30 09:35:30', 'nothing'),
    ('2018/12/14 11:04:00', 'nothing'),

    # 57 iteracia - Deep, 4 mesiace, 2;3
    ('2018/11/05 18:14:00', 'nothing'),
    ('2018/11/08 19:14:30', 'nothing'),
    ('2018/11/21 08:02:30', 'nothing'),
    ('2018/11/21 08:13:00', 'nothing'),
    ('2018/11/24 18:38:30', 'nothing'),
    ('2018/12/01 20:47:00', 'nothing'),
    ('2018/12/07 23:17:00', 'nothing'),
    ('2019/01/11 15:30:30', 'nothing'),

    # 58 iteracia - Deep, 4 mesiace, 2;3
    ('2018/10/10 23:24:00', 'nothing'),
    ('2018/10/11 00:58:00', 'nothing'),
    ('2018/10/17 11:16:00', 'nothing'),
    ('2018/10/26 15:17:00', 'nothing'),
    ('2018/11/09 07:17:00', 'nothing'),
    ('2018/11/10 02:57:30', 'nothing'),
    ('2018/11/13 20:48:30', 'nothing'),
    ('2018/11/17 10:03:00', 'nothing'),
    ('2018/11/18 09:56:30', 'nothing'),
    ('2018/11/20 10:45:30', 'nothing'),

    # 59 iteracia - , 4 mesiace, 2;3
    ('2018/10/10 21:50:00', 'nothing'),
    ('2018/10/10 23:00:00', 'nothing'),
    ('2018/11/15 21:43:00', 'nothing'),
    ('2018/11/22 17:54:30', 'nothing'),
    ('2018/11/24 18:41:00', 'nothing'),

    # 60 iteracia - , 4 mesiace, 2;3
    ('2018/10/10 21:50:00', 'nothing'),
    ('2018/10/10 23:00:00', 'nothing'),
    ('2018/11/15 21:43:00', 'nothing'),
    ('2018/11/22 17:54:30', 'nothing'),
    ('2018/11/24 18:41:00', 'nothing'),
]


def simple_f(value, timestamp):
    return value


def func(con, table_name, timestamp, row_selector, interval_selector):
    attrs = []
    columns = [
        'co2_in_ppm',
        'temperature_in_celsius',
        'rh_in_specific_g_kg',
        'rh_out_specific_g_kg',
    ]
    precision = 2

    for column in columns:
        for normalize in [False]:
            intervals_before = [x for x in range(20, 901, 20)]
            intervals_after = [x for x in range(15, 181, 15)]

            #
            # linearny posun DifferenceA
            op = FirstDifferenceAttrA(con, table_name, row_selector, interval_selector, simple_f)
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
            op = FirstDifferenceAttrB(con, table_name, row_selector, interval_selector, simple_f)
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

            op = DifferenceBetweenRealLinear(con, table_name, row_selector, interval_selector, simple_f)
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
            op = FirstDifferenceAttrB(con, table_name, row_selector, interval_selector, simple_f)
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
            op = FirstDifferenceAttrB(con, table_name, row_selector, interval_selector, simple_f)
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
            op = GrowthRate(con, table_name, row_selector, interval_selector, simple_f)
            b, a = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=[x for x in range(5, 901, 15)],
                              intervals_after=[x for x in range(5, 181, 15)],
                              value_delay=15, prefix='_step20')
            attrs += b + a
            be, af = op.arithmetic_mean(column, precision, b, a, 'G_linear_step_15')
            attrs += be + af

            # GrowRate - linearne
            op = GrowthRate(con, table_name, row_selector, interval_selector, simple_f)
            b, a = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=[x for x in range(5, 901, 30)],
                              intervals_after=[x for x in range(5, 181, 30)],
                              value_delay=30, prefix='_step_30')
            attrs += b + a
            be, af = op.arithmetic_mean(column, precision, b, a, 'G_linear_step_30')
            attrs += be + af

            # GrowRate - x^2
            op = GrowthRate(con, table_name, row_selector, interval_selector, simple_f)
            b, a = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=[x * x for x in range(2, 31, 1)],
                              intervals_after=[x * x for x in range(2, 14, 1)],
                              value_delay=30, prefix='_x2')
            attrs += b + a
            be, af = op.arithmetic_mean(column, precision, b, a, 'Grow_x2')
            attrs += be + af

            # GrowRate - x^3
            op = GrowthRate(con, table_name, row_selector, interval_selector, simple_f)
            b, a = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=[x * x * x for x in range(2, 10, 1)],
                              intervals_after=[x * x * x for x in range(2, 6, 1)],
                              value_delay=30, prefix='_x3')
            attrs += b + a
            be, af = op.arithmetic_mean(column, precision, b, a, 'Grow_x3')
            attrs += be + af

        op = InOutDiff(con, table_name, row_selector, interval_selector, simple_f)
        b, a = op.execute(timestamp=timestamp, column='co2_in_ppm_diff', precision=precision,
                          intervals_before=[1],
                          intervals_after=[],
                          prefix='')
        attrs += b + a

        # diff T + H in/out
        op = InOutDiff(con, table_name, row_selector, interval_selector, simple_f)
        b, a = op.execute(timestamp=timestamp, column='temperature_in_celsius_diff', precision=precision,
                          intervals_before=[1],
                          intervals_after=[],
                          prefix='')
        attrs += b + a

        op = InOutDiff(con, table_name, row_selector, interval_selector, simple_f)
        b, a = op.execute(timestamp=timestamp, column='rh_in_percentage_diff', precision=precision,
                          intervals_before=[1],
                          intervals_after=[],
                          prefix='')
        attrs += b + a

        op = InOutDiff(con, table_name, row_selector, interval_selector, simple_f)
        b, a = op.execute(timestamp=timestamp, column='rh_in_specific_g_kg_diff', precision=precision,
                          intervals_before=[1],
                          intervals_after=[],
                          prefix='')
        attrs += b + a

        op = InOutDiff(con, table_name, row_selector, interval_selector, simple_f)
        b, a = op.execute(timestamp=timestamp, column='rh_in_absolute_g_m3_diff', precision=precision,
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
    end = int(DateTimeUtil.local_time_str_to_utc('2019/04/29 18:00:00').timestamp())

    # Peto , februar, marec, april
    start = int(DateTimeUtil.local_time_str_to_utc('2019/02/04 18:00:00').timestamp())
    testing_set('measured_filtered_peto', start, end, '{0}/gt_peto.csv'.format(directory))

    # David
    start = int(DateTimeUtil.local_time_str_to_utc('2019/04/03 18:00:00').timestamp())
    testing_set('measured_david', start, end, '{0}/gt_david.csv'.format(directory))

    # Martin
    start = int(DateTimeUtil.local_time_str_to_utc('2019/04/01 18:00:00').timestamp())
    testing_set('measured_martin', start, end, '{0}/gt_martin.csv'.format(directory))

    # Klarka
    start = int(DateTimeUtil.local_time_str_to_utc('2018/12/18 18:00:00').timestamp())
    testing_set('measured_klarka', start, end, '{0}/gt_klarka.csv'.format(directory))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    # tabulka s CO2, ktora neprekroci hranicu 2000ppm
    table_name = 'measured_filtered_peto'

    directory = 'co2_t_h_out'
    if not os.path.isdir(directory):
        os.mkdir(directory)

    training_set('examples/events_peto.json', -500, table_name, directory)

    start = int(DateTimeUtil.local_time_str_to_utc('2018/10/07 06:00:00').timestamp())
    testing_set(table_name, start, start + 100, '{0}/testing.csv'.format(directory))

    # testing_month(table_name, start)
    # generic_testing(directory)
