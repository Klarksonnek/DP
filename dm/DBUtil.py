from mysql.connector.errors import Error


class DBUtil:
    @staticmethod
    def create_table(conn, table_name):
        sql = """
            CREATE TABLE IF NOT EXISTS """ + table_name + """ (
            measured_time int,
            measured_time_str timestamp,
            owner VARCHAR(8),
            open_close boolean,
            pressure_in_hpa float,
            temperature_in_celsius float,
            temperature_in2_celsius float,
            temperature_out_celsius float,
            rh_in_percentage float,
            rh_in2_percentage float,
            rh_in_absolute_g_m3 float,
            rh_in2_absolute_g_m3 float,
            rh_in_specific_g_kg float,
            rh_in2_specific_g_kg float,
            rh_out_percentage float,
            rh_out_absolute_g_m3 float,
            rh_out_specific_g_kg float,
            co2_in_ppm float,
            co2_in_g_m3 float,
            PRIMARY KEY (measured_time,owner)
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
            'owner',
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
            'co2_in_ppm',
            'co2_in_g_m3'
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
        except Error:
            return

        if enable_commit:
            conn.commit()

    @staticmethod
    def last_inserted_open_close_state(conn, table_name, owner):
        return DBUtil.last_inserted_values(conn, table_name, owner)[3]

    @staticmethod
    def rows_count(conn, table_name):
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM ' + table_name)
        return cur.fetchall()[0][0]

    @staticmethod
    def last_inserted_values(conn, table_name, owner):
        cur = conn.cursor()

        sql = """
            select * from `""" + table_name + """` 
            where measured_time = (SELECT MAX(measured_time) as mm FROM """ + table_name + """
            WHERE owner = '""" + owner + """') and owner = '""" + owner + '\''

        cur.execute(sql)

        res = cur.fetchall()
        if not res:
            return None

        return res[0]
