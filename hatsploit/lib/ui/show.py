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
from textwrap import dedent, fill

from badges import Badges, Tables

from hatsploit.lib.ui.modules import Modules
from hatsploit.lib.ui.payloads import Payloads
from hatsploit.lib.ui.plugins import Plugins
from hatsploit.lib.ui.sessions import Sessions
from hatsploit.lib.ui.encoders import Encoders
from hatsploit.lib.ui.jobs import Jobs

from hatsploit.lib.loot import Loot
from hatsploit.lib.core.module import Module
from hatsploit.lib.storage import STORAGE


class Show(Badges, Tables):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for providing
    tools for showing different things.
    """

    jobs = Jobs()
    loot = Loot()

    modules = Modules()
    payloads = Payloads()
    plugins = Plugins()
    encoders = Encoders()
    sessions = Sessions()

    def show_jobs(self, jobs: dict) -> None:
        """ Show active jobs.

        :param dict jobs: dictionary of jobs, where job IDs are keys
        and job objects are items
        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        if not jobs:
            raise RuntimeWarning("No running jobs available.")

        data = []
        headers = ("ID", "Name", "Module")

        for job_id, job in jobs.items():
            data.append(
                (job_id, job.name, job.module)
            )

        self.print_table("Active Jobs", headers, *data)

    def show_sessions(self, sessions: dict) -> None:
        """ Show opened sessions.

        :param dict sessions: sessions dictionary, where session ID is a key
        and session data is item
        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        if not sessions:
            raise RuntimeWarning("No opened sessions available.")

        data = []
        headers = ("ID", "Platform", "Arch", "Type", "Host", "Port")

        for session_id, session in sessions.items():
            data.append(
                (session_id, session.info['Platform'], session.info['Arch'],
                 session.info['Type'], session.info['Host'], session.info['Port'])
            )

        self.print_table("Opened Sessions", headers, *data)

    def show_loot(self, loot: list) -> None:
        """ Show collected loot.

        :param list loot: loot array
        (array of tuples containing loot information)
        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        if not loot:
            raise RuntimeWarning("No loot collected yet.")

        headers = ("Loot", "Path", "Time")
        self.print_table("Collected Loot", headers, *loot)

    def show_loaded_plugins(self, plugins: dict) -> None:
        """ Show loaded plugins.

        :param dict plugins: dictionary of plugins, where plugin name is a key
        and plugin object is an item
        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        headers = ("Number", "Plugin", "Name")
        shorts = {}
        data = []
        number = 0

        for plugin in sorted(plugins):
            data.append(
                (number, plugin, plugins[plugin].info['Name'])
            )

            shorts.update({
                number: plugin
            })
            number += 1

        if not shorts:
            raise RuntimeWarning("No plugins available.")

        self.print_table(f"Loaded Plugins", headers, *data)
        STORAGE.set("plugin_shorts", shorts)

    def show_plugins(self, plugins: dict) -> None:
        """ Show plugins.

        :param dict plugins: dictionary of plugins, where plugin name is a key
        and plugin data is an item
        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        headers = ("Number", "Plugin", "Name")
        shorts = {}
        number = 0
        data = []

        for plugin in sorted(plugins):
            plugin = plugins[plugin]

            data.append(
                (number, plugin['BaseName'], plugin['Name'])
            )

            shorts.update({
                number: plugin['BaseName']
            })

            number += 1

        self.print_table(f"Plugins", headers, *data)

        if not shorts:
            raise RuntimeWarning("No plugins available.")

        STORAGE.set("plugin_shorts", shorts)

    def show_encoders(self, encoders: dict) -> None:
        """ Show encoders.

        :param dict encoders: dictionary of encoders, where encoder name is a key
        and encoder data is an item
        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        headers = ("Number", "Encoder", "Name")
        shorts = {}
        number = 0
        data = []

        for encoder in sorted(encoders):
            encoder = encoders[encoder]

            data.append(
                (number, encoder['BaseName'], encoder['Name'])
            )

            shorts.update({
                number: encoder['BaseName']
            })

            number += 1

        self.print_table(f"Encoders", headers, *data)

        if not shorts:
            raise RuntimeWarning("No encoders available.")

        STORAGE.set("encoder_shorts", shorts)

    def show_modules(self, modules: dict, category: Optional[str] = None) -> None:
        """ Show modules by category.

        :param dict modules: modules dictionary, module name as key and
        module data as item
        :param Optional[str] category: category
        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        headers = ("Number", "Category", "Module", "Rank", "Name")
        shorts = {}
        number = 0
        data = []

        for module in sorted(modules):
            module = modules[module]

            if not category:
                data.append(
                    (number, module['Category'], module['BaseName'],
                     module['Rank'], module['Name'])
                )

                shorts.update(
                    {number: module['BaseName']}
                )

                number += 1
                continue

            if category == module['Category']:
                data.append(
                    (number, module['Category'], module['BaseName'],
                     module['Rank'], module['Name'])
                )

                shorts.update({
                    number: module['BaseName']
                })

                number += 1

        if category:
            self.print_table(f"{category.title()} Modules", headers, *data)
        else:
            self.print_table(f"Modules", headers, *data)

        if not shorts:
            raise RuntimeWarning("No modules available.")

        STORAGE.set("module_shorts", shorts)

    def show_payloads(self, payloads: dict) -> None:
        """ Show payloads.

        :param dict payloads: payloads dictionary, payload name as key
        and payload data as item
        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        headers = ("Number", "Payload", "Name")
        shorts = {}
        number = 0
        data = []

        for payload in sorted(payloads):
            payload = payloads[payload]

            data.append(
                (number, payload['BaseName'], payload['Name'])
            )

            shorts.update({
                number: payload['BaseName']
            })

            number += 1

        self.print_table(f"Payloads", headers, *data)

        if not shorts:
            raise RuntimeWarning("No payloads available.")

        STORAGE.set("payload_shorts", shorts)

    def show_search_plugins(self, plugins: dict, keyword: str) -> None:
        """ Show plugins that contain the keyword.

        :param dict plugins: dictionary of plugins, where plugin name is a key
        and plugin data is an item
        :param str keyword: keyword
        :return None: None
        """

        headers = ("Number", "Plugin", "Name")
        shorts = {}
        number = 0
        data = []

        for plugin in sorted(plugins):
            plugin = plugins[plugin]

            if keyword not in plugin['BaseName'] + plugin['Name']:
                continue

            data.append(
                (number, plugin['BaseName'].replace(keyword, f'%red{keyword}%end'),
                 plugin['Name'].replace(keyword, f'%red{keyword}%end'))
            )

            shorts.update(
                {number: plugin['BaseName']}
            )

            number += 1

        if data:
            self.print_table(f"Plugins", headers, *data)

        if shorts:
            STORAGE.set("plugin_shorts", shorts)

    def show_search_encoders(self, encoders: dict, keyword: str) -> None:
        """ Show encoders that contain the keyword.

        :param dict encoders: dictionary of encoders, where encoder name is a key
        and encoder data is an item
        :param str keyword: keyword
        :return None: None
        """

        headers = ("Number", "Encoder", "Name")
        shorts = {}
        number = 0
        data = []

        for encoder in sorted(encoders):
            encoder = encoders[encoder]

            if keyword not in encoder['BaseName'] + encoder['Name']:
                continue

            data.append(
                (number, encoder['BaseName'].replace(keyword, f'%red{keyword}%end'),
                 encoder['Name'].replace(keyword, f'%red{keyword}%end'))
            )

            shorts.update(
                {number: encoder['BaseName']}
            )

            number += 1

        if data:
            self.print_table(f"Encoders", headers, *data)

        if shorts:
            STORAGE.set("encoder_shorts", shorts)

    def show_search_modules(self, modules: dict, keyword: str) -> None:
        """ Show modules that contain the keyword.

        :param dict modules: dictionary of modules, where module name is a key
        and module data is an item
        :param str keyword: keyword
        :return None: None
        """

        headers = ("Number", "Category", "Module", "Rank", "Name")
        shorts = {}
        number = 0
        data = []

        for module in sorted(modules):
            module = modules[module]

            if keyword not in module['BaseName'] + module['Name']:
                continue

            data.append(
                (number, module['Category'],
                 module['BaseName'].replace(keyword, f'%red{keyword}%end'),
                 module['Rank'],
                 module['Name'].replace(keyword, f'%red{keyword}%end'))
            )

            shorts.update(
                {number: module['BaseName']}
            )

            number += 1

        if data:
            self.print_table(f"Modules", headers, *data)

        if shorts:
            STORAGE.set("module_shorts", shorts)

    def show_search_payloads(self, payloads: dict, keyword: str) -> None:
        """ Show payloads that contain the keyword.

        :param dict payloads: dictionary of payloads, where payload name is a key
        and payload data is an item
        :param str keyword: keyword
        :return None: None
        """

        headers = ("Number", "Module", "Name")
        shorts = {}
        number = 0
        data = []

        for payload in sorted(payloads):
            payload = payloads[payload]

            if keyword not in payload['BaseName'] + payload['Name']:
                continue

            data.append(
                (number,
                 payload['BaseName'].replace(keyword, f'%red{keyword}%end'),
                 payload['Name'].replace(keyword, f'%red{keyword}%end'))
            )

            shorts.update(
                {number: payload['BaseName']}
            )

            number += 1

        if data:
            self.print_table(f"Payloads", headers, *data)

        if shorts:
            STORAGE.set("payload_shorts", shorts)

    def show_module_targets(self, module: Module) -> None:
        """ Show module targets.

        :param Module module: module object
        :return None: None
        :raises RuntimeWarning: with trailing error message
        """

        if not module:
            raise RuntimeWarning("No module selected.")

        targets = module.info['Targets']
        headers = ('Current', 'ID', 'Name')
        number = 0
        data = []

        for target in targets:
            data.append(('*' if module.target == targets[target] else '', number, target))
            number += 1

        if data:
            self.print_table(f"Targets ({module.info['Module']})", headers, *data)

    def show_module_devices(self, module: Module) -> None:
        """ Show module devices.

        :param Module module: module object
        :return None: None
        :raises RuntimeWarning: with trailing error message
        """

        if not module:
            raise RuntimeWarning("No module selected.")

        devices = module.info['Devices']
        headers = ('ID', 'Name')
        number = 0
        data = []

        for device in devices:
            data.append((number, device))
            number += 1

        if data:
            self.print_table(f"Devices ({module.info['Module']})", headers, *data)

    def show_module_information(self, details: Optional[dict] = None) -> None:
        """ Show module details.

        :param Optional[dict] details: module details
        :return None: None
        """

        if not details:
            module = self.modules.get_current_module()
            details = module.info

        style = dedent(f"""
            Name: %s
          Module: %s
        Platform: %s
            Rank: %s

        Authors:
          %s

        Description:
          %s
        """)

        authors = '\n  '.join(details['Authors'])
        name = details.get('BaseName', details.get('Module', 'Unnamed'))

        desc = dedent(details['Description']).strip()
        desc = fill(desc, width=70,
                    subsequent_indent='  ')

        style = style % (details['Name'], name, details['Platform'],
                         details['Rank'], authors, desc)

        refs = []

        for ref in details['References']:
            for key, value in ref.items():
                refs.append(f'{key}: {str(value)}')

        if refs:
            refs = '\n  '.join(refs)

            style += dedent(f"""
            References:
              %s
            """) % refs

        if details['Devices']:
            devices = '\n  '.join(details['Devices'])

            style += dedent(f"""
            Devices:
              %s
            """) % devices

        effects = details['Notes'].get('SideEffects', [])
        stability = details['Notes'].get('Stability', [])
        reliability = details['Notes'].get('Reliability', [])

        if effects:
            effects = '\n  '.join(effects)

            style += dedent(f"""
            Side effects:
              %s
            """) % effects

        if stability:
            stability = '\n  '.join(stability)

            style += dedent(f"""
            Stability:
              %s
            """) % stability

        if reliability:
            reliability = '\n  '.join(reliability)

            style += dedent(f"""
            Reliability:
              %s
            """) % reliability

        self.print_empty(style)

    def show_options_table(self, title: str, options: dict) -> None:
        """ Show options for specific title.

        :param str title: title
        :param dict options: options, option names as keys and option data as
        items
        :return None: None
        """

        headers = ("Option", "Value", "Required", "Description")
        data = []

        for option in sorted(options):
            if not options[option].visible:
                continue

            value, required = options[option].value, \
                options[option].required

            required = "yes" if required else "no"
            value = "" if value is None else value

            if isinstance(value, bool):
                value = "yes" if value else "no"

            data.append(
                (option, value, required,
                 options[option].description)
            )

        self.print_table(title, headers, *data)

    def show_options(self, module: Module) -> None:
        """ Show options.

        :param Module module: module object
        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        if not module:
            raise RuntimeWarning("No module selected.")

        if module.options:
            self.show_options_table(
                f"Module Options ({module.info['Module']})", module.options)

        payload = self.payloads.get_current_payload(module)

        if not payload:
            return

        encoder = self.encoders.get_current_encoder(module, payload)

        if payload.options:
            self.show_options_table(
                f"Payload Options ({payload.info['Payload']})", payload.options)

        if encoder and encoder.options:
            self.show_options_table(
                f"Encoder Options ({encoder.info['Encoder']})", encoder.options)

    def show_advanced(self, module: Module) -> None:
        """ Show advanced options.

        :param Module module: module object
        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        payload = self.payloads.get_current_payload(module)

        if not module:
            raise RuntimeWarning("No module selected.")

        if module.advanced:
            self.show_options_table(
                f"Module Advanced Options ({module.info['Module']})", module.advanced)

        if not payload:
            return

        encoder = self.encoders.get_current_encoder(module, payload)

        if payload.advanced:
            self.show_options_table(
                f"Payload Advanced Options ({payload.info['Payload']})", payload.advanced)

        if encoder and encoder.advanced:
            self.show_options_table(
                f"Encoder Advanced Options ({encoder.info['Encoder']})", encoder.advanced)
