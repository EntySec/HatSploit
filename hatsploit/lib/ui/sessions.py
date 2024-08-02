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

from hatsploit.lib.core.session import Session
from hatsploit.lib.storage import GlobalStorage
from hatsploit.lib.storage import STORAGE


class Sessions(Badges):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for providing
    tools for working with HatSploit sessions.
    """

    storage_path = Config().path_config['storage_path']
    global_storage = GlobalStorage(storage_path)

    @staticmethod
    def get_sessions() -> dict:
        """ Get all opened sessions.

        :return dict: sessions, session ids as keys and
        session details as items
        """

        return STORAGE.get("sessions", {})

    def close_dead(self) -> None:
        """ Close all dead sessions.

        :return None: None
        """

        sessions = self.get_sessions()

        if sessions:
            for session in list(sessions):
                if not sessions[session].heartbeat():
                    self.print_warning(f"Session {str(session)} is dead (no heartbeat).")
                    self.close_session(session)

    def add_session(self, session: Session) -> int:
        """ Add session to local storage.

        :param Session session: session object
        :return int: session id
        """

        if not self.get_sessions():
            STORAGE.set("sessions", {})

        session_id = 0
        while session_id in self.get_sessions() or \
                session_id < len(self.get_sessions()):
            session_id += 1

        STORAGE.update("sessions", {session_id: session})
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

                if platform and session.info['Platform'] != platform:
                    return False

                if arch and session.info['Arch'] != arch:
                    return False

                if type and session.info['Type'] != type:
                    return False

                return True
        return False

    @staticmethod
    def get_auto_interaction() -> bool:
        """ Check if auto-interaction allowed.

        :return bool: True if allowed else False
        """

        return STORAGE.get("auto_interaction", False)

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
            self.print_process(f"Interacting with session {str(session_id)}...%newline")
            sessions[int(session_id)].interact()

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
            return sessions[int(session_id)].download(remote_file, local_path)

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
            return sessions[int(session_id)].upload(local_file, remote_path)

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
                sessions[int(session_id)].close()
                del sessions[int(session_id)]

                STORAGE.update("sessions", sessions)

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
                    sessions[session].close()
                    del sessions[session]

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
            return sessions[int(session_id)]

        raise RuntimeError("Invalid session given!")
