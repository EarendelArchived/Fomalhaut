from ... import Instance as _Instance
from ...handlers.message.embed import FieldElement as _Field
from ....core import Final as _Final
from ....core import Nullable as _Nullable


class BasicThrowableInterface:
    """
    예외 발생 시 self.instance를 통해 예외를 로그할 수 있는 인터페이스입니다.

    Parameters
    -----------
    instance: Instance
        예외를 로그할 인스턴스
    name: str
        클래스 이름

    Attributes
    -----------
    instance: Instance
        예외를 로그할 인스턴스
    _name: str
        클래스 이름
    """

    def __init__(self, instance: _Instance, name: str) -> None:
        self.instance: _Final[_Instance] = instance
        self._name: _Final[str] = name

    async def throw(
            self, exception: Exception, location: str, additional: _Nullable[_Field] = None, ignored: bool = False
    ) -> None:
        """
        예외를 로그합니다.

        Parameters
        ----------
        exception: Exception
            로그할 예외
        location: str
            예외가 발생한 위치
        additional: Optional[FieldElement]
            추가로 로그할 필드
        ignored: bool
            예외 무시 여부
        """
        await self.instance.throw(exception, f"{self._name}.{location}", additional=additional, ignored=ignored)
