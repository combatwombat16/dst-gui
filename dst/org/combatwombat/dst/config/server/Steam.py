from configparser import NoOptionError, ConfigParser


class Steam:
    """Steam port configurations for a server

    Args:
        authentication_port (int):  Internal port used by Steam.
        master_server_port (int):   Internal port used by Steam.
        conf (ConfigParser):    Configuration information optionally passed in if it already exists.

    Attributes:
        authentication_port (int):  Internal port used by steam.
            Make sure that this is different for each server you run on the same machine.
        master_server_port (int):   Internal port used by steam.
            Make sure that this is different for each server you run on the same machine.
    """
    def __init__(self, authentication_port=8766, master_server_port=27016, conf=ConfigParser()):
        if not conf.has_section("STEAM"):
            self.authentication_port = authentication_port
            self.master_server_port = master_server_port
        else:
            try:
                self.authentication_port = conf.getint("STEAM", "authentication_port")
            except NoOptionError:
                self.authentication_port = authentication_port
            try:
                self.master_server_port = conf.getint("STEAM", "master_server_port")
            except NoOptionError:
                self.master_server_port = master_server_port

    def set_config(self, config):
        """Sets config object with configurations from this class"""
        if not config.has_section("STEAM"):
            config.add_section("STEAM")
        config.set("STEAM", "authentication_port", self.authentication_port)
        config.set("STEAM", "master_server_port", self.master_server_port)
