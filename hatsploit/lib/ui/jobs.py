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
import time
import ctypes
import threading

from typing import (
    Callable,
    Any,
    Union,
    Optional
)

from hatsploit.lib.storage import STORAGE
from hatsploit.lib.runtime import Runtime


class Job(threading.Thread):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is a representation
    of a job instance used to store job related information and
    job object.
    """

    def __init__(self, *args, **kwargs) -> None:
        threading.Thread.__init__(self, *args, **kwargs)

        self._return = None
        self._exit_handle = None
        self._exit_args = []
        self._exit_kwargs = {}

        self.daemon = True
        self.visible = True
        self.module = None
        self.name = None
        self.pass_job = False

    def set_exit(self, target: Callable[..., Any], args: list = [],
                 kwargs: dict = {}) -> None:
        """ Set exit handle.

        :param Callable[..., Any] target: exit handle callback
        :param list args: target args
        :param dict kwargs: target kwargs
        :return None: None
        """

        self._exit_handle = target
        self._exit_args = args
        self._exit_kwargs = kwargs

    def run(self) -> None:
        """ Internal thread run method.

        :return None: None
        """

        if self.pass_job:
            self._kwargs['job'] = self

        if self._target is not None:
            self._return = Runtime().catch(
                target=self._target,
                args=self._args,
                kwargs=self._kwargs
            )

    def join(self, *args) -> Any:
        """ Flush job and wait for result.

        :return Any: thread return value
        """

        threading.Thread.join(self, *args)
        return self._return

    def shutdown(self) -> None:
        """ Terminate current job.

        :return None: None
        """

        if self._exit_handle:
            self._exit_handle(*self._exit_args, **self._exit_kwargs)

        exc = ctypes.py_object(Exception)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self.ident), exc)

        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(self.ident, None)
            raise RuntimeError("Failed to shutdown job!")


class Jobs(object):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for providing
    tools for working with HatSploit jobs (threads).
    """

    @staticmethod
    def get_jobs() -> dict:
        """ Get all jobs from local storage.

        :return dict: jobs, ids as keys and details as items
        """

        return STORAGE.get("jobs", {})

    def get_job(self, job_id: int) -> Union[Job, None]:
        """ Get job object.

        :param int job_id: job id
        :return Union[Job, None]: job object or None
        """

        return self.get_jobs().get(job_id, None)

    def stop_dead(self) -> None:
        """ Stop all dead jobs (inactive threads).

        :return None: None
        """

        jobs = self.get_jobs()

        if not jobs:
            return

        for job_id in list(jobs):
            if jobs[job_id].is_alive():
                continue

            STORAGE.delete_element('jobs', job_id)

    def count_jobs(self) -> int:
        """ Count all visible jobs from local storage.

        :return int: number of visible jobs
        """

        return len(self.get_jobs())

    def stop_job(self, job_id: int) -> None:
        """ Stop job object and delete it from the pool.

        :param int job_id: job id
        :return None: None
        :raises RuntimeError: with trailing error message
        """

        job = self.get_job(job_id)

        if not job:
            raise RuntimeError("Invalid job ID given!")

        job.shutdown()
        job.join()

        STORAGE.delete_element('jobs', job_id)

    def stop_jobs(self, module: Optional[str] = None) -> None:
        """ Stop all jobs.

        :param Optional[str] module: kill jobs that belong to
        specific module
        :return None: None
        """

        jobs = self.get_jobs()

        for _, job in jobs.items():
            if module and job.module != module:
                continue

            job.shutdown()
            job.join()

        self.stop_dead()

    def create_job(self, job: str, module: str, target: Callable[..., Any],
                   args: list = [], kwargs: dict = {}, timeout: Optional[int] = None,
                   bind_to_module: bool = False, pass_job: bool = False) -> int:
        """ Create and start job.

        :param str job: job name
        :param str module: name of module you want to reserve job for,
        empty if no module
        :param Callable[..., Any] target: job function
        :param list args: extra job function arguments
        :param dict kwargs: extra job function kwargs
        :param Optional[int] timeout: time to wait after job was created
        :param bool bind_to_module: bind to module so it can be freed if module
        is terminated or completed
        :param bool pass_job: pass job object as a an argument `job`
        :return int: job ID
        """

        if not self.get_jobs():
            STORAGE.set('jobs', {})

        job_id = 0
        while job_id in self.get_jobs() or \
                job_id < len(self.get_jobs()):
            job_id += 1

        if bind_to_module:
            module_object = STORAGE.get("current_module")

            if module_object:
                module = module_object[-1].info['Module']

        job_thread = Job(target=target, args=args, kwargs=kwargs)
        job_thread.module = module
        job_thread.name = job
        job_thread.pass_job = pass_job
        job_thread.start()

        STORAGE.update('jobs', {job_id: job_thread})
        if timeout:
            time.sleep(timeout)

        return job_id
