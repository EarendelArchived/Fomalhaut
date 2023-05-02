from ....module.core import Final as _Final


class YouTubeComponent:
    """
    유튜브 설정 요소입니다.

    Parameters
    -----------
    target: str
        처리할 유튜브 채널 ID
    target_id: str
        처리할 유튜브 채널 이름
    message: str
        영상 업로드 안내시 Embed와
        함께 보낼 메시지
    description: str
        Embed에 함께 추가할 설명
    send: list[int]
        영상 업로드 안내를 보낼 채널 리스트

    Attributes
    -----------
    target: Final[str]
        처리할 유튜브 채널 ID
    target_id: Final[str]
        처리할 유튜브 채널 이름
    message: Final[str]
        영상 업로드 안내시 Embed와
        함께 보낼 메시지
    description: Final[str]
        Embed에 함께 추가할 설명
    send: Final[list[int]]
        영상 업로드 안내를 보낼 채널 리스트
    """

    def __init__(self, target: str, target_id: str, message: str, description: str, send: list[int]):
        self.target: _Final[str] = target
        self.target_id: _Final[str] = target_id
        self.message: _Final[str] = message
        self.description: _Final[str] = description
        self.send: _Final[list[int]] = send


class BaseYouTubeComponent:
    """
    전역 유튜브 설정 요소입니다.

    Parameters
    -----------
    icon: str
        유튜브 브랜드 아이콘 URL

    Attributes
    -----------
    icon: Final[str]
        유튜브 브랜드 아이콘 URL
    """

    def __init__(self, icon: str):
        self.icon: _Final[str] = icon
