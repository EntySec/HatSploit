#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2022 EntySec
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
    def parse_addressbook(database):
        db = sqlite3.connect(database)
        db.row_factory = sqlite3.Row
        
        cursor = db.cursor()
        cursor.execute('''SELECT
                c0First,
                c16Phone
            FROM ABPersonFullTextSearch_content''')

        return list(map(dict,cursor.fetchall()))

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

    @staticmethod
    def parse_safari_bookmarks(database):
        db = sqlite3.connect(database)
        db.row_factory = sqlite3.Row

        cursor = db.cursor()
        cursor.execute('''SELECT
                title,
                url
            FROM bookmarks
            WHERE num_children = 0
            AND url <> "" ''')

        return list(map(dict,cursor.fetchall()))

    @staticmethod
    def parse_whatsapp_chat(database, partner):
        partner = partner.replace(" ", "").replace("+", "")
        result_arr = {
            "partner": "",
            "partner_id": partner,
            "success": True,
            "data": []
        }

        db = sqlite3.connect(database)
        db.row_factory = sqlite3.Row

        cursor = db.cursor()
        cursor.execute('''SELECT
                Z_PK as 'msg_id_pk',
                ZTEXT as "text",
                ZISFROMME as "is_from_me",
                ZMESSAGETYPE as "message_type",
                ZMESSAGEDATE as "timestamp"
            FROM ZWAMESSAGE
            WHERE ZFROMJID like "%{partner}%"
            OR ZTOJID like "%{partner}%"
        '''.format(partner=partner))

        all_messages_dict = list(map(dict, cursor.fetchall()))
        if len(all_messages_dict) > 0:
            for message in all_messages_dict:
                if message["text"] is None:
                    message["text"] = "<unknown message type>"

                message["is_from_me"] = True if message["is_from_me"] == 1 else False
                if message["message_type"] == 0:
                    message["message_type"] = "text"
                elif message["message_type"] == 7:
                    message["message_type"] = "link"
                elif message["message_type"] == 8:
                    message["message_type"] = "file"

                result_arr["data"].append(message)
        cursor.execute('''SELECT
            ZPARTNERNAME
            FROM ZWACHATSESSION
            WHERE ZCONTACTJID like "%{partner}%"
        '''.format(partner=partner))

        try:
            result_arr["partner"] = [str(username[0]) for username in cursor.fetchall()][0]
        except IndexError:
            result_arr["success"] = False
        return result_arr

    @staticmethod
    def parse_sms_chat(database, partner, imessage=True):
        partner = partner.replace(" ", "")
        db = sqlite3.connect(sms_db)
        result_arr = {
            "protocol": "{}".format('iMessage' if imessage == True else 'SMS'),
            "partner": partner,
            "success": True,
            "data": []
        }

        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute('''SELECT
                ROWID
            FROM chat
            WHERE guid LIKE '{protocol};%;{partner}' 
            '''.format(partner=partner, protocol=('iMessage' if imessage == True else 'SMS')))

        try:
            rowid_chat = list(map(dict,cursor.fetchall()))[0]["ROWID"]
        except IndexError:
            result_arr["success"] = False
            return result_arr

        cursor.execute('''SELECT
                message_id
            FROM chat_message_join
            WHERE chat_id = {row_id}
            '''.format(row_id=rowid_chat))

        message_id_arr = [int(item[0]) for item  in list(map(list, cursor.fetchall()))]
        for message_id in message_id_arr:
            cursor.execute('''SELECT
                    ROWID as 'message_id',
                    text,
                    date as 'timestamp',
                    is_from_me
                FROM message
                WHERE ROWID = {message_id}
                AND text <> ""
                ORDER BY date
                '''.format(message_id=message_id))
            message_element_arr = list(map(dict, cursor.fetchall()))[0]
            result_arr["data"].append(message_element_arr)

        return result_arr

    @staticmethod
    def parse_voicemail_chat(database):
        result_arr = {
            "total": 0,
            "data": []
        }

        db = sqlite3.connect(database)
        db.row_factory = sqlite3.Row

        cursor = db.cursor()
        cursor.execute('''SELECT
                sender,
                receiver,
                duration,
                date as 'timestamp'
            FROM voicemail
            ORDER BY date''')

        result_arr["data"] = list(map(dict, cursor.fetchall()))
        result_arr["total"] = len(result_arr["data"])

        return result_arr
