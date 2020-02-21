from marshmallow import Schema, fields, post_load


class Steam:
    """Steam port configurations for a server

    Args:
        authentication_port (int):  Internal port used by Steam.
        master_server_port (int):   Internal port used by Steam.

    Attributes:
        authentication_port (int):  Internal port used by steam.
            Make sure that this is different for each server you run on the same machine.
        master_server_port (int):   Internal port used by steam.
            Make sure that this is different for each server you run on the same machine.
    """
    def __init__(self, authentication_port=8766, master_server_port=27016):
        self.authentication_port = authentication_port
        self.master_server_port = master_server_port

    def set_config(self, config):
        """Sets config object with configurations from this class"""
        if not config.has_section("STEAM"):
            config.add_section("STEAM")
        config.set("STEAM", "authentication_port", str(self.authentication_port))
        config.set("STEAM", "master_server_port", str(self.master_server_port))

    def to_json(self):
        """Turns configuration class into JSON"""
        return SteamSchema().dumps(self)


class SteamSchema(Schema):
    authentication_port = fields.Integer()
    master_server_port = fields.Integer()

    @post_load
    def make_steam(self, data, **kwargs):
        return Steam(**data)
