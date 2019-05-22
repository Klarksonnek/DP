"""Utils that contain simple SQL queries.
"""

__author__ = 'Peter Tisovčík'
__email__ = 'xtisov00@stud.fit.vutbr.cz'


class SQLUtil:
    @staticmethod
    def select_interval_size(table_name: str, start: int, end: int, column: str):
        """Zistenie poctu zaznamov, ktore nie su null v danom stlpci

        :param column:
        :param table_name:
        :param start:
        :param end:
        :return:
        """

        sql = 'SELECT COUNT(*) FROM ' + table_name
        sql += ' WHERE measured_time >= ' + str(start)
        sql += ' and measured_time <= ' + str(end)
        sql += ' and ' + column + ' IS NOT NULL'

        return sql

    @staticmethod
    def select_interval(table_name: str, start: int, end: int, columns: str):
        """Vyber casoveho intervalu na zaklade zadanych casov.

        :param columns: zoznam stlpcov, ktore sa maju vybrat, hviezdicka znaci vsetky stlpce
        :param table_name: nazov tabulky, z ktorej sa maju vyberat udaje
        :param start: timestamp zaciatku intervalu
        :param end: timestamp konca intervalu
        :return: sql dotaz na vyber daneho intervalu
        """

        sql = 'SELECT ' + columns + ' FROM ' + table_name
        sql += ' WHERE measured_time >= ' + str(start)
        sql += ' and measured_time <= ' + str(end)

        return sql

    @staticmethod
    def select_one_value(table_name: str, measured_time: int, columns: str):
        """Vyber jednej hodnoty na zaklade zadaneho casu.

        :param columns: zoznam stlpcov, ktore sa maju vybrat, hviezdicka znaci vsetky stlpce
        :param table_name: nazov tabulky, z ktorej sa maju vyberat udaje
        :param measured_time: cas, v ktorom sa nachadza pozadovana hodnota
        :return: sql dotaz na vyber jednej hodnoty
        """

        sql = 'SELECT ' + columns + ' FROM ' + table_name
        sql += ' WHERE measured_time = ' + str(measured_time)

        return sql
