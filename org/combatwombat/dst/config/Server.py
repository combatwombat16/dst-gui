from org.combatwombat.dst.config.server.Network import Network
from org.combatwombat.dst.config.server.Shard import Shard
from org.combatwombat.dst.config.server.Steam import Steam
from configparser import ConfigParser
from os import path
import json


class Server:
    """Server configuration class for Don't Starve Together.

    Args:
        server_file (str): Path to server.ini file for a DST server.

    Attributes:
        network (Network): Network configuration section.
        shard (Shard): Shard configuration section.
        steam (Steam): Steam configuration section.
    """
    def __init__(self, server_file=None):
        config = ConfigParser()
        if server_file is not None:
            if path.exists(server_file):
                config.read(server_file)
        self.network = Network(conf=config)
        self.shard = Shard(conf=config)
        self.steam = Steam(conf=config)

    def write_ini(self, file):
        """Write configuration data to specified file path

        Args:
            file (str): Path to write configuration file
        """
        write_config = ConfigParser()
        with open(file, 'w') as iniFile:
            self.network.set_config(write_config)
            self.shard.set_config(write_config)
            self.steam.set_config(write_config)
            write_config.write(iniFile)

    def to_json(self):
        """Turns configuration class into JSON"""
        dict_to_return = {"NETWORK": self.network.__dict__
                          , "SHARD": self.shard.__dict__
                          , "STEAM": self.steam.__dict__}
        return json.dumps(dict_to_return, indent=4)
