import configparser
import os
import mysql.connector


class ConnectionUtil:
    @staticmethod
    def create_con(config_file='/etc/dp/config.ini'):
        # example travis hostname: travis-job-d072bd30-f722-4d10-*
        hostname = os.uname()[1]
        if 'travis' in hostname:
            return mysql.connector.connect(
                host='localhost',
                user='root',
                passwd='',
                database='demo'
            )

        config = configparser.ConfigParser()
        config.read(config_file)

        return mysql.connector.connect(
            host=config['db']['host'],
            user=config['db']['user'],
            passwd=config['db']['passwd'],
            database=config['db']['database']
        )

    @staticmethod
    def api_key(server_name, config_file='/etc/dp/config.ini'):
        config = configparser.ConfigParser()
        config.read(config_file)

        return config[server_name]['api.key']
