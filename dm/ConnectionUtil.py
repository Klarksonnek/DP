"""

"""
import configparser
import mysql.connector
import os

__author__ = ''
__email__ = ''


class ConnectionUtil:
    MAX_TESTABLE_EVENTS = 100

    @staticmethod
    def create_con(config_file='/etc/dp/config.ini'):
        if ConnectionUtil.is_testable_system():
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

    @staticmethod
    def rapid_miner(config_file='/etc/dp/config.ini'):
        config = configparser.ConfigParser()
        config.read(config_file)

        return config['rapidminer']

    @staticmethod
    def is_testable_system():
        # example travis hostname: travis-job-d072bd30-f722-4d10-*
        return 'travis' in os.uname()[1]
