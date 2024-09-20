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

import os
import json
import sqlite3

from badges import Badges

from hatsploit.core.db.importer import Importer
from hatsploit.lib.config import Config


class Builder(Config, Badges):
    """ Subclass of hatsploit.core.db module.

    This subclass of hatsploit.core.db module is intended for
    providing tools for building HatSploit databases.
    """

    def check_base_built(self) -> bool:
        """ Check if base databases are built.

        :return bool: True if built else False
        """

        base_dbs = self.db_config['base_dbs']
        db_path = self.path_config['db_path']

        if os.path.exists(db_path + base_dbs['database']):
            return True

        return False

    def rebuild_base(self) -> bool:
        """ Rebuild base databases.

        :return bool: True if success else False
        """

        if self.check_base_build():
            self.build_base()
            return True

        return False

    def build_base(self) -> None:
        """ Build base databases.

        :return None: None
        """

        base_dbs = self.db_config['base_dbs']
        db_path = self.path_config['db_path']

        if not os.path.exists(db_path):
            os.mkdir(db_path)

        self.build_module_database(
            self.path_config['modules_path'],
            db_path + base_dbs['database'],
        )
        self.build_payload_database(
            self.path_config['payloads_path'],
            db_path + base_dbs['database'],
        )
        self.build_encoder_database(
            self.path_config['encoders_path'],
            db_path + base_dbs['database'],
        )
        self.build_plugin_database(
            self.path_config['plugins_path'],
            db_path + base_dbs['database'],
        )

    def build_encoder_database(self, input_path: str, output_path: str) -> None:
        """ Build encoder database from encoder path.

        :param str input_path: path to encoders
        :param str output_path: database path
        :return None: None
        """

        con = sqlite3.connect(output_path)
        cur = con.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS
                encoders(
                    BaseName TEXT PRIMARY KEY,
                    Path TEXT,
                    Name TEXT,
                    Description TEXT,
                    Arch TEXT
                )''')

        data = []

        for dir, _, files in os.walk(os.path.normpath(input_path)):
            for file in files:
                if not file.endswith('.py') or file == '__init__.py':
                    continue

                encoder = os.path.join(dir, file[:-3])

                try:
                    encoder_object = Importer().import_encoder(encoder)
                    data.append((
                        encoder_object.info['Encoder'],
                        encoder,
                        encoder_object.info['Name'],
                        encoder_object.info['Description'],
                        str(encoder_object.info['Arch'])
                    ))

                except Exception:
                    self.print_error(
                        f"Failed to add {encoder} to encoder database!"
                    )

        cur.executemany('''INSERT OR REPLACE INTO encoders
                        VALUES (?, ?, ?, ?, ?)''', data)
        con.commit()

    def build_payload_database(self, input_path: str, output_path: str) -> None:
        """ Build payload database from payload path.

        :param str input_path: path to payloads
        :param str output_path: database path
        :return None: None
        """

        con = sqlite3.connect(output_path)
        cur = con.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS
                payloads(
                    BaseName TEXT PRIMARY KEY,
                    Path TEXT,
                    Category TEXT,
                    Name TEXT,
                    Description TEXT,
                    Arch TEXT,
                    Platform TEXT,
                    Type TEXT
                )''')

        data = []

        for dir, _, files in os.walk(os.path.normpath(input_path)):
            for file in files:
                if not file.endswith('.py') or file == '__init__.py':
                    continue

                payload = os.path.join(dir, file[:-3])

                try:
                    payload_object = Importer().import_payload(payload)
                    data.append((
                        payload_object.info['Payload'],
                        payload,
                        payload_object.info['Category'],
                        payload_object.info['Name'],
                        payload_object.info['Description'],
                        str(payload_object.info['Arch']),
                        str(payload_object.info['Platform']),
                        payload_object.info['Type'],
                    ))

                except Exception:
                    self.print_error(
                        f"Failed to add {payload} to payload database!"
                    )

        cur.executemany('''INSERT OR REPLACE INTO payloads
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', data)
        con.commit()

    def build_module_database(self, input_path: str, output_path: str) -> None:
        """ Build module database from module path.

        :param str input_path: path to modules
        :param str output_path: database path
        :return None: None
        """

        con = sqlite3.connect(output_path)
        cur = con.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS
                modules(
                    BaseName TEXT PRIMARY KEY,
                    Path TEXT,
                    Category TEXT,
                    Name TEXT,
                    Description TEXT,
                    Platform TEXT,
                    DisclosureDate TEXT,
                    jDevices TEXT,
                    jReferences TEXT,
                    jAuthors TEXT,
                    jNotes TEXT,
                    Rank TEXT
                )''')

        data = []

        for dir, _, files in os.walk(os.path.normpath(input_path)):
            for file in files:
                if not file.endswith('.py') or file == '__init__.py':
                    continue

                module = os.path.join(dir, file[:-3])

                try:
                    module_object = Importer().import_module(module)
                    data.append((
                        module_object.info['Module'],
                        module,
                        module_object.info['Category'],
                        module_object.info['Name'],
                        module_object.info['Description'],
                        str(module_object.info['Platform']),
                        module_object.info['DisclosureDate'],
                        json.dumps(module_object.info['Devices']),
                        json.dumps(module_object.info['References']),
                        json.dumps(module_object.info['Authors']),
                        json.dumps(module_object.info['Notes']),
                        module_object.info['Rank'],
                    ))

                except Exception:
                    self.print_error(
                        f"Failed to add {module} to module database!"
                    )

        cur.executemany('''INSERT OR REPLACE INTO modules
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
        con.commit()

    def build_plugin_database(self, input_path: str, output_path: str) -> None:
        """ Build plugin database from plugin path.

        :param str input_path: path to plugins
        :param str output_path: database path
        :return None: None
        """

        con = sqlite3.connect(output_path)
        cur = con.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS
                plugins(
                    BaseName TEXT PRIMARY KEY,
                    Path TEXT,
                    Name TEXT,
                    Description TEXT
                )''')

        data = []

        for dir, _, files in os.walk(os.path.normpath(input_path)):
            for file in files:
                if not file.endswith('.py') or file == '__init__.py':
                    continue

                plugin = os.path.join(dir, file[:-3])

                try:
                    plugin_object = Importer().import_plugin(plugin)
                    data.append((
                        plugin_object.info['Plugin'],
                        plugin,
                        plugin_object.info['Name'],
                        plugin_object.info['Description'],
                    ))

                except Exception:
                    self.print_error(
                        f"Failed to add {plugin} to plugin database!"
                    )

        cur.executemany('''INSERT OR REPLACE INTO plugins
                        VALUES (?, ?, ?, ?)''', data)
        con.commit()
