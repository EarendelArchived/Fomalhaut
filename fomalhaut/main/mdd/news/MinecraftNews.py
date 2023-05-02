from ...settings import Settings as _Settings
from ....module.instance import Instance as _Instance
from ....module.instance.handlers.ActivityHandler import ActivityHandler as _Activity


class MinecraftNews(_Instance):
    """
    모든 기술의 집약체를 시작합니다.

    Parameters
    -----------
    settings: Settings
        설정
    """

    def __init__(self, settings: _Settings):
        super().__init__(settings, "mdd", "News", _Activity("dnd", "playing", "뉴스 업로드"))
