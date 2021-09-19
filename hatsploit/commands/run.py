#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from copy import deepcopy
from hatvenom import HatVenom

from hatsploit.lib.jobs import Jobs
from hatsploit.lib.storage import LocalStorage
from hatsploit.lib.command import Command
from hatsploit.lib.modules import Modules
from hatsploit.lib.payloads import Payloads


class HatSploitCommand(Command, HatVenom):
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
        values = list()

        for option in current_module.options:
            opt = current_module.options[option]
            val = str(opt['Value'])

            if val.startswith('file:') and len(val) > 5:
                file = val[5:]

                with open(file, 'r') as f:
                    vals = f.read().strip()
                    values.append(vals.split('\n'))

        if not values:
            if argc > 0:
                if argv[0] in ['-j', '--job']:
                    self.print_process("Running module as a background job...")
                    job_id = self.jobs.create_job(current_module.details['Name'], current_module.details['Module'],
                                                    current_module.run)
                    self.print_information("Module started as a background job " + str(job_id) + ".")
                    return

            current_module.run()
            return

        if not all(len(value) == len(values[0]) for value in values):
            self.print_error("All files should contain equal number of values!")
            return

        save = deepcopy(current_module.options)
        for i in range(0, len(values[0])):
            count = 0

            for option in current_module.options:
                opt = current_module.options[option]
                val = str(opt['Value'])

                if val.startswith('file:') and len(val) > 5:
                    current_module.options[option]['Value'] = values[count][i]
                    count += 1

            if argc > 0:
                if argv[0] in ['-j', '--job']:
                    self.print_process("Running module as a background job...")
                    job_id = self.jobs.create_job(current_module.details['Name'], current_module.details['Module'],
                                                    current_module.run)
                    self.print_information("Module started as a background job " + str(job_id) + ".")
                    return

            try:
                current_module.run()
            except (KeyboardInterrupt, EOFError):
                pass

            current_module.options = save
            save = deepcopy(current_module.options)

    def run(self, argc, argv):
        if argc > 0:
            if argv[0] in ['-h', '--help']:
                self.print_usage(self.details['Usage'])
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
                self.print_error(f"These options failed to validate: {missed[:-2]}!")
            else:
                try:
                    if current_payload:
                        payload_name = current_module.payload['Value']
                        payload_data = current_payload.run()

                        if current_payload.details['Platform'] in ['macos', 'iphoneos']:
                            executable = 'macho'
                        elif current_payload.details['Platform'] in ['windows']:
                            executable = 'pe'
                        else:
                            executable = 'elf'

                        if isinstance(payload_data, tuple):
                            raw = self.generate('raw', 'generic', payload_data[0], payload_data[1])
                            payload = self.generate(executable if current_payload.details['Architecture'] != 'generic' else 'raw',
                                                    current_payload.details['Architecture'],
                                                    payload_data[0], payload_data[1])
                        else:
                            raw = self.generate('raw', 'generic', payload_data)
                            payload = self.generate(executable if current_payload.details['Architecture'] != 'generic' else 'raw',
                                                    current_payload.details['Architecture'],
                                                    payload_data)

                        current_module.payload['Category'] = current_payload.details['Category']
                        current_module.payload['Platform'] = current_payload.details['Platform']
                        current_module.payload['Type'] = current_payload.details['Type']

                        current_module.payload['Raw'] = raw
                        current_module.payload['Payload'] = payload
                        current_module.payload['Args'] = None
                        current_module.payload['Session'] = None

                    self.entry_to_module(argc, argv, current_module)
                except Exception as e:
                    self.print_error("An error occurred in module: " + str(e) + "!")
        else:
            self.print_warning("No module selected.")
