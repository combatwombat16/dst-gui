from marshmallow import Schema, fields, post_load, validate


class Network:
    """Network configuration for a cluster

    Args:
        offline_server (bool):  Create an offline server.
        tick_rate (int):    This is the number of times per-second that the server sends updates to clients.
        whitelist_slots (int):  The number of reserved slots for whitelisted players.
        cluster_password (str): This is the password that players must enter to join your server.
        cluster_name (str): The name for your server cluster.
        cluster_description (str):  Cluster description.
        cluster_intention (str):   The cluster’s playstyle.
        lan_only_cluster (bool):   The server will only accept connections from machines on the same LAN
        autosaver_enabled (bool): Automatically save state at end of each game day.

    Attributes:
        offline_server (bool):  Create an offline server.
            The server will not be listed publicly, and only players on the local network will be able to join.
            Steam-related functionality will not work.
        tick_rate (int):    This is the number of times per-second that the server sends updates to clients.
            Increasing this may improve precision, but will result in more network traffic.
        whitelist_slots (int):  The number of reserved slots for whitelisted players.
            To whitelist a player, add their Klei UserId to the whitelist.txt file
            (Place this file in the same directory as cluster.ini)
        cluster_password (str): This is the password that players must enter to join your server.
            Leave this blank or omit it for no password.
        cluster_name (str): The name for your server cluster.
            This is the name that will show up in server browser.
        cluster_description (str):  Cluster description.
            This will show up in the server details area on the “Browse Games” screen.
        cluster_intention (str):   The cluster’s playstyle.
            This field is the equivalent of the “Server Playstyle” field on the “Host Game” screen.
            Valid values are cooperative, competitive, social, or madness.
        lan_only_cluster (bool):   The server will only accept connections from machines on the same LAN
        autosaver_enabled (bool): Automatically save state at end of each game day.
            The game will still save on shutdown, and can be manually saved using c_save().
    """
    def __init__(self, offline_server=False, tick_rate=15, whitelist_slots=0, cluster_password=""
                 , cluster_name="", cluster_description="", lan_only_cluster=False
                 , cluster_intention="cooperative", autosaver_enabled=True):
        self.offline_server = offline_server
        self.tick_rate = tick_rate
        self.whitelist_slots = whitelist_slots
        self.cluster_password = cluster_password
        self.cluster_name = cluster_name
        self.cluster_description = cluster_description
        self.lan_only_cluster = lan_only_cluster
        self.cluster_intention = cluster_intention
        self.autosaver_enabled = autosaver_enabled

    def set_config(self, config):
        """Sets config object with configurations from this class"""
        if not config.has_section("NETWORK"):
            config.add_section("NETWORK")
        config.set("NETWORK", "offline_server", str(self.offline_server))
        config.set("NETWORK", "tick_rate", str(self.tick_rate))
        config.set("NETWORK", "whitelist_slots", str(self.whitelist_slots))
        config.set("NETWORK", "cluster_password", self.cluster_password)
        config.set("NETWORK", "cluster_name", self.cluster_name)
        config.set("NETWORK", "cluster_description", self.cluster_description)
        config.set("NETWORK", "lan_only_cluster", str(self.lan_only_cluster))
        config.set("NETWORK", "cluster_intention", self.cluster_intention)
        config.set("NETWORK", "autosaver_enabled", str(self.autosaver_enabled))

    def to_json(self):
        """Turns configuration class into JSON"""
        return NetworkSchema().dumps(self)


class NetworkSchema(Schema):
    offline_server = fields.Boolean(required=True)
    tick_rate = fields.Integer(validate=validate.OneOf([10, 15, 30, 60]))
    whitelist_slots = fields.Integer()
    cluster_password = fields.String()
    cluster_name = fields.String(required=True)
    cluster_description = fields.String(required=True)
    lan_only_cluster = fields.Boolean(required=True)
    cluster_intention = fields.String(validate=validate.OneOf(["cooperative", "competitive", "social", "madness"]))
    autosaver_enabled = fields.Boolean()

    @post_load
    def make_network(self, data, **kwargs):
        return Network(**data)
