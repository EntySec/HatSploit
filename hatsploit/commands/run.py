#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.jobs import Jobs
from hatsploit.lib.storage import LocalStorage
from hatsploit.lib.command import Command
from hatsploit.lib.modules import Modules
from hatsploit.lib.payloads import Payloads


class HatSploitCommand(Command):
    payloads = Payloads()
    local_storage = LocalStorage()
    modules = Modules()
    jobs = Jobs()

    usage = ""
    usage += "run [option]\n\n"
    usage += "  -h, --help  Show this help message.\n"
    usage += "  -j, --job   Run current module as a background job.\n"

    details = {
        'Category': "modules",
        'Name': "run",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Run current module.",
        'Usage': usage,
        'MinArgs': 0
    }

    def entry_to_module(self, argc, argv, current_module):
        if argc > 0:
            if argv[0] in ['-j', '--job']:
                self.output_process("Running module as a background job...")
                job_id = self.jobs.create_job(current_module.details['Name'], current_module.details['Module'],
                                              current_module.run)
                self.output_information("Module started as a background job " + str(job_id) + ".")
                return
        current_module.run()

    def run(self, argc, argv):
        if argc > 0:
            if argv[0] in ['-h', '--help']:
                self.output_usage(self.details['Usage'])
                return

        if self.modules.check_current_module():
            current_module = self.modules.get_current_module_object()
            current_payload = self.payloads.get_current_payload()
            missed = ""
            if hasattr(current_module, "options"):
                for option in current_module.options.keys():
                    current_option = current_module.options[option]
                    if not current_option['Value'] and current_option['Value'] != 0 and current_option['Required']:
                        missed += option + ', '
            if current_payload:
                if hasattr(current_payload, "options"):
                    for option in current_payload.options.keys():
                        current_option = current_payload.options[option]
                        if not current_option['Value'] and current_option['Value'] != 0 and current_option['Required']:
                            missed += option + ', '
            if len(missed) > 0:
                self.output_error(f"These options failed to validate: {missed[:-2]}!")
            else:
                try:
                    if current_payload:
                        payload_name = current_module.payload['Value']

                        payload_data = current_payload.run()
                        payload, args, session = None, None, None
                        
                        if isinstance(payload_data, tuple):
                            if len(payload_data) == 2:
                                payload, args = payload_data[0], payload_data[1]
                            elif len(payload_data) == 3:
                                payload, args, session = payload_data[0], payload_data[1], payload_data[2]
                        else:
                            payload = payload_data

                        current_module.payload['Category'] = current_payload.details['Category']
                        current_module.payload['Platform'] = current_payload.details['Platform']
                        current_module.payload['Type'] = current_payload.details['Type']

                        current_module.payload['Payload'] = payload
                        current_module.payload['Args'] = args
                        current_module.payload['Session'] = session

                    self.entry_to_module(argc, argv, current_module)
                except Exception as e:
                    self.output_error("An error occurred in module: " + str(e) + "!")
        else:
            self.output_warning("No module selected.")
