from ...settings import Settings as _Settings
from ....module.instance import Instance as _Instance
from ....module.instance.handlers.ActivityHandler import ActivityHandler as _Activity


class BasicNoticeInstance(_Instance):
    """
    일반 공지 인스턴스를 생성합니다.

    Parameters
    -----------
    settings: Settings
        설정
    name: str
        인스턴스 이름
    activity: ActivityHandler
        활동 핸들러
    """

    def __init__(
            self, settings: _Settings, name: str, activity: _Activity
    ):
        super().__init__(settings, "mdd", name, activity)
