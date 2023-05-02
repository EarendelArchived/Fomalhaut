from ....module.core import Final as _Final


class MinecraftVersionControl:
    """
    Minecraft: Java Edition의 최신 버전을 관리하는 설정 요소입니다.

    Parameters
    -----------
    major: str
        최신 메이저 버전
    minor: int
        최신 마이너 버전

    Attributes
    -----------
    major: Final[str]
        최신 메이저 버전
    minor: Final[int]
        최신 마이너 버전
    """

    def __init__(self, major: str, minor: int) -> None:
        self.major: _Final[str] = major
        self.minor: _Final[int] = minor
