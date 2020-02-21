from configparser import ConfigParser, NoOptionError
from marshmallow import Schema, fields, post_load


class Misc:
    """Misc configuration for a cluster

    Args:
        max_snapshots (int):    Maximum number of snapshots to retain.
        console_enabled (bool): Allow lua commands to be entered in the command prompt or terminal.
        conf (ConfigParser):    Configuration information optionally passed in if it already exists.

    Attributes:
        max_snapshots (int):    Maximum number of snapshots to retain.
            These snapshots are created every time a save occurs.
            Snapshots are available in the “Rollback” tab on the “Host Game” screen.
        console_enabled (bool): Allow lua commands to be entered in the command prompt or terminal.
    """
    def __init__(self, max_snapshots=6, console_enabled=True, conf=ConfigParser()):
        if not conf.has_section("MISC"):
            self.max_snapshots = max_snapshots
            self.console_enabled = console_enabled
        else:
            try:
                self.max_snapshots = conf.getint("MISC", "max_snapshots")
            except NoOptionError:
                self.max_snapshots = max_snapshots
            try:
                self.console_enabled = conf.getint("MISC", "console_enabled")
            except NoOptionError:
                self.console_enabled = console_enabled

    def set_config(self, config):
        """Sets config object with configurations from this class"""
        if not config.has_section("MISC"):
            config.add_section("MISC")
        config.set("MISC", "max_snapshots", str(self.max_snapshots))
        config.set("MISC", "console_enabled", str(self.console_enabled))

    def to_json(self):
        """Turns configuration class into JSON"""
        return MiscSchema().dumps(self)


class MiscSchema(Schema):
    max_snapshots = fields.Integer()
    console_enabled = fields.Boolean()

    @post_load
    def make_misc(self, data, **kwargs):
        return Misc(**data)
