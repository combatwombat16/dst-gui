from random import random
from marshmallow import Schema, fields, post_load


class Shard:
    """Shard configurations for a server.

    Args:
        is_master (bool):   Sets a shard to be the master shard for a cluster.
        name (str):   This is the name of the shard that will show up in log files.
        shard_id (int):  This is field is automatically generated for non-master servers.

    Attributes:
        is_master (bool):   Sets a shard to be the master shard for a cluster.
            There must be exactly one master server per cluster.
            Set this to true in your master server’s server.ini, and false in every other server.ini.
            Required: If shard_enabled = true
        name (str):   This is the name of the shard that will show up in log files.
            It is ignored for the master server, which always has the name [SHDMASTER].
            Required: if shard_enabled = true and is_master = false
        id (int):  This is field is automatically generated for non-master servers.
            Used internally to uniquely identify a server.
            Altering this or removing it may cause problems on your server if anybody’s
            character currently resides in the world that this server manages.
    """
    def __init__(self, is_master=True, name="", shard_id=random()):
        self.is_master = is_master
        self.name = name
        self.id = shard_id if (self.is_master is None) else None

    def set_config(self, config):
        """Sets config object with configurations from this class"""
        if not config.has_section("SHARD"):
            config.add_section("SHARD")
        config.set("SHARD", "is_master", str(self.is_master))
        config.set("SHARD", "name", self.name)
        config.set("SHARD", "id", str(self.id))

    def to_json(self):
        """Turns configuration class into JSON"""
        return ShardSchema().dumps(self)


class ShardSchema(Schema):
    is_master = fields.Boolean()
    name = fields.Str()
    shard_id = fields.Integer()

    @post_load
    def make_shard(self, data, **kwargs):
        return Shard(**data)
