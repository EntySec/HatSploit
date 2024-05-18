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

from typing import Optional
from badges import Badges

from hatsploit.lib.config import Config

from hatsploit.lib.session import Session
from hatsploit.lib.storage import GlobalStorage
from hatsploit.lib.storage import LocalStorage


class Sessions(object):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for providing
    tools for working with HatSploit sessions.
    """

    def __init__(self) -> None:
        super().__init__()

        self.badges = Badges()
        self.config = Config()

        self.storage_path = self.config.path_config['storage_path']

        self.global_storage = GlobalStorage(self.storage_path)
        self.local_storage = LocalStorage()

    def get_sessions(self) -> dict:
        """ Get all opened sessions.

        :return dict: sessions, session ids as keys and
        session details as items
        """

        return self.local_storage.get("sessions", {})

    def close_dead(self) -> None:
        """ Close all dead sessions.

        :return None: None
        """

        sessions = self.get_sessions()

        if sessions:
            for session in list(sessions):
                if not sessions[session]['Object'].heartbeat():
                    self.badges.print_warning(f"Session {str(session)} is dead (no heartbeat).")
                    self.close_session(session)

    def add_session(self, platform: str, arch: str, type: str,
                    host: str, port: int, session: Session) -> int:
        """ Add session to local storage.

        :param str platform: session platform
        :param str arch: session architecture
        :param str type: session type
        :param str host: session host
        :param int port: session port
        :param Session session: session object
        """

        if not self.get_sessions():
            self.local_storage.set("sessions", {})

        session_id = 0
        while (session_id in self.get_sessions() or
               session_id < len(self.get_sessions())):
            session_id += 1

        sessions = {
            session_id: {
                'Platform': platform,
                'Arch': arch,
                'Type': type,
                'Host': host,
                'Port': port,
                'Object': session
            }
        }

        self.local_storage.update("sessions", sessions)
        return session_id

    def check_exist(self, session_id: int, platform: Optional[str] = None,
                    arch: Optional[str] = None, type: Optional[str] = None) -> bool:
        """ Check if session exists in local storage.

        :param int session_id: session id
        :param Optional[str] platform: session platform
        :param Optional[str] arch: session architecture
        :param Optional[str] type: session type
        :return bool: True if exists else False
        """

        sessions = self.get_sessions()

        if sessions:
            if int(session_id) in sessions:
                session = sessions[int(session_id)]

                if platform and session['Platform'] != platform:
                    return False

                if arch and session['Arch'] != arch:
                    return False

                if type and session['Type'] != type:
                    return False

                return True
        return False

    def get_auto_interaction(self) -> bool:
        """ Check if auto-interaction allowed.

        :return bool: True if allowed else False
        """

        return self.local_storage.get("auto_interaction", False)

    def enable_auto_interaction(self) -> None:
        """ Enable automatic interaction with session
        right after it was opened.

        :return None: None
        """

        self.global_storage.set("auto_interaction", True)
        self.global_storage.set_all()

    def disable_auto_interaction(self) -> None:
        """ Disable automatic interaction with session
        right after it was opened.

        :return None: None
        """

        self.global_storage.set("auto_interaction", False)
        self.global_storage.set_all()

    def interact_with_session(self, session_id: int) -> None:
        """ Interact with specific session.

        :param int session_id: session id
        :return None: None
        :raises RuntimeError: with trailing error message
        """

        sessions = self.get_sessions()

        if self.check_exist(session_id):
            self.badges.print_process(f"Interacting with session {str(session_id)}...%newline")
            sessions[int(session_id)]['Object'].interact()

        else:
            raise RuntimeError("Invalid session given!")

    def session_download(self, session_id: int, remote_file: str, local_path: str) -> bool:
        """ Download file from session.

        :param int session_id: session id
        :param str remote_file: remote file to download
        :param str local_path: local path to save downloaded file
        :return bool: True if success else False
        :raises RuntimeError: with trailing error message
        """

        sessions = self.get_sessions()

        if self.check_exist(session_id):
            return sessions[int(session_id)]['Object'].download(remote_file, local_path)

        raise RuntimeError("Invalid session given!")

    def session_upload(self, session_id: int, local_file: str, remote_path: str) -> bool:
        """ Upload file to session.

        :param int session_id: session id
        :param str local_file: local file to upload
        :param str remote_path: remote path to save uploaded file
        :return bool: True if success else False
        :raises RuntimeError: with trailing error message
        """

        sessions = self.get_sessions()

        if self.check_exist(session_id):
            return sessions[int(session_id)]['Object'].upload(local_file, remote_path)

        raise RuntimeError("Invalid session given!")

    def close_session(self, session_id: int) -> None:
        """ Close specific session.

        :param int session_id: session id
        :return None: None
        :raises RuntimeError: with trailing error message
        """

        sessions = self.get_sessions()

        if self.check_exist(session_id):
            try:
                sessions[int(session_id)]['Object'].close()
                del sessions[int(session_id)]

                self.local_storage.update("sessions", sessions)

            except Exception:
                raise RuntimeError("Failed to close session!")

        else:
            raise RuntimeError("Invalid session given!")

    def close_sessions(self) -> None:
        """ Close all sessions.

        :return None: None
        :raises RuntimeError: with trailing error message
        """

        sessions = self.get_sessions()

        if sessions:
            for session in list(sessions):
                try:
                    sessions[session]['Object'].close()
                    del sessions[session]

                    self.local_storage.update("sessions", sessions)

                except Exception:
                    raise RuntimeError("Failed to close session!")

    def get_session(self, session_id: int, platform: Optional[str] = None,
                    arch: Optional[str] = None, type: Optional[str] = None) -> Session:
        """ Get session object.

        :param int session_id: session id
        :param Optional[str] platform: session platform
        :param Optional[str] arch: session architecture
        :param Optional[str] type: session type
        :return Session: session object
        :raises RuntimeError: with trailing error message
        """

        sessions = self.get_sessions()

        if self.check_exist(session_id, platform, arch, type):
            return sessions[int(session_id)]['Object']

        raise RuntimeError("Invalid session given!")
