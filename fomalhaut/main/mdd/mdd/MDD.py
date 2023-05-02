from ..common.BasicNoticeInstance import BasicNoticeInstance as _Instance
from ...settings import Settings as _Settings
from ....module.instance.handlers.ActivityHandler import ActivityHandler as _Activity


class MDD(_Instance):
    """
    MDD 공지봇 인스턴스를 생성합니다.

    Parameters
    -----------
    settings: Settings
        설정
    """

    def __init__(self, settings: _Settings):
        super().__init__(settings, "MDD", _Activity("dnd", "playing", "MDD에서 공지"))
