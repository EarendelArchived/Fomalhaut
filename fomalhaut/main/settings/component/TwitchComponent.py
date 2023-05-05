from .TokenComponent import EnvironmentHandler
from ....module.core import Final as _Final
from ....module.core import Self as _Self


class TwitchComponent:
    """
    트위치 설정 요소입니다.

    Parameters
    -----------
    target: str
        처리할 트위치 채널 ID
    profile_art: str
        트위치 채널 프로필 이미지 URL
    message: str
        트위치 채널이 스트리밍 중일 때
        Embed와 함께 보낼 메시지
    offline: str
        트위치 채널이 스트리밍 중이 아닐 때
    send: list[int]
        트위치 채널이 스트리밍 중일 때
        메세지를 보낼 채널 ID 리스트

    Attributes
    -----------
    target: Final[str]
        처리할 트위치 채널 ID
    profile_art: Final[str]
        트위치 채널 프로필 이미지 URL
    message: Final[str]
        트위치 채널이 스트리밍 중일 때
        Embed와 함께 보낼 메시지
    offline: Final[str]
        트위치 채널이 스트리밍 중이 아닐 때
    send: Final[list[int]]
        트위치 채널이 스트리밍 중일 때
        메세지를 보낼 채널 ID 리스트

    """

    def __init__(
            self,
            target: str,
            profile_art: str,
            message: str,
            offline: str,
            send: list[int]
    ) -> None:
        self.target: _Final[str] = target
        self.profile_art: _Final[str] = profile_art
        self.message: _Final[str] = message
        self.offline: _Final[str] = offline
        self.send: _Final[list[int]] = send


class BaseTwitchComponent:
    """
    전역 트위치 설정 요소입니다.

    Parameters
    -----------
    cli_id: str
        트위치 API 클라이언트 ID
    secret: str
        트위치 API 보안 키
    icon: str
        트위치 브랜드 아이콘 URL

    Attributes
    -----------
    cli_id: Final[str]
        트위치 API 클라이언트 ID
    secret: Final[str]
        트위치 API 보안 키
    icon: Final[str]
        트위치 브랜드 아이콘 URL
    """

    def __init__(
            self, cli_id: str, secret: str, icon: str
    ) -> None:
        self.cli_id: _Final[str] = cli_id
        self.secret: _Final[str] = secret
        self.icon: _Final[str] = icon

    @classmethod
    def default(cls, handler: EnvironmentHandler, icon: str) -> _Self:
        """
        시스템 환경 변수에 캐시된 전역 트위치 설정 요소를 읽어옵니다.

        Parameters
        ----------
        handler: EnvironmentHandler
            시스템 환경 변수 캐시 핸들러
        icon: str
            트위치 브랜드 아이콘 URL
        """
        return cls(
            handler.get("TWITCH_CLI_ID"),
            handler.get("TWITCH_SECRET"),
            icon
        )
