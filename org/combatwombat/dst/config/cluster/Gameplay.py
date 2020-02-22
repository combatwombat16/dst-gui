from marshmallow import Schema, fields, post_load, validate


class Gameplay:
    """Gameplay configuration for a cluster

    Args:
        max_players (int):  The maximum number of players that may be connected to the cluster at one time.
        pvp (bool): Enable PVP.
        game_mode (str):    The cluster’s game mode.
        pause_when_empty (bool):    Pause the server when there are no players connected.
        vote_kick_enabled (bool):   Set to true to enable the “Vote to Kick” feature.

    Attributes:
        max_players (int):  The maximum number of players that may be connected to the cluster at one time.
        pvp (bool): Enable PVP.
        game_mode (str):    The cluster’s game mode.
            This field is the equivalent of the “Game Mode” field on the “Host Game” screen.
            Valid values are survival, endless or wilderness.
        pause_when_empty (bool):    Pause the server when there are no players connected.
        vote_kick_enabled (bool):   Set to true to enable the “Vote to Kick” feature.
    """
    def __init__(self, max_players=16, pvp=False, game_mode="survival", pause_when_empty=False, vote_kick_enabled=False):
        self.max_players = max_players
        self.pvp = pvp
        self.game_mode = game_mode
        self.pause_when_empty = pause_when_empty
        self.vote_kick_enabled = vote_kick_enabled

    def set_config(self, config):
        """Sets config object with configurations from this class"""
        if not config.has_section("GAMEPLAY"):
            config.add_section("GAMEPLAY")
        config.set("GAMEPLAY", "max_players", str(self.max_players))
        config.set("GAMEPLAY", "pvp", str(self.pvp))
        config.set("GAMEPLAY", "game_mode", self.game_mode)
        config.set("GAMEPLAY", "pause_when_empty", str(self.pause_when_empty))
        config.set("GAMEPLAY", "vote_kick_enabled", str(self.vote_kick_enabled))

    def to_json(self):
        """Turns configuration class into JSON"""
        return GameplaySchema().dumps(self)


class GameplaySchema(Schema):
    max_players = fields.Integer()
    pvp = fields.Boolean()
    game_mode = fields.String(required=True, validate=validate.OneOf(["survival", "endless", "wilderness"]))
    pause_when_empty = fields.Boolean()
    vote_kick_enabled = fields.Boolean()

    @post_load
    def make_gameplay(self, data, **kwargs):
        return Gameplay(**data)
