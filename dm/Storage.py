import json
import os
from dm.DateTimeUtil import DateTimeUtil
from dm.SQLUtil import SQLUtil


class Storage:
    def __init__(self, filename: str, no_event_time_shift: int, owner: str, table_name: str):
        self.__filename = self.__root_folder() + filename
        self.__no_event_time_shift = no_event_time_shift
        self.__owner = owner
        self.__table_name = table_name

    def __root_folder(self):
        pwd = os.path.dirname(__file__)
        return os.path.abspath(os.path.join(pwd, './..', '')) + '/'

    def read_meta(self):
        with open(self.__filename) as f:
            events = json.load(f)

        out = []
        for event in events['events']:
            # stributy, ktore su spolocne pre vsetky udalosti
            attributes = {
                'e_start': {
                    'readable': event['times']['event_start'],
                    'timestamp': int(DateTimeUtil.local_time_str_to_utc(
                        event['times']['event_start']).timestamp())
                },
                'e_end': {
                    'readable': event['times']['event_end'],
                    'timestamp': int(
                        DateTimeUtil.local_time_str_to_utc(
                            event['times']['event_end']).timestamp())
                },
                'measured': {
                    'pressure_in_hpa': [],
                    'temperature_in_celsius': [],
                    'temperature_in2_celsius': [],
                    'temperature_out_celsius': [],
                    'rh_in_percentage': [],
                    'rh_in_absolute_g_m3': [],
                    'rh_in_specific_g_kg': [],
                    'rh_in2_percentage': [],
                    'rh_in2_absolute_g_m3': [],
                    'rh_in2_specific_g_kg': [],
                    'rh_out_percentage': [],
                    'rh_out_absolute_g_m3': [],
                    'rh_out_specific_g_kg': [],
                    'co2_in_ppm': [],
                    'co2_in_g_m3': []
                },
                'derivatives': {
                    'after': [],
                    'before': [],
                    'no_event_after': [],
                    'no_event_before': []
                },
                'no_event_time_shift': self.__no_event_time_shift,
                'no_event_columns': None,
                'owner': self.__owner,
                'valid_event': True
            }

            # doplnenie atributov, ktore su specificke pre dany json
            # len sa nakopuruju jednotlive polozky json struktury
            for key, value in event.items():
                if key in ['times', 'devices']:
                    continue
                attributes[key] = value

            out.append(attributes)

        return out

    def load_data(self, con, start_shift: int, end_shift: int, column: str):
        data = self.read_meta()

        cur = con.cursor()
        for i in range(0, len(data)):
            event = data[i]
            owner = event['owner']

            event['start_shift'] = start_shift
            event['end_shift'] = end_shift

            start = event['e_start']['timestamp'] + start_shift
            end = event['e_end']['timestamp'] + end_shift

            # kontrola, ci velkost intervalu v db bez Null hodnot je rovnaka
            # ako rozdiel intervalov
            sql = SQLUtil.select_interval_size(self.__table_name, start, end, column, owner)
            cur.execute(sql)

            if end - start + 1 != cur.fetchone()[0]:
                event['valid_event'] = False
                continue

            # zistanie pozadovaneho intervalu
            cur.execute(SQLUtil.select_interval(self.__table_name, start, end, '*', owner))

            # doplnenie udajov z db do struktury
            for row in cur.fetchall():
                event['measured']['pressure_in_hpa'].append(row[4])
                event['measured']['temperature_in_celsius'].append(row[5])
                event['measured']['temperature_in2_celsius'].append(row[6])
                event['measured']['temperature_out_celsius'].append(row[7])
                event['measured']['rh_in_percentage'].append(row[8])
                event['measured']['rh_in2_percentage'].append(row[9])
                event['measured']['rh_in_absolute_g_m3'].append(row[10])
                event['measured']['rh_in2_absolute_g_m3'].append(row[11])
                event['measured']['rh_in_specific_g_kg'].append(row[12])
                event['measured']['rh_in2_specific_g_kg'].append(row[13])
                event['measured']['rh_out_percentage'].append(row[14])
                event['measured']['rh_out_absolute_g_m3'].append(row[15])
                event['measured']['rh_out_specific_g_kg'].append(row[16])
                event['measured']['co2_in_ppm'].append(row[17])
                event['measured']['co2_in_g_m3'].append(row[18])

            # ak je nastaveny posun no_eventu na nulu tato cast sa preskoci,
            # v opacnom priapde sa stiahne hodnota
            if event['no_event_time_shift'] != 0:
                sql = SQLUtil.select_one_value(self.__table_name,
                                               start + event['no_event_time_shift'],
                                               '*', owner)
                cur.execute(sql)
                event['no_event_columns'] = cur.fetchone()

        return data