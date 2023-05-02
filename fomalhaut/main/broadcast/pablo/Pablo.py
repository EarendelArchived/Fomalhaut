from ..common.BasicTwitchInstance import BasicTwitchInstance as _Instance
from ...settings import Settings as _Settings
from ....module.instance.handlers.ActivityHandler import ActivityHandler as _Activity


class Pablo(_Instance):
    """
    트위치 스트리머 Pablo님의 봇 인스턴스를 생성합니다.

    Parameters
    -----------
    settings: Settings
        설정
    """

    def __init__(self, settings: _Settings):
        super().__init__(settings, "Pablo", _Activity("dnd", "playing", "대나무 먹방"))
