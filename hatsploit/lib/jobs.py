"""
MIT License

Copyright (c) 2020-2023 EntySec

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

import ctypes
import threading

from typing import Callable, Any

from hatsploit.lib.storage import LocalStorage


class Jobs(object):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for providing
    tools for working with HatSploit jobs (threads).
    """

    def __init__(self) -> None:
        super().__init__()

        self.local_storage = LocalStorage()

    def get_jobs(self) -> dict:
        """ Get all visible jobs from local storage.

        :return dict: jobs, ids as keys and details as items
        """

        return self.local_storage.get("jobs", {})

    def get_hidden_jobs(self) -> dict:
        """ Get all hidden jobs from local storage.

        :return dict: hidden jobs, ids as keys and details as items
        """

        return self.local_storage.get("hidden_jobs", {})

    def stop_dead(self) -> None:
        """ Stop all dead visible and hidden jobs (inactive threads).

        :return None: None
        """

        jobs = self.get_jobs()

        if jobs:
            for job_id in list(jobs):
                if not jobs[job_id]['Process'].is_alive():
                    self.delete_job(job_id)

        hidden_jobs = self.get_hidden_jobs()

        if hidden_jobs:
            for job_id in list(hidden_jobs):
                if not hidden_jobs[job_id]['Process'].is_alive():
                    self.delete_job(job_id, True)

    def count_jobs(self) -> int:
        """ Count all visible jobs from local storage.

        :return int: number of visible jobs
        """

        return len(self.get_jobs())

    def stop_jobs(self) -> None:
        """ Stop all visible and hidden jobs.

        :return None: None
        """

        jobs = self.get_jobs()

        for job_id in list(jobs):
            self.delete_job(job_id)

        hidden_jobs = self.get_hidden_jobs()

        for job_id in list(hidden_jobs):
            self.delete_job(job_id, True)

    @staticmethod
    def stop_job(job: threading.Thread) -> None:
        """ Stop job thread.

        :param threading.Thread job: job thread
        :return None: None
        :raises RuntimeError: with trailing error message
        """

        if job.is_alive():
            exc = ctypes.py_object(SystemExit)
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(job.ident), exc)

            if res > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(job.ident, None)
                raise RuntimeError("Failed to stop job!")

    @staticmethod
    def start_job(target: Callable[..., Any], args: list = [], kwargs: dict = {}) -> threading.Thread:
        """ Start job thread.

        :param Callable[..., Any] target: function to thread
        :param list args: extra function arguments
        :param dict kwargs: extra job function kwargs
        :return threading.Thread: job thread
        """

        thread = threading.Thread(target=target, args=args, kwargs=kwargs)
        thread.setDaemon(True)
        thread.start()

        return thread

    def delete_job(self, job_id: int, hidden: bool = False) -> None:
        """ Delete specific job by id.

        :param int job_id: job id
        :param bool hidden: True if job hidden else False
        :return None: None
        :raises RuntimeError: with trailing error message
        """

        jobs_var = "jobs"

        if hidden:
            jobs_var = "hidden_jobs"

        if self.local_storage.get(jobs_var):
            job_id = int(job_id)

            if job_id in list(self.local_storage.get(jobs_var)):
                self.stop_job(self.local_storage.get(jobs_var)[job_id]['Process'])
                self.local_storage.delete_element(jobs_var, job_id)

            else:
                raise RuntimeError("Invalid job given!")

        else:
            raise RuntimeError("Invalid job given!")

    def create_job(self, job: str, module: str, target: Callable[..., Any],
                   args: list = [], kwargs: dict = {}, hidden: bool = False) -> None:
        """ Create and start job.

        :param str job: job name
        :param str module: name of module you want to reserve job for,
        empty if no module
        :param Callable[..., Any] target: job function
        :param list args: extra job function arguments
        :param dict kwargs: extra job function kwargs
        :param bool hidden: True if you want to create hidden job
        :return None: None
        """

        jobs_var = "jobs"

        if hidden:
            jobs_var = "hidden_jobs"

        if not self.local_storage.get(jobs_var):
            self.local_storage.set(jobs_var, {})

        job_id = len(self.local_storage.get(jobs_var))
        job_thread = self.start_job(target, args, kwargs)

        job_data = {
            job_id: {
                'Name': job,
                'Module': module,
                'Process': job_thread
            }
        }

        self.local_storage.update(jobs_var, job_data)
