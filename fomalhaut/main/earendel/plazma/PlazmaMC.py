from ...settings import Settings as _Settings
from ....module.instance import Instance as _Instance
from ....module.instance.handlers.ActivityHandler import ActivityHandler as _Activity


class Plazma(_Instance):
    """
    An Instance module for Discord based discord.py

    Parameters
    -----------
    settings: Settings
        설정
    """

    def __init__(self, settings: _Settings):
        super().__init__(settings, "earendel", "Plazma", _Activity("idle", "playing", "Plazma 1.19.4"))
