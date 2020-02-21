from configparser import ConfigParser, NoOptionError
import json


class Shard:
    """Shard configuration for a cluster

    Args:
        shard_enabled (bool):   Enable server sharding.
        bind_ip (str):  IP address the master server will listen on for other shard servers to connect to.
        master_ip (str):    IP address that a non-master shard will use when trying to connect to the master shard.
        master_port (int):  UDP port that the master server will listen on or a shard will connect to.
        cluster_key (str):  Password used to authenticate a slave server to the master.
        conf (ConfigParser):    Configuration information optionally passed in if it already exists.

    Attributes:
        shard_enabled (bool):   Enable server sharding.
            This must be set to true for multi-level servers.
            For single-level servers, it can be omitted.
        bind_ip (str):  IP address the master server will listen on for other shard servers to connect to.
            Required: If shard_enabled = true and is_master = true
            Set this to 127.0.0.1 if all of your servers in your cluster are on the same machine
            or 0.0.0.0 if the servers in your cluster are on different machines.
            This only needs to be set for the master server, either in cluster.ini, or the master server's server.ini.
        master_ip (str):    IP address that a non-master shard will use when trying to connect to the master shard.
            Required: If shard_enabled = true and is_master = false
            If all servers in a cluster are on the same machine, set this to 127.0.0.1
        master_port (int):  UDP port that the master server will listen on or a shard will connect to.
            This should be set to the same value for all shards by having a single entry in cluster.ini
             or omitted completely to use the default.
        cluster_key (str):  Password used to authenticate a slave server to the master.
            If you are running servers on different machines that need to connect to each other
            this value must be the same on each machine.
            For servers running on the same machine, you can just set this once in cluster.ini.
    """
    def __init__(self, shard_enabled=False, bind_ip="127.0.0.1", master_ip="127.0.0.1"
                 , master_port=10888, cluster_key="", conf=ConfigParser()):
        if not conf.has_section("SHARD"):
            self.shard_enabled = shard_enabled
            self.bind_ip = bind_ip
            self.master_ip = master_ip
            self.master_port = master_port
            self.cluster_key = cluster_key
        else:
            try:
                self.shard_enabled = conf.getboolean("SHARD", "shard_enabled")
            except NoOptionError:
                self.shard_enabled = shard_enabled
            try:
                self.bind_ip = conf.get("SHARD", "bind_ip")
            except NoOptionError:
                self.bind_ip = bind_ip
            try:
                self.master_ip = conf.get("SHARD", "master_ip")
            except NoOptionError:
                self.master_ip = master_ip
            try:
                self.master_port = conf.getint("SHARD", "master_port")
            except NoOptionError:
                self.master_port = master_port
            try:
                self.cluster_key = conf.get("SHARD", "cluster_key")
            except NoOptionError:
                self.cluster_key = cluster_key

    def set_config(self, config):
        """Sets config object with configurations from this class"""
        if not config.has_section("SHARD"):
            config.add_section("SHARD")
        config.set("SHARD", "shard_enabled", str(self.shard_enabled))
        config.set("SHARD", "bind_ip", self.bind_ip)
        config.set("SHARD", "master_ip", self.master_ip)
        config.set("SHARD", "master_port", str(self.master_port))
        config.set("SHARD", "cluster_key", self.cluster_key)

    def to_json(self):
        """Turns configuration class into JSON"""
        return json.dumps(self.__dict__, indent=4)
