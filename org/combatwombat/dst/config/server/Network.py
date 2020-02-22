from marshmallow import Schema, fields, post_load, validate


class Network:
    """Network port configuration for server

    Args:
        port (int): The UDP port that this server will listen for connections on.

    Attributes:
        server_port (int): The UDP port that this server will listen for connections on.
            If you are running a multi-level cluster, this port must be different for each server.
            This port must be between 10998 and 11018 inclusive in order for players on the same LAN
            to see it in their server listing.
            Ports below 1024 are restricted to privileged users on some operating systems.
    """
    def __init__(self, port=10999):
        self.server_port = port

    def set_config(self, config):
        if not config.has_section("NETWORK"):
            config.add_section("NETWORK")
        config.set("NETWORK", "server_port", str(self.server_port))

    def to_json(self):
        """Turns configuration class into JSON"""
        return NetworkSchema().dumps(self)


class NetworkSchema(Schema):
    port = fields.Integer(required=True, validate=validate.Range(10998, 11018))

    @post_load
    def make_network(self, data, **kwargs):
        return Network(**data)


