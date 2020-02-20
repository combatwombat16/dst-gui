from configparser import ConfigParser, NoOptionError


class Misc:
    """Misc configuration for a cluster

    Args:
        max_snapshots (int):    Maximum number of snapshots to retain.
        conf (ConfigParser):    Configuration information optionally passed in if it already exists.

    Attributes:
        max_snapshots (int):    Maximum number of snapshots to retain.
            These snapshots are created every time a save occurs.
            Snapshots are available in the “Rollback” tab on the “Host Game” screen.
    """
    def __init__(self, max_snapshots=6, conf=ConfigParser()):
        if not conf.has_section("MISC"):
            self.max_snapshots = max_snapshots
        else:
            try:
                self.max_snapshots = conf.getint("MISC", "max_snapshots")
            except NoOptionError:
                self.max_snapshots = max_snapshots

    def set_config(self, config):
        """Sets config object with configurations from this class"""
        if not config.has_section("MISC"):
            config.add_section("MISC")
        config.set("MISC", "max_snapshots", self.max_snapshots)
