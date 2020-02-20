from configparser import NoOptionError, ConfigParser
from random import random


class Shard:
    """Shard configurations for a server.

    Args:
        is_master (bool):   Sets a shard to be the master shard for a cluster.
        name (str):   This is the name of the shard that will show up in log files.
        shard_id (int):  This is field is automatically generated for non-master servers.
        conf (ConfigParser):    Configuration information optionally passed in if it already exists.

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
    def __init__(self, is_master=None, name=None, shard_id=random(), conf=ConfigParser()):
        if not conf.has_section("SHARD"):
            self.is_master = is_master
            self.name = name
            self.id = shard_id if (self.is_master is None) else None
        else:
            try:
                self.is_master = conf.get("SHARD", "is_master")
            except NoOptionError:
                self.is_master = is_master
            try:
                self.name = conf.get("SHARD", "name")
            except NoOptionError:
                self.name = name
            try:
                self.id = conf.get("SHARD", "id")
            except NoOptionError:
                self.id = shard_id

    def set_config(self, config):
        """Sets config object with configurations from this class"""
        if not config.has_section("SHARD"):
            config.add_section("SHARD")
        config.set("SHARD", "is_master", self.is_master)
        config.set("SHARD", "name", self.name)
        config.set("SHARD", "id", self.id)
