"""
MIT License

Copyright (c) 2020-2024 EntySec

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sqlite3

from typing import Optional

from hatsploit.core.db.builder import Builder
from hatsploit.core.db.importer import Importer

from hatsploit.lib.config import Config
from hatsploit.lib.storage import STORAGE


class DB(object):
    """ Subclass of hatsploit.core.db module.

    This subclass of hatsploit.core.db module is intended for
    providing tools for working with HatSploit databases.
    """

    def __init__(self, table: str,
                 path: Optional[str] = None) -> None:
        """ Initialize DB connector.

        :param str table: table name
        :param Optional[str] path: path to database
        :return None: None
        """

        self.config = Config()

        self.path = path or (
            self.config.path_config['db_path'] +
            self.config.db_config['base_dbs']['database'])
        self.table = table

        self.conn = STORAGE.get('database_connector')
        self.cursor = STORAGE.get('database_cursor')

        if self.conn and self.cursor:
            return

        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row

        self.cursor = self.conn.cursor()

        STORAGE.set("database_connector", self.conn)
        STORAGE.set("database_cursor", self.cursor)

    def dump(self, criteria: dict = {}) -> list:
        """ Dump database table contents.

        :param dict criteria: criteria
        (key - field name, value - expected value)
        :return list: contents
        """

        query = ''

        if criteria:
            query = ' WHERE '
            query += ' AND '.join([f'{entry}="{str(value)}"' for entry, value in criteria.items()])

        query = self.cursor.execute(f'SELECT * FROM "{self.table}"' + query)
        result = query.fetchall()

        data = {}

        for entry in result:
            row = dict(entry)
            data[row['BaseName']] = row

        return data

    def load(self, criteria: dict = {}) -> dict:
        """ Load all entries matching criteria.

        :param dict criteria: criteria
        (key - field name, value - expected value)
        :return dict: names as keys, objects as values
        """

        data = {}
        query = ''

        if criteria:
            query = ' WHERE '
            query += ' AND '.join([f'{entry}="{str(value)}"' for entry, value in criteria.items()])

        query = self.cursor.execute(f'SELECT BaseName, Path FROM "{self.table}"' + query)
        result = query.fetchall()

        for entry in result:
            row = dict(entry)

            if self.table == 'modules':
                data[row['BaseName']] = Importer.import_module(row['Path'])

            elif self.table == 'payloads':
                data[row['BaseName']] = Importer.import_payload(row['Path'])

            elif self.table == 'encoders':
                data[row['BaseName']] = Importer.import_encoder(row['Path'])

            elif self.table == 'plugins':
                data[row['BaseName']] = Importer.import_plugin(row['Path'])

        return data

    def build(self, path: str) -> None:
        """ Build database table from path.

        :param str path: path to build from
        :return None: None
        :raises RuntimeError: with trailing error message
        """

        if self.table == 'modules':
            Builder().build_module_database(path, self.path)

        elif self.table == 'payloads':
            Builder().build_payload_database(path, self.path)

        elif self.table == 'encoders':
            Builder().build_encoder_database(path, self.path)

        elif self.table == 'plugins':
            Builder().build_plugin_database(path, self.path)

        else:
            raise RuntimeError("Table provided does not support building!")
