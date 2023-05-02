from ...settings import Settings as _Settings
from ....module.instance import Instance as _Instance
from ....module.instance.handlers.ActivityHandler import ActivityHandler as _Activity


class AlphaBot(_Instance):
    """
    스파이 알파봇을 Git에 파견합니다.

    Parameters
    -----------
    settings: Settings
        설정
    """

    def __init__(self, settings: _Settings):
        super().__init__(settings, "earendel", "AlphaBot", _Activity("idle", "playing", "공작 활동"))
