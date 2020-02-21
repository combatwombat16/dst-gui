from marshmallow import Schema, fields, post_load


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
        self.server_port = self.__check_port_validity(port)

    def set_config(self, config):
        if not config.has_section("NETWORK"):
            config.add_section("NETWORK")
        config.set("NETWORK", "server_port", str(self.server_port))

    def __check_port_validity(self, port_to_check):
        """Check whether the server port is within the valid range"""
        if 10998 <= port_to_check <= 11018:
            return port_to_check
        else:
            raise ValueError("Port assignment outside of valid range, 10998-11018.\n Port provided: {}".format(port_to_check))

    def to_json(self):
        """Turns configuration class into JSON"""
        return NetworkSchema().dumps(self)


class NetworkSchema(Schema):
    port = fields.Integer()

    @post_load
    def make_network(self, data, **kwargs):
        return Network(**data)


