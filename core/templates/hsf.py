from core.cli.fmt import fmt
from core.cli.badges import badges
from core.cli.parser import parser
from core.cli.tables import tables

from core.base.jobs import jobs
from core.base.config import config
from core.base.sessions import sessions
from core.base.execute import execute
from core.base.exceptions import exceptions
from core.base.storage import local_storage
from core.base.storage import global_storage

from core.modules.modules import modules
from core.plugins.plugins import plugins

from utils.adb_tools import adb_tools
from utils.fsmanip import fsmanip
from utils.hatvenom import hatvenom
from utils.web_tools import web_tools
from utils.tcp_tools import tcp_tools
from utils.pseudo_shell import pseudo_shell
from utils.string_tools import string_tools

class HatSploit:
    def __init__(self):
        self.fmt = fmt()
        self.badges = badges()
        self.parser = parser()
        self.tables = tables()
        
        self.jobs = jobs()
        self.config = config()
        self.sessions = sessions()
        self.execute = execute()
        self.exceptions = exceptions()
        self.local_storage = local_storage()
        self.global_storage = global_storage()
        
        self.modules = modules()
        self.plugins = plugins()
        
        self.adb_tools = adb_tools()
        self.fsmanip = fsmanip()
        self.hatvenom = hatvenom()
        self.web_tools = web_tools()
        self.tcp_tools = tcp_tools()
        self.pseudo_shell = pseudo_shell()
        self.string_tools = string_tools()
