#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2021 EntySec
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import sqlite3


class DBTools:
    @staticmethod
    def parse_safari_history(database):
        db = sqlite3.connect(database)
        db.row_factory = sqlite3.Row

        cursor = db.cursor()
        cursor.execute('''SELECT 
                history_item as lookup_id,
                title,
                load_successful as open_successfull,
                datetime(visit_time + 978307200, 'unixepoch', 'localtime') as 'date'
            FROM history_visits''')

        result_temp_dict = list(map(dict,cursor.fetchall()))
        for item in result_temp_dict:
            cursor.execute( '''SELECT 
                    url,
                    domain_expansion,
                    visit_count
                FROM history_items
                WHERE id = {item_id}'''.format(item_id=item["lookup_id"]))

            current_row_dict = list(map(dict,cursor.fetchall()))
            item["details"] = current_row_dict[0]

            del item["lookup_id"]
        return result_temp_dict
