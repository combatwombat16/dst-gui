from configparser import NoOptionError, ConfigParser
import json


class Network:
    """Network port configuration for server

    Args:
        port (int): The UDP port that this server will listen for connections on.
        conf (ConfigParser):    Configuration information optionally passed in if it already exists.

    Attributes:
        server_port (int): The UDP port that this server will listen for connections on.
            If you are running a multi-level cluster, this port must be different for each server.
            This port must be between 10998 and 11018 inclusive in order for players on the same LAN
            to see it in their server listing.
            Ports below 1024 are restricted to privileged users on some operating systems.
    """
    def __init__(self, port=10999, conf=ConfigParser()):
        if not conf.has_section("NETWORK"):
            self.server_port = self.check_port_validity(port)
        else:
            try:
                self.server_port = self.check_port_validity(conf.get("NETWORK", "server_port"))
            except NoOptionError:
                self.server_port = self.check_port_validity(port)

    def set_config(self, config):
        if not config.has_section("NETWORK"):
            config.add_section("NETWORK")
        config.set("NETWORK", "server_port", str(self.server_port))

    def check_port_validity(self, port_to_check):
        """Check whether the server port is within the valid range"""
        if 10998 <= port_to_check <= 11018:
            return port_to_check
        else:
            raise ValueError("Port assignment outside of valid range, 10998-11018.\n Port provided: {}".format(port_to_check))

    def to_json(self):
        """Turns configuration class into JSON"""
        return json.dumps(self.__dict__, indent=4)
