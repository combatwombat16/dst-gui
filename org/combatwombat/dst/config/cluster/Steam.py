from marshmallow import Schema, fields, post_load


class Steam:
    """Steam configuration for a cluster

    Args:
        steam_group_only (bool): Restrict access to cluster by steam_group
        steam_group_id (int): Steam group ID to control access to cluster
        steam_group_admins (bool): Use Steam group admins as cluster admins

    Attributes:
        steam_group_only (bool): Restrict access to cluster by steam_group
        steam_group_id (int): Steam group ID to control access to cluster.
            See here for instructions on finding your steam group id:
            http://forums.kleientertainment.com/topic/55994-server-admin-associate-your-server-with-a-steam-group/
        steam_group_admins (bool): Use Steam group admins as cluster admins
    """

    def __init__(self, steam_group_only=False, steam_group_id=0, steam_group_admins=False):
        self.steam_group_only = steam_group_only
        self.steam_group_id = steam_group_id
        self.steam_group_admins = steam_group_admins

    def set_config(self, config):
        """Sets config object with configurations from this class"""
        if not config.has_section("STEAM"):
            config.add_section("STEAM")
        config.set("STEAM", "steam_group_only", str(self.steam_group_only))
        config.set("STEAM", "steam_group_id", str(self.steam_group_id))
        config.set("STEAM", "steam_group_admins", str(self.steam_group_admins))

    def to_json(self):
        """Turns configuration class into JSON"""
        return SteamSchema().dumps(self)


class SteamSchema(Schema):
    steam_group_only = fields.Boolean(required=True)
    steam_group_id = fields.Integer()
    steam_group_admins = fields.Boolean()

    @post_load
    def make_steam(self, data, **kwargs):
        return Steam(**data)
