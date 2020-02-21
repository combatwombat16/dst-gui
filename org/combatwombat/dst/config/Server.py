from org.combatwombat.dst.config.server.Network import Network, NetworkSchema
from org.combatwombat.dst.config.server.Shard import Shard, ShardSchema
from org.combatwombat.dst.config.server.Steam import Steam, SteamSchema
from configparser import ConfigParser
from marshmallow import Schema, fields, post_load


class Server:
    """Server configuration class for Don't Starve Together.

    Args:
        network (Network): Network configuration section.
        shard (Shard): Shard configuration section.
        steam (Steam): Steam configuration section.

    Attributes:
        network (Network): Network configuration section.
        shard (Shard): Shard configuration section.
        steam (Steam): Steam configuration section.
    """
    def __init__(self, network=Network(), shard=Shard(), steam=Steam()):
        self.network = network
        self.shard = shard
        self.steam = steam

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
        return ServerSchema().dumps(self)


class ServerSchema(Schema):
    network = fields.Nested(NetworkSchema, load_from="network")
    shard = fields.Nested(ShardSchema, load_from="shard")
    steam = fields.Nested(SteamSchema, load_from="steam")

    @post_load
    def make_server(self, data, **kwargs):
        return Server(**data)
