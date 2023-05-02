from multiprocessing import Process as _Proc

from . import Callable as _Callable
from . import Final as _Final
from ..instance import Instance as _Instance
from ...main.settings import Settings as _Settings


class Runtime:
    """
    인스턴스 프로세스를 관리합니다.

    Parameters
    -----------
    settings: Settings
        인스턴스 전역 설정
    """

    def __init__(self, settings: _Settings) -> None:
        self._settings: _Final[_Settings] = settings

    def start(self, target: _Callable[_Instance]) -> None:
        """
        인스턴스 프로세스를 시작합니다.

        Parameters
        ----------
        target: Callable[Instance]
            시작할 인스턴스의 메인 클래스
        """
        _Proc(target=target, args=(self._settings,)).start()
