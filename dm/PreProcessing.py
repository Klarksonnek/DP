from env_dp.core import BeeeOnClient
from dm.DBUtil import DBUtil
from dm.ValueConversionUtil import ValueConversionUtil as conv
from dm.DateTimeUtil import DateTimeUtil


class PreProcessing:
    TIME_ATTR_NAME = 'measured_time'
    TIME_STRING_ATTR_NAME = 'measured_time_str'
    OPEN_CLOSE_ATTR_NAME = 'open_close'
    OWNER_ATTR_NAME = 'owner'

    @staticmethod
    def db_name_maps(devices: list) -> list:
        """Zoznam nazvov stlpcov v db, ktory sa nacita zo zoznamu zariadeni.

        Nazov stlpca je nacitany zo suboru, aby bolo mozne priradit danu hodnotu
        do spravneho stlpca v db.

        :param devices: zoznam informacii o zariadeniach
        :return: zoznam nazvov stlpcov
        """

        names = []
        for device in devices:
            names.append(device['db_column_name'])

        return names

    @staticmethod
    def rename_attribute(values: list, old_attribute: str, new_attribute: str) -> list:
        """Premenovanie atributu v datach, z povodneho nazvu na novy nazov.

        :param values: zoznam hodnot
        :param old_attribute: nazov povodneho atributu
        :param new_attribute: nazov noveho atributu
        :return: zoznam hodnot s premenovanym atributom
        """

        out_values = []

        # loop over all values
        for value in values:
            new_val = {}

            # loop over all attributes
            for key, val in value.items():
                if key == old_attribute:
                    new_val[new_attribute] = val
                    continue

                new_val[key] = val
            out_values.append(new_val)

        return out_values

    @staticmethod
    def rename_all_attributes(items: list, devices: list) -> list:
        """Premenovanie vsetkych atributov v zozname, ktory obsahuje zoznam hodnot.

        Premenovanie jednodlivych atributov, ktore sa viazu k danym modulom. Predvolene
        ma kazda stiahnuta hodnota zoznama hodnot s preddefinovam nazvom atributov.
        Nove nazvy atributov su odvodene zo zoznamu zariadeni.

        :param items: zoznam, v ktorom je zoznam hodnot
        :param devices: zoznam informacii o zariadeniach
        :return: zoznam, v ktorom je upraveny zoznam hodnot s premenovanymi atributmi
        """

        out_values = []
        maps = PreProcessing.db_name_maps(devices)

        for i in range(0, len(items)):
            item = items[i]
            key = maps[i]

            item = PreProcessing.rename_attribute(item, 'at', PreProcessing.TIME_ATTR_NAME)
            item = PreProcessing.rename_attribute(item, 'value', key)

            out_values.append(item)

            i += 1

        return out_values

    @staticmethod
    def download_data(client: BeeeOnClient, devices: list, start: int, end: int) -> list:
        """ Stiahnutie potrebnych dat na zaklade zoznamu zariadeni.

        :param client: klient, ktory umoznuje stiahnut data na zaklade zadanych dat
        :param devices: zoznam informacii o zariadeniach
        :param start: cas, od ktoreho sa maju stiahnut data
        :param end: cas, do ktoreho sa maju stiahnut data
        :return: zoznam stiahnutych dat
        """

        out_items = []

        for dev in devices:
            values = client.history(
                dev['gateway'],
                dev['device'],
                dev['module'],
                start,
                end
            )['data']

            out_items.append(values)

        return out_items

    @staticmethod
    def generate_open_close(values: list, time_attribute_name: str,
                            open_close_attribute_name: str, start: int, end: int,
                            last_open_close_state: int) -> list:

        # prevod hodnot zo stringu do cisiel
        for i in range(0, len(values)):
            values[i][open_close_attribute_name] = float(values[i][open_close_attribute_name])

        out = []

        # vygenerovanie zoznamu hodnot
        for t in range(start, end):
            out.append({
                time_attribute_name: t,
                open_close_attribute_name: None
            })

        out_index = 0
        for i in range(0, len(values)):
            value = values[i]

            for tt in range(out_index, len(out)):
                if out[tt][time_attribute_name] >= value[time_attribute_name]:
                    break
                out[tt][open_close_attribute_name] = last_open_close_state
                out_index += 1

            last_open_close_state = value[open_close_attribute_name]

        # dogenerovanie dat, v pripade, ze akcia s oknom je v ramci zadaneho intervalu
        for tt in range(out_index, len(out)):
            out[tt][open_close_attribute_name] = last_open_close_state

        return out


    @staticmethod
    def generate_data(values: list, value_attribute: str, time_attribute: str,
                      precision: int=7) -> list:
        """Rozgenerovanie stiahnutych dat, tak by boli data dostupne kazdu sekundu.

        Rozgenerovanie je linearne a nezohladnuje nijak veliciny ani ich priebeh.

        :param values: zoznam hodnot
        :param value_attribute: nazov atributu, v ktorom su ulozene data
        :param time_attribute: nazov atributu, v ktorom je ulozeny timestamp
        :param precision: presnost daneho vypoctu
        :return: zoznam hodnot, v ktorom je rozgenerovany zoznam hodnot na kazdu sekundu
        """

        new = []

        for i in range(0, len(values) - 1):
            act_value = values[i]
            next_value = values[i + 1]

            value_start = act_value[value_attribute]
            value_end = next_value[value_attribute]

            if value_start is None or value_end is None:
                continue

            value_start = float(act_value[value_attribute])
            value_end = float(next_value[value_attribute])

            time_start = act_value[time_attribute]
            time_end = next_value[time_attribute]

            if value_start - value_end == 0:
                value_increase = 0
            else:
                value_diff = value_end - value_start
                value_increase = value_diff / (time_end - time_start)

            act_value = value_start
            for j in range(1, time_end - time_start + 1):
                new.append({
                    time_attribute: time_start + j,
                    value_attribute: round(act_value, precision)
                })
                act_value = act_value + value_increase

        return new

    @staticmethod
    def cut_interval(items: list, start: int, end: int, time_attribute: str) -> list:
        """Orezanie vsetkych dat tak, aby mali rovnaky interval (zaciatocny a koncovy cas).

        :param items: zoznam, v ktorom je zoznam hodnot
        :param start: cas, od ktoreho sa maju data orezat
        :param end: cas, do ktoreho sa maju data orezat
        :param time_attribute: posun zaciatku a konca casovych intervalo
        :return: zoznam, v ktorom je orezany zoznam hodnot
        """

        out_values = []

        for value in items:
            if value[time_attribute] < start or value[time_attribute] >= end:
                continue

            out_values.append(value)

        return out_values

    @staticmethod
    def check_equal_size(items: list) -> None:
        """Kontrola, ci zoznamy hodnot v zozname maju rovnaku velkost.

        :param items: zoznam, v ktorom je zoznam hodnot
        """

        length = None
        for item in items:
            if length is None:
                length = len(item)
                continue

            if length != len(item):
                raise SyntaxError('size of all list must be equal')

    @staticmethod
    def check_start_end_interval(items: list, time_attribute: str) -> None:
        """Kontrola, zoznamy hodnot maju rovnaky pociatocny a koncovy cas.

        :param items: zoznam, v ktorom je zoznam hodnot
        :param time_attribute: nazov atributu, v ktorom sa nachadza timestamp
        :return:
        """

        start = None
        end = None

        for item in items:
            if start is None:
                start = item[0][time_attribute]

            if end is None:
                end = item[-1][time_attribute]

            if not item:
                raise SyntaxError('empty list of values')

            if start != item[0][time_attribute]:
                raise SyntaxError('start time must be equal in all items')

            if end != item[-1][time_attribute]:
                raise SyntaxError('end time must be equal in all items')

    @staticmethod
    def join_items(items: list, time_attribute: str) -> list:
        """Spojenie niekolkych zoznamov hodnot do jedneho.

        Vysledny zoznam obsahuje len jeden atributom s casom, pretoze su casy rovnake.
        Obsahuje ale rozne hodnoty, ktore boli v roznych zoznamoch.

        :param items: zoznam, v ktorom je zoznam hodnot
        :param time_attribute: nazov atributu, ktory obsahuje cas
        :return: jeden zoznam hodnot zo vsetkymi atributmi a casom
        """

        PreProcessing.check_equal_size(items)
        PreProcessing.check_start_end_interval(items, time_attribute)

        item_out = items[0]
        for values in items[1:]:

            for i in range(0, len(values)):
                item = values[i]

                # loop over dictionary items
                for key, value in item.items():
                    if key is time_attribute and item_out[i][time_attribute] != value:
                        raise SyntaxError(
                            'value in `%s` attribute is different' % (time_attribute))

                    item_out[i][key] = value

        return item_out

    @staticmethod
    def prepare_downloaded_data(client: BeeeOnClient, devices: list, start: int, end: int,
                                time_shift: int, last_open_close_state) -> list:

        data = PreProcessing.download_data(client, devices,
                                           start - time_shift,
                                           end + time_shift)
        data = PreProcessing.rename_all_attributes(data, devices)

        new_data = []
        maps = PreProcessing.db_name_maps(devices)
        i = 0
        for key in maps:
            item = data[i]
            val = []

            if key == PreProcessing.OPEN_CLOSE_ATTR_NAME:
                val = PreProcessing.generate_open_close(item, PreProcessing.TIME_ATTR_NAME,
                                                        key, start, end, last_open_close_state)
            else:
                val = PreProcessing.generate_data(item, key, PreProcessing.TIME_ATTR_NAME)
                val = PreProcessing.generate_data(val, key, PreProcessing.TIME_ATTR_NAME)

            val = PreProcessing.cut_interval(val, start, end, PreProcessing.TIME_ATTR_NAME)

            PreProcessing.check_equal_size(val)
            new_data.append(val)

            i += 1

        return new_data

    @staticmethod
    def prepare_value_conversion(value):
        # absolute humidity in
        if 'temperature_in_celsius' in value and 'rh_in_percentage' in value:
            value['rh_in_absolute_g_m3'] = conv.rh_to_absolute_g_m3(
                value['temperature_in_celsius'],
                value['rh_in_percentage'])

        # specific humidity in
        if 'temperature_in_celsius' in value and 'rh_in_percentage' in value:
            value['rh_in_specific_g_kg'] = conv.rh_to_specific_g_kg(
                value['temperature_in_celsius'],
                value['rh_in_percentage'])

        # absolute humidity out
        if 'temperature_out_celsius' in value and 'rh_out_percentage' in value:
            value['rh_out_absolute_g_m3'] = conv.rh_to_absolute_g_m3(
                value['temperature_out_celsius'],
                value['rh_out_percentage'])

        # specific humidity out
        if 'temperature_out_celsius' in value and 'rh_out_percentage' in value:
            value['rh_out_specific_g_kg'] = conv.rh_to_specific_g_kg(
                value['temperature_out_celsius'],
                value['rh_out_percentage'])

        # CO2 concentration
        if 'co2_in_ppm' in value:
            value['co2_in_g_m3'] = conv.co2_ppm_to_mg_m3(value['co2_in_ppm'])

        return value

    @staticmethod
    def insert_values(conn, table_name, values, maps, owner, write_each, precision):
        for i in range(0, len(values)):
            value = values[i]
            t = ()

            if i % write_each != 0:
                continue

            for column in DBUtil.measured_values_table_column_names():
                if column == PreProcessing.TIME_STRING_ATTR_NAME:
                    t += (DateTimeUtil.utc_timestamp_to_str(
                        value[PreProcessing.TIME_ATTR_NAME]),)
                    continue

                if column == PreProcessing.OWNER_ATTR_NAME:
                    t += (owner,)
                    continue

                if column in maps:
                    t += (round(value[column], precision),)
                else:
                    t += (None,)

            DBUtil.insert_value(conn, t, False, table_name)


    @staticmethod
    def prepare(client: BeeeOnClient, conn, table_name: str, devices: list, start: int,
                end: int, last_open_close_state: int, owner: str,
                time_shift: int, precision: int=2, write_each: int=1) -> None:

        values = []
        try:
            values = PreProcessing.prepare_downloaded_data(client, devices, start, end,
                                                           time_shift, last_open_close_state)

            PreProcessing.check_start_end_interval(values, PreProcessing.TIME_ATTR_NAME)
            values = PreProcessing.join_items(values, PreProcessing.TIME_ATTR_NAME)
        except:
            maps = [
                PreProcessing.TIME_ATTR_NAME,
                PreProcessing.TIME_STRING_ATTR_NAME,
                PreProcessing.OPEN_CLOSE_ATTR_NAME,
                PreProcessing.OWNER_ATTR_NAME
            ]

            PreProcessing.insert_values(conn, table_name, values[0], maps, owner,
                                        write_each, precision)

            return

        for value in values:
            PreProcessing.prepare_value_conversion(value)

        maps = PreProcessing.db_name_maps(devices)
        for value in values:
            for key, _ in value.items():
                maps.append(key)
            break

        # odstranenie duplicit zo zonamu
        maps = list(set(maps))

        PreProcessing.insert_values(conn, table_name, values, maps, owner,
                                    write_each, precision)
