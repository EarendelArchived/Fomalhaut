from ...basicio.BasicIOHandler import BasicIOHandler as _Handler
from ...core import Final as _Final
from ...core import Self as _Self
from ...instance import Instance as _Instance
from ...instance.handlers.interface.BasicInterface import BasicThrowableInterface as _Interface


class BasicAPICache(_Interface):
    """
    API 캐시를 관리하는 클래스의 인터페이스 입니다.

    Parameters
    -----------
    instance: Instance
        인스턴스
    name: str
        캐시 대상 API 이름
    handler: BasicIOHandler
        캐시를 관리하는 핸들러

    Attributes
    -----------
    handler: BasicIOHandler
        캐시를 관리하는 핸들러
    success: bool
        API의 정상 작동 여부
    """

    def __init__(self, instance: _Instance, name: str, handler: _Handler, success: bool = True) -> None:
        super().__init__(instance, name)
        self.handler: _Final[_Handler] = handler
        self.success: bool = success

    async def fail(self) -> _Self:
        """
        API가 처리에 실패했음을 반환합니다.
        """
        self.success = False
        return await self.save()

    async def save(self) -> _Self:
        """
        (DummyFunction) 캐시를 저장합니다.
        """
        return self
