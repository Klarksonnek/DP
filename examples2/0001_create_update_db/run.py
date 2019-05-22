""" Creates tables in database, updates or deletes records in tables.
"""
from os.path import dirname, abspath, join
import sys
sys.path.append(abspath(join(dirname(__file__), '../..', '')))

from dm.BeeeOnClient import BeeeOnClient
from dm.ConnectionUtil import ConnectionUtil
from dm.DBUtil import DBUtil
from dm.DateTimeUtil import DateTimeUtil
from dm.PreProcessing import PreProcessing
from dm.Storage import Storage
import json
import logging
import time

__author__ = ''
__email__ = ''


def delete_rows(con, timestamp_from, timestamp_to, table_name):
    table = table_name
    f = timestamp_from
    t = timestamp_to
    cur = con.cursor()

    cur.execute('UPDATE {0} SET pressure_in_hpa = Null WHERE measured_time >= {1} AND measured_time <= {2}'.format(table, f, t))
    cur.execute('UPDATE {0} SET temperature_in_celsius = Null WHERE measured_time >= {1} AND measured_time <= {2}'.format(table, f, t))
    cur.execute('UPDATE {0} SET temperature_in2_celsius = Null WHERE measured_time >= {1} AND measured_time <= {2}'.format(table, f, t))
    cur.execute('UPDATE {0} SET temperature_out_celsius = Null WHERE measured_time >= {1} AND measured_time <= {2}'.format(table, f, t))
    cur.execute('UPDATE {0} SET rh_in_percentage = Null WHERE measured_time >= {1} AND measured_time <= {2}'.format(table, f, t))
    cur.execute('UPDATE {0} SET rh_in2_percentage = Null WHERE measured_time >= {1} AND measured_time <= {2}'.format(table, f, t))
    cur.execute('UPDATE {0} SET rh_in_absolute_g_m3 = Null WHERE measured_time >= {1} AND measured_time <= {2}'.format(table, f, t))
    cur.execute('UPDATE {0} SET rh_in2_absolute_g_m3 = Null WHERE measured_time >= {1} AND measured_time <= {2}'.format(table, f, t))
    cur.execute('UPDATE {0} SET rh_in_specific_g_kg = Null WHERE measured_time >= {1} AND measured_time <= {2}'.format(table, f, t))
    cur.execute('UPDATE {0} SET rh_in2_specific_g_kg = Null WHERE measured_time >= {1} AND measured_time <= {2}'.format(table, f, t))
    cur.execute('UPDATE {0} SET rh_out_percentage = Null WHERE measured_time >= {1} AND measured_time <= {2}'.format(table, f, t))
    cur.execute('UPDATE {0} SET rh_out_absolute_g_m3 = Null WHERE measured_time >= {1} AND measured_time <= {2}'.format(table, f, t))
    cur.execute('UPDATE {0} SET rh_out_specific_g_kg = Null WHERE measured_time >= {1} AND measured_time <= {2}'.format(table, f, t))
    cur.execute('UPDATE {0} SET co2_in_ppm = Null WHERE measured_time >= {1} AND measured_time <= {2}'.format(table, f, t))

    con.commit()


def update_rows(con, table_name, attr_name, new_value, timestamp_from, timestamp_to):
    table = table_name
    f = timestamp_from
    t = timestamp_to
    cur = con.cursor()

    cur.execute('UPDATE {0} SET {1} = {2} WHERE measured_time >= {3} AND measured_time <= {4}'
                .format(table, attr_name, new_value, f, t))

    con.commit()


def update_invalid_values(con):
    cur = con.cursor()

    # Peto
    for table in ['measured_peto', 'measured_peto_reduced', 'measured_filtered_peto', 'measured_filtered_peto_reduced']:
        cur.execute('UPDATE ' + table + ' SET open_close = 1 WHERE measured_time = 1538920482')
        cur.execute('UPDATE ' + table + ' SET open_close = 0 WHERE measured_time >= 1539410852 AND measured_time <= 1539410865')
        cur.execute('UPDATE ' + table + ' SET open_close = 0 WHERE measured_time >= 1542011517 AND measured_time <= 1542011529')
        cur.execute('UPDATE ' + table + ' SET open_close = 0 WHERE measured_time >= 1551896814 AND measured_time <= 1551902894')
        cur.execute('UPDATE ' + table + ' SET open_close = 0 WHERE measured_time >= 1551890462 AND measured_time <= 1551890556')
        cur.execute('UPDATE ' + table + ' SET open_close = 0 WHERE measured_time >= 1540144019 AND measured_time <= 1540144924')
        cur.execute('UPDATE ' + table + ' SET open_close = 1 WHERE measured_time >= 1545208319 AND measured_time <= 1545208364')
        cur.execute('UPDATE ' + table + ' SET open_close = 0 WHERE measured_time >= 1547292105 AND measured_time <= 1547292149')
        cur.execute('UPDATE ' + table + ' SET open_close = 0 WHERE measured_time >= 1551339840 AND measured_time <= 1551339852')
        cur.execute('UPDATE ' + table + ' SET open_close = 1 WHERE measured_time >= 1554613585 AND measured_time <= 1554613592')

        update_rows(con, table, 'open_close', '0', 1548318471, 1548318474)
        update_rows(con, table, 'open_close', '0', 1544377548, 1544377695)
        update_rows(con, table, 'open_close', '0', 1549953360, 1549954342)
        update_rows(con, table, 'open_close', '1', 1551904261, 1551904268)
        update_rows(con, table, 'open_close', '1', 1538896688, 1538896691)
        update_rows(con, table, 'open_close', '1', 1548318470, 1548318475)
        update_rows(con, table, 'open_close', '0', 1544794909, 1544795005)

        delete_rows(con, 1551847133, 1551889587, table)
        delete_rows(con, 1551903872, 1551908262, table)
        delete_rows(con, 1540374284, 1540378270, table)
        delete_rows(con, 1538995201, 1539012743, table)
        delete_rows(con, 1540365694, 1540366698, table)
        delete_rows(con, 1541870939, 1541883662, table)
        delete_rows(con, 1543082767, 1543128959, table)
        delete_rows(con, 1540366406, 1540392145, table)
        delete_rows(con, 1541342801, 1541342997, table)
        delete_rows(con, 1541248034, 1541256678, table)
        delete_rows(con, 1541336415, 1541343035, table)
        delete_rows(con, 1541265886, 1541268330, table)
        delete_rows(con, 1547017612, 1547017804, table)
        delete_rows(con, 1547764885, 1547797834, table)
        delete_rows(con, 1549952386, 1549954380, table)

        delete_rows(con, 1538951188, 1538951527, table)
        delete_rows(con, 1542105369, 1542106204, table)
        delete_rows(con, 1543180780, 1543182998, table)
        delete_rows(con, 1544377532, 1544378399, table)
        delete_rows(con, 1544733452, 1544736700, table)
        delete_rows(con, 1546466972, 1546529446, table)
        delete_rows(con, 1546792707, 1546812008, table)
        delete_rows(con, 1548016983, 1548076447, table)
        delete_rows(con, 1548117828, 1548135492, table)
        delete_rows(con, 1548211577, 1548228314, table)
        delete_rows(con, 1548238685, 1548239010, table)
        delete_rows(con, 1548279855, 1548280843, table)
        delete_rows(con, 1548826585, 1548828602, table)
        delete_rows(con, 1547291955, 1547292307, table)
        delete_rows(con, 1554060946, 1554063977, table)
        delete_rows(con, 1539170291, 1539187647, table)
        delete_rows(con, 1539332345, 1539382163, table)
        delete_rows(con, 1542496507, 1542497157, table)
    con.commit()

    # Klarka
    for table in ['measured_klarka', 'measured_klarka_reduced']:
        cur.execute('UPDATE ' + table + ' SET open_close = 0 WHERE measured_time = 1547490233')
        cur.execute('UPDATE ' + table + ' SET open_close = 0 WHERE measured_time = 1547642276')

        update_rows(con, table, 'open_close', 0, 1543650667, 1543650670)
        update_rows(con, table, 'open_close', 0, 1543789966, 1543789968)
        update_rows(con, table, 'open_close', 1, 1544047968, 1544047971)
        update_rows(con, table, 'open_close', 0, 1547490233, 1547490236)
        update_rows(con, table, 'open_close', 1, 1548678892, 1548678904)
        update_rows(con, table, 'open_close', 0, 1548742218, 1548742221)
        update_rows(con, table, 'open_close', 0, 1544520898, 1544520901)
        update_rows(con, table, 'open_close', 0, 1547447766, 1547447768)
        update_rows(con, table, 'open_close', 0, 1552246992, 1552246995)
        update_rows(con, table, 'open_close', 1, 1552336762, 1552336765)
        update_rows(con, table, 'open_close', 1, 1556356758, 1556356761)

        delete_rows(con, 1543778231, 1543780663, table)
        delete_rows(con, 1543870389, 1543872050, table)
        delete_rows(con, 1543957520, 1543959601, table)
        delete_rows(con, 1543997375, 1543999203, table)
        delete_rows(con, 1544083221, 1544085985, table)
        delete_rows(con, 1544853244, 1544854638, table)
        delete_rows(con, 1544858207, 1544859522, table)
        delete_rows(con, 1544872040, 1544873665, table)
        delete_rows(con, 1545245340, 1545248670, table)
        delete_rows(con, 1545557366, 1545559131, table)
        delete_rows(con, 1545627631, 1545629640, table)
        delete_rows(con, 1545719336, 1545720430, table)
        delete_rows(con, 1545977374, 1545979301, table)
        delete_rows(con, 1546058643, 1546061636, table)
        delete_rows(con, 1546242220, 1546242512, table)
        delete_rows(con, 1546334479, 1546335248, table)
        delete_rows(con, 1546517881, 1546518855, table)
        delete_rows(con, 1547060502, 1547061743, table)
        delete_rows(con, 1547099682, 1547100651, table)
        delete_rows(con, 1547276544, 1547277427, table)
        delete_rows(con, 1547386299, 1547392041, table)
        delete_rows(con, 1547507658, 1547508639, table)
        delete_rows(con, 1547528889, 1547529718, table)
        delete_rows(con, 1547585580, 1547586257, table)
        delete_rows(con, 1547705649, 1547707389, table)
        delete_rows(con, 1547710355, 1547711841, table)
        delete_rows(con, 1547794549, 1547795467, table)
        delete_rows(con, 1547800149, 1547801075, table)
        delete_rows(con, 1547978575, 1547979117, table)
        delete_rows(con, 1549023730, 1549025070, table)
        delete_rows(con, 1549261021, 1549262220, table)
        delete_rows(con, 1549274799, 1549276027, table)
        delete_rows(con, 1549482223, 1549482942, table)
        delete_rows(con, 1549774951, 1549775512, table)
        delete_rows(con, 1549802642, 1549803647, table)
        delete_rows(con, 1549999713, 1550000336, table)
        delete_rows(con, 1550041705, 1550043003, table)
        delete_rows(con, 1550065278, 1550065742, table)
        delete_rows(con, 1550127551, 1550135344, table)
        delete_rows(con, 1550313983, 1550315187, table)
        delete_rows(con, 1550386479, 1550387654, table)
        delete_rows(con, 1550425625, 1550427306, table)
        delete_rows(con, 1550911707, 1550912637, table)
        delete_rows(con, 1550990225, 1550991041, table)
        delete_rows(con, 1551075714, 1551077034, table)
        delete_rows(con, 1551114681, 1551115090, table)
        delete_rows(con, 1551472217, 1551474696, table)
        delete_rows(con, 1551497002, 1551498131, table)
        delete_rows(con, 1551535157, 1551535854, table)
        delete_rows(con, 1551603043, 1551604570, table)
        delete_rows(con, 1551611897, 1551612707, table)
        delete_rows(con, 1551615797, 1551616512, table)
        delete_rows(con, 1551773395, 1551774278, table)
        delete_rows(con, 1551847552, 1551848069, table)
        delete_rows(con, 1551852471, 1551852740, table)
        delete_rows(con, 1551934301, 1551935989, table)
        delete_rows(con, 1552028555, 1552031024, table)
        delete_rows(con, 1552579048, 1552580015, table)
        delete_rows(con, 1552678283, 1552679648, table)
        delete_rows(con, 1552805692, 1552806603, table)
        delete_rows(con, 1552820722, 1552822268, table)
        delete_rows(con, 1553081434, 1553082352, table)
        delete_rows(con, 1553193785, 1553196264, table)
        delete_rows(con, 1553404359, 1553405932, table)
        delete_rows(con, 1553416708, 1553418395, table)
        delete_rows(con, 1553454456, 1553455531, table)
        delete_rows(con, 1553501914, 1553503068, table)
        delete_rows(con, 1553576079, 1553578058, table)

        delete_rows(con, 1553125531, 1553135913, table)
        delete_rows(con, 1553212877, 1553225588, table)
        delete_rows(con, 1555104457, 1555105702, table)
        delete_rows(con, 1555958944, 1555960296, table)
        delete_rows(con, 1556168621, 1556182367, table)

        update_rows(con, table, 'co2_in_ppm', 'Null', 1545145981, 1545146519)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1545227263, 1545227631)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1545285000, 1545286797)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1545371005, 1545372536)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1545380745, 1545381030)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1545383168, 1545383539)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1545385267, 1545385667)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1545540913, 1545559168)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1545566498, 1545566707)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1545567887, 1545569277)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1545587869, 1545588391)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1545629523, 1545635366)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1545718299, 1545726423)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1545890364, 1545894039)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1546084632, 1546085338)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1546195544, 1546196440)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1546220996, 1546228992)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1546235652, 1546242333)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1546331391, 1546335631)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1546417795, 1546418053)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1546421159, 1546421469)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1546428152, 1546428535)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1546636173, 1546637939)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1546703068, 1546705989)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1546717181, 1546717658)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1546790369, 1546791340)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1546804611, 1546808190)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1546826032, 1546826630)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1546928069, 1546928450)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1546934271, 1546934742)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1546956845, 1546959489)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1547013178, 1547018986)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1547035653, 1547036098)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1547116826, 1547117078)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1547238589, 1547242481)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1547285065, 1547286528)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1547358907, 1547361575)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1547365853, 1547366967)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1547401646, 1547414073)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1547430530, 1547431931)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1547506754, 1547507970)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1547527555, 1547541208)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1547642207, 1547642478)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1547728138, 1547728898)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1547781382, 1547782906)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1547792954, 1547910546)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1547954433, 1547955806)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1547977000, 1547984525)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1548015129, 1548021098)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1548035782, 1548036114)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1548127917, 1548129600)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1548136796, 1548138483)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1548214488, 1548215164)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1548223766, 1548224624)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1548253153, 1548263476)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1548395337, 1548396280)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1548473238, 1548474687)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1548500773, 1548502516)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1548582248, 1548584866)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1548640370, 1548647937)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1548658682, 1548660830)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1548684342, 1548684843)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1548741915, 1548743247)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1548773153, 1548774755)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1548819334, 1548820618)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1548945799, 1548948458)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1548994744, 1548995898)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1549009901, 1549038460)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1549178346, 1549180648)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1549183630, 1549185218)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1549245234, 1549246215)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1549269597, 1549270909)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1549302145, 1549303635)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1549347346, 1549348018)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1549426462, 1549432062)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1549449180, 1549449554)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1549479803, 1549488149)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1549514774, 1549523834)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1549560661, 1549562848)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1549568675, 1549569752)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1549601853, 1549607251)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1549688302, 1549695257)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1549740582, 1549747678)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1549769438, 1549775038)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1549787105, 1549803425)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1549864223, 1549883203)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1549917971, 1549918843)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1549951336, 1549962371)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550039599, 1550042041)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550124827, 1550125439)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550212101, 1550214205)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550215751, 1550216085)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550257053, 1550257947)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550295519, 1550296703)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550314739, 1550315530)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550454790, 1550455504)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550468492, 1550470112)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550488621, 1550491544)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550506022, 1550512993)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550555964, 1550558875)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550580264, 1550583278)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550719438, 1550720495)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550726882, 1550729565)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550727954, 1550729209)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550735936, 1550736543)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550754582, 1550755028)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550779557, 1550781465)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550805941, 1550807089)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550825568, 1550827408)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550854615, 1550855701)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550867413, 1550869662)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550902970, 1550903872)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550923195, 1550924158)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550976720, 1550977053)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1551044746, 1551066856)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1551073222, 1551078265)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1551123582, 1551124297)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1551131806, 1551140976)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1551159897, 1551164874)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1551182206, 1551182996)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1551218260, 1551252809)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1551288408, 1551290991)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1551301493, 1551566758)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1552541745, 1552545452)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1552615951, 1552616973)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1552633181, 1552635774)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1552670510, 1552671766)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1552717811, 1552719908)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1552735254, 1552735779)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1552755349, 1552756034)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1552803246, 1552805875)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1552817205, 1552820981)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1552874180, 1552874653)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1552936282, 1552943801)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1552973195, 1552979662)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1552978939, 1552979317)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553024783, 1553030073)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553053111, 1553059628)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553080803, 1553084232)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553103190, 1553104564)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553188229, 1553188916)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553229513, 1553237637)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553262944, 1553269324)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553292787, 1553295285)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553324214, 1553338825)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553354973, 1553356793)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553373203, 1553374328)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553398102, 1553404637)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553417628, 1553436890)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553451206, 1553454892)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553478994, 1553479425)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553478976, 1553486287)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553492458, 1553502654)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553549489, 1553551362)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553570379, 1553573569)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553583480, 1553587210)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553635132, 1553636434)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553657321, 1553658256)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553706044, 1553708104)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553722071, 1553725718)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553743747, 1553745696)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553762590, 1553763501)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553772176, 1553774977)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553784332, 1553786764)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553799401, 1553801677)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553830146, 1553833566)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553838765, 1553850190)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553893539, 1553899457)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553916558, 1553918288)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553921956, 1553929033)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553931578, 1553932937)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553981238, 1553984915)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554002889, 1554003141)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554016395, 1554031326)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554083384, 1554086706)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554093726, 1554098054)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554137881, 1554143446)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554171887, 1554173653)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554184771, 1554189400)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554206645, 1554208346)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554232125, 1554235364)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554258596, 1554265221)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554292942, 1554294103)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554308750, 1554314005)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554394128, 1554398955)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554430968, 1554432378)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554438340, 1554440790)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554525386, 1554528209)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554541700, 1554576785)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554611902, 1554617433)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554704067, 1554706700)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554740029, 1554743283)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554754748, 1554757465)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554776930, 1554777792)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554792792, 1554794174)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554823766, 1554833553)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554863145, 1554864289)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554913203, 1554916527)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554949732, 1554950621)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554960322, 1554961094)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554995347, 1554997314)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1555013013, 1555014786)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1555035284, 1555036854)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1555122584, 1555123292)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1555130124, 1555133032)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1555157269, 1555158046)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1555209047, 1555210137)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1555219384, 1555225901)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1555246421, 1555247727)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1555254400, 1555255752)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1555293313, 1555297152)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1555311070, 1555314436)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1555381511, 1555383197)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1555393648, 1555401929)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1555417011, 1555424133)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1555442573, 1555446379)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1555468122, 1555472063)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1555483254, 1555487400)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1545188672, 1545190836)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1545198789, 1545200198)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1545430372, 1545432576)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1545458410, 1545460140)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1545470826, 1545486366)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1545565171, 1545566529)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1546080679, 1546081451)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1546323017, 1546323764)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1546839685, 1546840259)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1546851590, 1546852281)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1547334868, 1547335237)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1547431624, 1547444930)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1547487611, 1547488317)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1547609189, 1547610275)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1547649333, 1547650457)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1548041087, 1548042288)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1548227868, 1548229232)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1548386930, 1548388024)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1548559409, 1548561163)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1548598944, 1548620264)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1548691897, 1548702139)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1548732467, 1548733750)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1548915223, 1548916380)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1549342496, 1549344241)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550158830, 1550159773)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550148239, 1550159993)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550263306, 1550263816)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550336948, 1550337663)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550415799, 1550416229)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1550767292, 1550768930)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1552417318, 1552418658)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1552707602, 1552708408)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553674868, 1553676051)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553754376, 1553755207)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1553940824, 1553944041)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554048968, 1554051117)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554180822, 1554184913)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554343981, 1554345894)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554517856, 1554519134)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554626409, 1554646727)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554688260, 1554692039)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554698794, 1554698794)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1554785397, 1554787389)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1555083524, 1555104922)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1555305437, 1555307093)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1555559745, 1555562843)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1555640993, 1555641923)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1555653845, 1555657074)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1555711923, 1555713433)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1555727957, 1555729268)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1555753451, 1555776430)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1555813890, 1555815833)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1555823295, 1555843416)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1555897522, 1555902061)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1555905436, 1555934315)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1555944901, 1555959377)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1555994795, 1556007259)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1556206226, 1556212471)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1556245928, 1556247336)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1556250957, 1556255471)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1556331588, 1556334455)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1556339194, 1556341540)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1556375075, 1556381147)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1556418637, 1556420362)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1556439429, 1556448876)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1556476515, 1556478129)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1556591735, 1556593245)
        update_rows(con, table, 'co2_in_ppm', 'Null', 1556607666, 1556608573)
    con.commit()

    for table in ['measured_klarka_shower', 'measured_klarka_shower_reduced']:
        delete_rows(con, 1543691739, 1543692802, table)
        delete_rows(con, 1543763354, 1543765783, table)
        delete_rows(con, 1543768918, 1543771764, table)
        delete_rows(con, 1543867909, 1543869942, table)
        delete_rows(con, 1544033698, 1544035813, table)
        delete_rows(con, 1544040744, 1544041792, table)
        delete_rows(con, 1544071291, 1544072531, table)
        delete_rows(con, 1544123600, 1544124611, table)
        delete_rows(con, 1544765501, 1544766004, table)
        delete_rows(con, 1544855407, 1544857498, table)
        delete_rows(con, 1544900701, 1544902516, table)
        delete_rows(con, 1544912466, 1544913135, table)
        delete_rows(con, 1544963217, 1544964542, table)
        delete_rows(con, 1544981395, 1544982187, table)
        delete_rows(con, 1545070652, 1545072295, table)
        delete_rows(con, 1545075421, 1545077116, table)
        delete_rows(con, 1545108753, 1545109405, table)
        delete_rows(con, 1545110920, 1545111711, table)
        delete_rows(con, 1545283812, 1545284350, table)
        delete_rows(con, 1545308109, 1545309888, table)
        delete_rows(con, 1545336923, 1545338519, table)
        delete_rows(con, 1545577036, 1545578297, table)
        delete_rows(con, 1545588610, 1545590175, table)
        delete_rows(con, 1545595024, 1545598810, table)
        delete_rows(con, 1545674780, 1545675524, table)
        delete_rows(con, 1545678932, 1545679614, table)
        delete_rows(con, 1545760372, 1545762405, table)
        delete_rows(con, 1545853669, 1545854644, table)
        delete_rows(con, 1545863051, 1545864591, table)
        delete_rows(con, 1545891711, 1545892821, table)
        delete_rows(con, 1545983681, 1545984176, table)
        delete_rows(con, 1546204528, 1546209592, table)
        delete_rows(con, 1546232917, 1546233497, table)
        delete_rows(con, 1541088008, 1541090731, table)
        delete_rows(con, 1541279857, 1541280254, table)
        delete_rows(con, 1541286112, 1541287036, table)
        delete_rows(con, 1541310816, 1541312132, table)
        delete_rows(con, 1541395087, 1541396619, table)
        delete_rows(con, 1541533493, 1541534571, table)
        delete_rows(con, 1541570587, 1541571704, table)
        delete_rows(con, 1541618285, 1541623525, table)
        delete_rows(con, 1541709669, 1541712171, table)
        delete_rows(con, 1541788483, 1541790486, table)
        delete_rows(con, 1541798528, 1541799419, table)
        delete_rows(con, 1541956889, 1541959658, table)
        delete_rows(con, 1541967882, 1541968823, table)
        delete_rows(con, 1542051900, 1542052167, table)
        delete_rows(con, 1542053266, 1542053430, table)
        delete_rows(con, 1542142212, 1542143028, table)
        delete_rows(con, 1542146397, 1542146820, table)
        delete_rows(con, 1542217575, 1542219168, table)
        delete_rows(con, 1542234623, 1542234984, table)
        delete_rows(con, 1542309302, 1542310528, table)
        delete_rows(con, 1542476232, 1542477958, table)
        delete_rows(con, 1542486437, 1542487023, table)
        delete_rows(con, 1542501113, 1542501929, table)
        delete_rows(con, 1542550482, 1542551077, table)
        delete_rows(con, 1542556849, 1542558429, table)
        delete_rows(con, 1542559096, 1542576536, table)
        delete_rows(con, 1542735230, 1542738298, table)
        delete_rows(con, 1542831037, 1542832725, table)
        delete_rows(con, 1543000103, 1543001059, table)
        delete_rows(con, 1543004811, 1543005128, table)
        delete_rows(con, 1543037605, 1543038200, table)
        delete_rows(con, 1543163486, 1543164834, table)
        delete_rows(con, 1543175265, 1543176590, table)
        delete_rows(con, 1543352357, 1543352598, table)
        delete_rows(con, 1543426616, 1543428060, table)
        delete_rows(con, 1543512702, 1543512988, table)
        delete_rows(con, 1543691767, 1543692587, table)
        delete_rows(con, 1543763423, 1543764583, table)
        delete_rows(con, 1543768987, 1543770574, table)
        delete_rows(con, 1543867918, 1543868611, table)
        delete_rows(con, 1544033794, 1544035100, table)
        delete_rows(con, 1544040702, 1544041341, table)
        delete_rows(con, 1544071317, 1544072310, table)
        delete_rows(con, 1544123601, 1544124405, table)
        delete_rows(con, 1544156029, 1544156443, table)
        delete_rows(con, 1544734474, 1544734702, table)
        delete_rows(con, 1544765498, 1544765910, table)
        delete_rows(con, 1544855426, 1544856588, table)
        delete_rows(con, 1544900830, 1544902090, table)
        delete_rows(con, 1544908144, 1544908807, table)
        delete_rows(con, 1544912462, 1544913127, table)
        delete_rows(con, 1544963244, 1544964300, table)
        delete_rows(con, 1544981421, 1544982190, table)
        delete_rows(con, 1544988594, 1544988905, table)
        delete_rows(con, 1545018603, 1545018925, table)
        delete_rows(con, 1545022806, 1545023306, table)
        delete_rows(con, 1545070654, 1545072029, table)
        delete_rows(con, 1545075436, 1545076270, table)
        delete_rows(con, 1545108685, 1545109238, table)
        delete_rows(con, 1545110905, 1545111469, table)
        delete_rows(con, 1545153800, 1545154028, table)
        delete_rows(con, 1545283789, 1545284218, table)
        delete_rows(con, 1545308128, 1545309223, table)
        delete_rows(con, 1545336903, 1545337807, table)
        delete_rows(con, 1545577014, 1545577832, table)
        delete_rows(con, 1545588603, 1545590232, table)
        delete_rows(con, 1545594999, 1545595382, table)
        delete_rows(con, 1545596619, 1545598537, table)
        delete_rows(con, 1545678869, 1545679753, table)
        delete_rows(con, 1545760555, 1545762400, table)
        delete_rows(con, 1545764194, 1545764426, table)
        delete_rows(con, 1545766647, 1545766916, table)
        delete_rows(con, 1545853642, 1545854191, table)
        delete_rows(con, 1545862987, 1545864534, table)
        delete_rows(con, 1545891683, 1545892510, table)
        delete_rows(con, 1545949961, 1545950188, table)
        delete_rows(con, 1545951597, 1545951803, table)
        delete_rows(con, 1545983696, 1545984249, table)
        delete_rows(con, 1546204526, 1546205532, table)
        delete_rows(con, 1546208091, 1546208889, table)
        delete_rows(con, 1546232742, 1546233400, table)
        delete_rows(con, 1546244151, 1546245205, table)
        delete_rows(con, 1546248620, 1546249021, table)
        delete_rows(con, 1546277136, 1546278849, table)
        delete_rows(con, 1541478527, 1541479393, table)
    con.commit()

    for table in ['measured_david', 'measured_david_reduced']:
        update_rows(con, table, 'open_close', '0', 1556212321, 1556212333)
        update_rows(con, table, 'open_close', '0', 1556483850, 1556483863)
        update_rows(con, table, 'open_close', '0', 1556275417, 1556275423)
        update_rows(con, table, 'open_close', '0', 1556558716, 1556558729)

        delete_rows(con, 1554361539, 1554362046, table)
        delete_rows(con, 1554435692, 1554435878, table)
        delete_rows(con, 1554557639, 1554558434, table)
        delete_rows(con, 1554620345, 1554620760, table)
        delete_rows(con, 1554706450, 1554706758, table)
        delete_rows(con, 1554736285, 1554736553, table)
        delete_rows(con, 1554747168, 1554747168, table)
        delete_rows(con, 1555571304, 1555571734, table)
        delete_rows(con, 1555610575, 1555610575, table)
        delete_rows(con, 1555959752, 1555959969, table)
        delete_rows(con, 1555959969, 1555962048, table)
        delete_rows(con, 1555999916, 1555999916, table)
        delete_rows(con, 1556167497, 1556167675, table)
        delete_rows(con, 1556212375, 1556218781, table)
        delete_rows(con, 1556407111, 1556407111, table)
        delete_rows(con, 1554497448, 1554497704, table)
        delete_rows(con, 1554640921, 1554641794, table)
        delete_rows(con, 1554647586, 1554648845, table)
        delete_rows(con, 1554753783, 1554754117, table)
        delete_rows(con, 1554829883, 1554830518, table)
        delete_rows(con, 1555610605, 1555611521, table)
        delete_rows(con, 1555964860, 1555965077, table)
    con.commit()

    for table in ['measured_martin', 'measured_martin_reduced']:
        cur.execute('UPDATE {0} SET co2_in_ppm = Null WHERE measured_time >= {1} AND measured_time <= {2}'
                    .format(table, 1556131671, 1556527728704))

        update_rows(con, table, 'open_close', '0', 1554369411, 1554369419)
        update_rows(con, table, 'open_close', '1', 1556010237, 1556010281)
        update_rows(con, table, 'open_close', '1', 1556011145, 1556011174)

        delete_rows(con, 1554105279, 1554111856, table)
        delete_rows(con, 1554209613, 1554213251, table)
        delete_rows(con, 1554311736, 1554312129, table)
        delete_rows(con, 1554369256, 1554369855, table)
        delete_rows(con, 1554382936, 1554386565, table)
        delete_rows(con, 1554549577, 1554555291, table)
        delete_rows(con, 1554695016, 1554697933, table)
        delete_rows(con, 1554752248, 1554752753, table)
        delete_rows(con, 1554954830, 1554956089, table)
        delete_rows(con, 1554986587, 1554991207, table)
        delete_rows(con, 1555224375, 1555224927, table)
        delete_rows(con, 1556009821, 1556011638, table)
        delete_rows(con, 1556049828, 1556050173, table)
        delete_rows(con, 1556096559, 1556097672, table)
        delete_rows(con, 1556104984, 1556106264, table)
        delete_rows(con, 1554111977, 1554113616, table)
        delete_rows(con, 1554275418, 1554278553, table)
        delete_rows(con, 1554782585, 1554783859, table)
        delete_rows(con, 1554874366, 1554908657, table)
        delete_rows(con, 1554956135, 1554958682, table)
        delete_rows(con, 1554994535, 1554998530, table)
        delete_rows(con, 1556165161, 1556166805, table)
    con.commit()


def devices(filename='devices.json'):
    with open(filename, 'r') as f:
        data = json.load(f)

    return data


def create_update_table(con, clients, start, end, devices, tables):
    step_size = 600
    time_shift = 1200
    min_commit_size = 10000
    precision = 2

    total_min = None
    last_inserted_table = tables[0][0]
    str_tables = ''

    # delete last interval where missing values could appear because some values in this interval did not exist
    delete_step = 1 * step_size

    for table in tables:
        DBUtil.create_table(con, table[0])

        DBUtil.delete_from_time(con, table[0], delete_step)
        str_tables += table[0] + ', '

        last_inserted_row = DBUtil.last_inserted_values(con, table[0])
        if last_inserted_row is None:
            continue

        if total_min is None or total_min > last_inserted_row[0]:
            total_min = last_inserted_row[0]
            last_inserted_table = table[0]

    last_open_close_state = 0
    actual_commit_size = 0

    logging.info('table: %s' % str_tables)

    for interval_from in range(start - delete_step, end, step_size):
        interval_to = interval_from + step_size

        # if some data is stored in database and timestamp of last inserted event is
        # greater than currently processed interval, the interval is not processed,
        # otherwise, a table is updated using new data from this timestamp
        if total_min is not None:
            if interval_to < total_min:
                # skip inserted interval
                continue

        logging.debug('processed interval %s' % DateTimeUtil.create_interval_str(interval_from,
                                                                                 interval_to))

        maps, values = PreProcessing.prepare(clients, devices, interval_from, interval_to,
                                             last_open_close_state, time_shift)

        for table in tables:
            if 'filtered' in table[0]:
                values = PreProcessing.ppm_filter(values)

            PreProcessing.insert_values(con, table[0], values, maps, table[1], precision)
            actual_commit_size += step_size // table[1]

        if actual_commit_size > min_commit_size:
            logging.debug('commit %s rows' % actual_commit_size)
            con.commit()
            actual_commit_size = 0

        last_open_close_state = DBUtil.last_inserted_open_close_state(con, last_inserted_table)

    logging.debug('commit %s rows' % actual_commit_size)
    con.commit()

    logging.info('table %s created and updated' % str_tables)


def peto_intrak_db(con, cls, start, end, devs):
    # date when Device ID of Protronix CO2 sensor was changed
    middle = int(DateTimeUtil.local_time_str_to_utc('2019/02/20 03:00:00').timestamp())

    tables = [
        ('measured_peto', 1),
        ('measured_peto_reduced', 15),
        ('measured_filtered_peto', 1),
        ('measured_filtered_peto_reduced', 15),
    ]

    create_update_table(con, cls, start, middle, devs['peto'], tables)
    create_update_table(con, cls, middle, end, devs['peto2'], tables)


def klarka_izba_db(con, cls, start, end, devs):
    tables = [
        ('measured_klarka', 1),
        ('measured_klarka_reduced', 15),
    ]
    create_update_table(con, cls, start, end, devs['klarka'], tables)

    # the second database contains outdoor IQ Home sensor from this date
    middle = int(DateTimeUtil.local_time_str_to_utc('2019/02/19 12:00:00').timestamp())
    tables = [
        ('measured_klarka_iqhome', 1),
        ('measured_klarka_iqhome_reduced', 15),
    ]
    create_update_table(con, cls, start, middle, devs['klarka'], tables)
    create_update_table(con, cls, middle, end, devs['klarka2'], tables)


def klarka_sprcha_db(con, cls, start, end, devs):
    tables = [
        ('measured_klarka_shower', 1),
        ('measured_klarka_shower_reduced', 15),
    ]
    create_update_table(con, cls, start, end, devs['klarka_shower2'], tables)

    update_shower(con, 'examples/events_klarka_shower.json', ['measured_klarka_shower', 'measured_klarka_shower_reduced'])


def update_shower(con, filename, table_names):
    pwd = dirname(__file__)
    abspath(join(pwd, './..', '')) + '/'

    events = Storage(filename, 0, '').read_meta()

    cur = con.cursor()
    for table in table_names:
        cur.execute('UPDATE {0} SET open_close = 0'.format(table))
    con.commit()

    for event in events:
        start = event['e_start']['timestamp']
        end = event['e_end']['timestamp']

        for timestamp in range(start, end):
            for table in table_names:
                DBUtil.update_attribute(con, table, 'open_close', 1, timestamp)
        con.commit()


def david(con, cls, start, end, devs):
    tables = [
        ('measured_david', 1),
        ('measured_david_reduced', 15),
    ]
    create_update_table(con, cls, start, end, devs['david'], tables)


def martin(con, cls, start, end, devs):
    tables = [
        ('measured_martin', 1),
        ('measured_martin_reduced', 15),
    ]
    create_update_table(con, cls, start, end, devs['martin'], tables)


def martin_door(con, cls, start, end, devs):
    tables = [
        ('measured_martin_door', 1),
        ('measured_martin_door_reduced', 15),
    ]
    create_update_table(con, cls, start, end, devs['martin_door'], tables)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
    devs = devices()

    con = ConnectionUtil.create_con()
    cur = con.cursor()

    cls = {
        "ant-work": BeeeOnClient("ant-work.fit.vutbr.cz", 8010),
        "rehivetech": BeeeOnClient("beeeon.rehivetech.com", 8010),
    }

    cls['ant-work'].api_key = ConnectionUtil.api_key('ant-work')
    cls['rehivetech'].api_key = ConnectionUtil.api_key('rehivetech')

    # from 2018/09/20 00:01:00
    start = int(DateTimeUtil.local_time_str_to_utc('2018/09/20 01:00:00').timestamp())
    end = int(time.time())

    peto_intrak_db(con, cls, start, end, devs)
    klarka_izba_db(con, cls, start, end, devs)

    start = int(DateTimeUtil.local_time_str_to_utc('2018/07/18 06:00:00').timestamp())
    klarka_sprcha_db(con, cls, start, end, devs)

    start = int(DateTimeUtil.local_time_str_to_utc('2019/04/03 15:00:00').timestamp())
    david(con, cls, start, end, devs)

    start = int(DateTimeUtil.local_time_str_to_utc('2019/04/01 15:00:00').timestamp())
    martin(con, cls, start, end, devs)
    martin_door(con, cls, start, end, devs)

    update_invalid_values(con)
