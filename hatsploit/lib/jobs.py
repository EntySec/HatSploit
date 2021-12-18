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

import ctypes
import os
import sys
import threading

from hatsploit.core.base.exceptions import Exceptions
from hatsploit.core.cli.badges import Badges
from hatsploit.core.cli.tables import Tables
from hatsploit.lib.modules import Modules
from hatsploit.lib.storage import LocalStorage


class Jobs:
    exceptions = Exceptions()
    tables = Tables()
    badges = Badges()
    local_storage = LocalStorage()
    modules = Modules()

    job_process = None

    def stop_dead(self):
        jobs = self.local_storage.get("jobs")
        if jobs:
            for job_id in list(jobs):
                if not jobs[job_id]['job_process'].is_alive():
                    self.delete_job(job_id)

        hidden_jobs = self.local_storage.get("hidden_jobs")
        if hidden_jobs:
            for job_id in list(hidden_jobs):
                if not hidden_jobs[job_id]['job_process'].is_alive():
                    self.delete_job(job_id, True)

    def count_jobs(self):
        jobs = self.local_storage.get("jobs")
        if jobs:
            return len(jobs)
        return 0

    def exit_jobs(self):
        if not self.local_storage.get("jobs"):
            if self.local_storage.get("hidden_jobs"):
                self.stop_all_jobs()
            return True

        self.badges.print_warning("You have some running jobs.")
        if self.badges.input_question("Exit anyway? [y/N] ")[0].lower() in ['yes', 'y']:
            self.badges.print_process("Stopping all jobs...")
            self.stop_all_jobs()
            return True
        return False

    def stop_all_jobs(self):
        jobs = self.local_storage.get("jobs")
        if jobs:
            for job_id in list(jobs):
                self.delete_job(job_id)

        hidden_jobs = self.local_storage.get("hidden_jobs")
        if hidden_jobs:
            for job_id in list(hidden_jobs):
                self.delete_job(job_id, True)

    def stop_job(self, job):
        if job.is_alive():
            exc = ctypes.py_object(SystemExit)
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(job.ident), exc)
            if res == 0:
                raise self.exceptions.GlobalException
            if res > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(job.ident, None)
                raise self.exceptions.GlobalException

    def start_job(self, job_function, job_arguments):
        self.job_process = threading.Thread(target=job_function, args=job_arguments)
        self.job_process.setDaemon(True)
        self.job_process.start()

    def delete_job(self, job_id, hidden=False):
        jobs_var = "jobs"
        if hidden:
            jobs_var = "hidden_jobs"

        if self.local_storage.get(jobs_var):
            job_id = int(job_id)
            if job_id in list(self.local_storage.get(jobs_var)):
                try:
                    self.stop_job(self.local_storage.get(jobs_var)[job_id]['job_process'])
                    self.local_storage.delete_element(jobs_var, job_id)
                except Exception:
                    self.badges.print_error("Failed to stop job!")
            else:
                self.badges.print_error("Invalid job given!")
        else:
            self.badges.print_error("Invalid job given!")

    def create_job(self, job_name, module_name, job_function, job_arguments=[], hidden=False):
        jobs_var = "jobs"
        if hidden:
            jobs_var = "hidden_jobs"

        self.start_job(job_function, job_arguments)
        if not self.local_storage.get(jobs_var):
            self.local_storage.set(jobs_var, {})
        job_id = len(self.local_storage.get(jobs_var))

        job_data = {
            job_id: {
                'job_name': job_name,
                'module_name': module_name,
                'job_process': self.job_process
            }
        }
        self.local_storage.update(jobs_var, job_data)
