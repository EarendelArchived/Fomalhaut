from os import environ

from ....module.core import Final as _Final
from ....module.core import Nullable as _Nullable


class EnvironmentHandler:
    """
    시스템 환경 변수를 캐시하고 읽어옵니다.
    """

    def __init__(self) -> None:
        self._environ: _Final[environ] = environ

    def get(self, key: str) -> str:
        """
        메모리에 캐시된 시스템 환경 변수를 읽어옵니다.

        Parameters
        ----------
        key: str
            읽어올 환경 변수의 키
        """
        var: _Nullable[str] = self._environ.get(key)
        if var is None:
            raise KeyError(f"Environment variable '{key}' not found")
        return var


class TokenComponent:
    """
    시스템 환경 변수에 캐시된 토큰을 읽어옵니다.

    Parameters
    -----------
    handler: EnvironmentHandler
        시스템 환경 변수 캐시 핸들러
    """

    def __init__(self, handler: EnvironmentHandler) -> None:
        super().__init__()
        self._handler: _Final[EnvironmentHandler] = handler

    def get(self, name: str, beta: bool = False) -> str:
        """
        시스템 환경 변수에 캐시된 토큰을 읽어옵니다.

        Parameters
        ----------
        name: str
            인스턴스의 이름
        beta: bool
            베타 버전 여부
        """
        return self._handler.get(f"BETA_TOKEN_{name.upper()}") if beta else self._handler.get(f"TOKEN_{name.upper()}")
