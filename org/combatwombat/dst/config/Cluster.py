from org.combatwombat.dst.config.cluster.Gameplay import Gameplay
from org.combatwombat.dst.config.cluster.Misc import Misc
from org.combatwombat.dst.config.cluster.Network import Network
from org.combatwombat.dst.config.cluster.Steam import Steam
from org.combatwombat.dst.config.cluster.Shard import Shard
from os import path
from configparser import ConfigParser
import json


class Cluster:
    """Cluster configuration class for Don't Starve Together.

    Args:
        cluster_file (str): Path to cluster.ini file for a DST cluster.

    Attributes:
        gameplay (Gameplay): Gameplay configuration section.
        misc (Misc): Misc configuration section.
        network (Network): Network configuration section.
        shard (Shard): Shard configuration section.
        steam (Steam): Steam configuration section.
    """

    def __init__(self, cluster_file=None):
        config = ConfigParser()
        if cluster_file is not None:
            if path.exists(cluster_file):
                config.read(cluster_file)
        self.gameplay = Gameplay(conf=config)
        self.misc = Misc(conf=config)
        self.network = Network(conf=config)
        self.shard = Shard(conf=config)
        self.steam = Steam(conf=config)

    def write_ini(self, file):
        """Write configuration data to specified file path

        Args:
            file (str): Path to write configuration file
        """
        config = ConfigParser()
        with open(file, 'w') as iniFile:
            self.network.set_config(config)
            self.shard.set_config(config)
            self.steam.set_config(config)
            self.gameplay.set_config(config)
            self.misc.set_config(config)
            config.write(iniFile)

    def to_json(self):
        """Turns configuration class into JSON"""
        dict_to_return = {"GAMEPLAY": self.gameplay.__dict__
                          , "MISC": self.misc.__dict__
                          , "NETWORK": self.network.__dict__
                          , "SHARD": self.shard.__dict__
                          , "STEAM": self.steam.__dict__}
        return json.dumps(dict_to_return, indent=4)
