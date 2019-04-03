import logging
from mysql.connector.errors import Error
from mysql.connector.errors import DataError
from dm.DateTimeUtil import DateTimeUtil


class DBUtil:
    @staticmethod
    def create_table(conn, table_name):
        '''
        http://www.mysqltutorial.org/mysql-decimal/
        '''

        sql = """
            CREATE TABLE IF NOT EXISTS """ + table_name + """ (
            measured_time INT,
            measured_time_str TIMESTAMP,
            open_close BOOLEAN,
            pressure_in_hpa DECIMAL(6,2),
            temperature_in_celsius DECIMAL(4,2),
            temperature_in2_celsius DECIMAL(4,2),
            temperature_out_celsius DECIMAL(4,2),
            rh_in_percentage DECIMAL(4,2),
            rh_in2_percentage DECIMAL(4,2),
            rh_in_absolute_g_m3 DECIMAL(4,2),
            rh_in2_absolute_g_m3 DECIMAL(4,2),
            rh_in_specific_g_kg DECIMAL(4,2),
            rh_in2_specific_g_kg DECIMAL(4,2),
            rh_out_percentage DECIMAL(4,2),
            rh_out_absolute_g_m3 DECIMAL(4,2),
            rh_out_specific_g_kg DECIMAL(4,2),
            co2_in_ppm DECIMAL(6,2),
            PRIMARY KEY (measured_time)
        )"""

        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

    @staticmethod
    def drop_table(conn, table_name):
        cur = conn.cursor()
        cur.execute('DROP TABLE IF EXISTS ' + table_name)
        conn.commit()

    @staticmethod
    def measured_values_table_column_names():
        return [
            'measured_time',
            'measured_time_str',
            'open_close',
            'pressure_in_hpa',
            'temperature_in_celsius',
            'temperature_in2_celsius',
            'temperature_out_celsius',
            'rh_in_percentage',
            'rh_in2_percentage',
            'rh_in_absolute_g_m3',
            'rh_in2_absolute_g_m3',
            'rh_in_specific_g_kg',
            'rh_in2_specific_g_kg',
            'rh_out_percentage',
            'rh_out_absolute_g_m3',
            'rh_out_specific_g_kg',
            'co2_in_ppm'
        ]

    @staticmethod
    def insert_value(conn, task, enable_commit, table_name):
        sql = 'INSERT INTO ' + table_name + ' ('

        names = DBUtil.measured_values_table_column_names()

        for i in range(0, len(names)):
            sql += names[i]
            if i != len(names) - 1:
                sql += ','

        sql += ') VALUES ('
        for i in range(0, len(names)):
            sql += '%s'
            if i != len(names) - 1:
                sql += ','

        sql += ')'

        # ak je duplicitny kluc ignoruje sa
        try:
            cur = conn.cursor()
            cur.execute(sql, task)
        except DataError as e:
            logging.exception(e)
            exit(1)
        except Error:
            return

        if enable_commit:
            conn.commit()

    @staticmethod
    def last_inserted_open_close_state(conn, table_name):
        return DBUtil.last_inserted_values(conn, table_name)[2]

    @staticmethod
    def rows_count(conn, table_name):
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM ' + table_name)
        return cur.fetchall()[0][0]

    @staticmethod
    def last_inserted_values(conn, table_name):
        cur = conn.cursor()

        sql = """
            select * from `""" + table_name + """`
            where measured_time = (SELECT MAX(measured_time) as mm FROM """ + table_name + ')'

        cur.execute(sql)

        res = cur.fetchall()
        if not res:
            return None

        return res[0]

    @staticmethod
    def first_inserted_values(conn, table_name):
        cur = conn.cursor()

        sql = """
            select * from `""" + table_name + """`
            where measured_time = (SELECT MIN(measured_time) as mm FROM """ + table_name + ')'

        cur.execute(sql)

        res = cur.fetchall()
        if not res:
            return None

        return res[0]

    @staticmethod
    def check_timestamp_order(con, table_name):
        """Overenie ci db obsahuje databazu, kde nechyba ziadna hodnota

        :param con: spojenie s db
        :param table_name: nazov tabulky pre overenie
        """

        cur = con.cursor()

        rows = DBUtil.rows_count(con, table_name)
        if rows == 0:
            logging.debug('db is empty')
            return

        first_inserted_timestamp = DBUtil.first_inserted_values(con, table_name)[0]
        last_inserted_timestamp = DBUtil.last_inserted_values(con, table_name)[0]
        last_checked_timestamp = first_inserted_timestamp

        if (last_inserted_timestamp - first_inserted_timestamp + 1) != rows:
            raise ValueError('DB contains missing or extra rows')

        step = 100000
        for i in range(0, rows, step):
            sql = 'SELECT measured_time, measured_time_str FROM '
            sql += table_name + ' ORDER BY measured_time ASC'
            sql += ' LIMIT ' + str(i) + ', ' + str(step)

            interval = DateTimeUtil.create_interval_str(first_inserted_timestamp + i,
                                                        first_inserted_timestamp + i + step)

            logging.debug('check timestamp between %s' % interval)
            cur.execute(sql)

            res = cur.fetchall()
            for r in res:
                if last_checked_timestamp == r[0]:
                    last_checked_timestamp += 1
                else:
                    raise IndexError('missing or extra row: ' + str(last_checked_timestamp))

    @staticmethod
    def delete_from_time(con, table_name, delay):
        cur = con.cursor()

        maximum_sql = 'SELECT MAX(measured_time) as mm FROM ' + table_name
        cur.execute(maximum_sql)

        res = cur.fetchone()
        if res[0] is None:
            return

        maximum = res[0]
        sql = 'DELETE FROM {0} WHERE measured_time > {1}'.format(table_name, maximum - delay)
        cur.execute(sql)
        con.commit()

    @staticmethod
    def update_attribute(con, table_name, attribute, value, timestamp):
        cur = con.cursor()

        sql = 'UPDATE {0} SET {1} = {2} WHERE `measured_time` = {3}'.format(table_name, attribute, value, timestamp)

        cur.execute(sql)
