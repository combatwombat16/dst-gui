from configparser import ConfigParser, NoOptionError
from enum import Enum
from marshmallow import Schema, fields, post_load


class GameMode(Enum):
    """Allowable values for game_mode

        Values:
            survival (str): Survival mode.
                Dead players are ghosts until revived.
                Sanity is drained for dead players.
                Reviving costs a penalty to maximum health.
                World will be rebuild when all active players are dead.
            endless (str):  Endless mode.
                Players may resurrect themselves at the portal.
                Reviving costs a penalty to maximum health.
                World does not reset.
            wilderness (str):   Wilderness mode.
                Players spawn in random locations.
                Dying sends you back to character select screen.
                No reviving.
                World does not reset.
    """
    survival = "survival"
    endless = "endless"
    wilderness = "wilderness"


class Gameplay:
    """Gameplay configuration for a cluster

    Args:
        max_players (int):  The maximum number of players that may be connected to the cluster at one time.
        pvp (bool): Enable PVP.
        game_mode (str):    The cluster’s game mode.
        pause_when_empty (bool):    Pause the server when there are no players connected.
        vote_kick_enabled (bool):   Set to true to enable the “Vote to Kick” feature.
        conf (ConfigParser):    Configuration information optionally passed in if it already exists.

    Attributes:
        max_players (int):  The maximum number of players that may be connected to the cluster at one time.
        pvp (bool): Enable PVP.
        game_mode (str):    The cluster’s game mode.
            This field is the equivalent of the “Game Mode” field on the “Host Game” screen.
            Valid values are survival, endless or wilderness.
        pause_when_empty (bool):    Pause the server when there are no players connected.
        vote_kick_enabled (bool):   Set to true to enable the “Vote to Kick” feature.
    """
    def __init__(self, max_players=16, pvp=False, game_mode=GameMode.survival.value
                 , pause_when_empty=False, vote_kick_enabled=False, conf=ConfigParser()):
        if not conf.has_section("GAMEPLAY"):
            self.max_players = max_players
            self.pvp = pvp
            self.game_mode = game_mode
            self.pause_when_empty = pause_when_empty
            self.vote_kick_enabled = vote_kick_enabled
        else:
            try:
                self.max_players = conf.getint("GAMEPLAY", "max_players")
            except NoOptionError:
                self.max_players = max_players
            try:
                self.pvp = conf.getboolean("GAMEPLAY", "pvp")
            except NoOptionError:
                self.pvp = pvp
            try:
                self.game_mode = conf.get("GAMEPLAY", "game_mode")
            except NoOptionError:
                self.game_mode = game_mode
            try:
                self.pause_when_empty = conf.getboolean("GAMEPLAY", "pause_when_empty")
            except NoOptionError:
                self.pause_when_empty = pause_when_empty
            try:
                self.vote_kick_enabled = conf.getboolean("GAMEPLAY", "vote_kick_enabled")
            except NoOptionError:
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
    game_mode = fields.String()
    pause_when_empty = fields.Boolean()
    vote_kick_enabled = fields.Boolean()

    @post_load
    def make_gameplay(self, data, **kwargs):
        return Gameplay(**data)
