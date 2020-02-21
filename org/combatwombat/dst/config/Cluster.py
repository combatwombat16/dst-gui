from org.combatwombat.dst.config.cluster.Gameplay import Gameplay, GameplaySchema
from org.combatwombat.dst.config.cluster.Misc import Misc, MiscSchema
from org.combatwombat.dst.config.cluster.Network import Network, NetworkSchema
from org.combatwombat.dst.config.cluster.Steam import Steam, SteamSchema
from org.combatwombat.dst.config.cluster.Shard import Shard, ShardSchema
from os import path
from configparser import ConfigParser
from marshmallow import Schema, fields, post_load


class Cluster:
    """Cluster configuration class for Don't Starve Together.

    Args:
        gameplay (Gameplay): Gameplay configuration section.
        misc (Misc): Misc configuration section.
        network (Network): Network configuration section.
        shard (Shard): Shard configuration section.
        steam (Steam): Steam configuration section.

    Attributes:
        gameplay (Gameplay): Gameplay configuration section.
        misc (Misc): Misc configuration section.
        network (Network): Network configuration section.
        shard (Shard): Shard configuration section.
        steam (Steam): Steam configuration section.
    """

    def __init__(self, gameplay=Gameplay(), misc=Misc(), network=Network(), shard=Shard(), steam=Steam()):
        self.gameplay = gameplay
        self.misc = misc
        self.network = network
        self.shard = shard
        self.steam = steam

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
        return ClusterSchema().dumps(self)


class ClusterSchema(Schema):
    network = fields.Nested(NetworkSchema, load_from="network")
    shard = fields.Nested(ShardSchema, load_from="shard")
    steam = fields.Nested(SteamSchema, load_from="steam")
    gameplay = fields.Nested(GameplaySchema, load_from="gameplay")
    misc = fields.Nested(MiscSchema, load_from="misc")

    @post_load
    def make_cluster(self, data, **kwargs):
        return Cluster(**data)
