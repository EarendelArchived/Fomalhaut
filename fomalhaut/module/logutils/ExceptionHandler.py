from traceback import format_exception as _exc

from discord import File as _File

from .ExternalLoggerHandler import ExternalLoggerHandler as _ExtHandler
from .LogUtils import HandledMessage as _Handled
from .LogUtils import LogUtils as _LogUtils
from ..basicio import BasicIOHandler as _IOHandler
from ..core import Final as _Final
from ..core import Nullable as _Nullable
from ..core import Self as _Self
from ..instance import Instance as _Instance
from ..instance.handlers.message.embed import ColourElement as _Colour
from ..instance.handlers.message.embed import Embed as _Embed
from ..instance.handlers.message.embed import FieldElement as _Field
from ..instance.handlers.message.embed import FooterElement as _Footer
from ...main.settings import Settings as _Settings


class ExceptionHandler:
    """
    발생한 예외를 처리하고 로그를 출력합니다.

    Parameters
    -----------
    logger: LogUtils
        로거
    settings: Settings
        메인 핸들 설정
    """

    def __init__(self, logger: _LogUtils, settings: _Settings):
        self._logger: _Final[_Nullable[_LogUtils]] = logger
        self._thrower: _Final[_ExtHandler] = _ExtHandler(settings)
        self._handled: _Nullable[_Handled] = None

    def handle(
            self, exception: Exception, location: str, additional: _Nullable[_Field] = None, ignored: bool = False,
            instance: _Nullable[_Instance] = None
    ) -> _Self:
        """
        발생한 예외를 로그 가능하도록 처리합니다.

        Parameters
        ----------
        exception: Exception
            발생한 예외
        location: str
            예외가 발생한 위치
        additional: Optional[FieldElement]
            추가 필드
        ignored: bool
            예외가 무시되었는지 여부
        instance: Optional[Instance]
            예외가 발생한 인스턴스
        """
        e: str = "".join(_exc(exception))
        colour: _Colour = _Colour.yellow() if ignored else _Colour.red()

        log_content: str = (
            f"""!!! 예외 발생을 감지했습니다 !!!
            
            위치: {location}
            예외 타입: {str(type(exception))}
            상세 정보: {exception}
            무시 여부: {ignored}
            
            ########## Traceback ##########
            {e}
            """
        )

        file: _Nullable[_File] = None
        if len(e) > 1023:
            file = _IOHandler.as_attachment(e)
            e = "첨부 로그 파일을 참조하십시오"

        footer: _Nullable[_Footer] = None
        if instance is not None:
            footer = instance.footer

        self._handled = _Handled(
            content=log_content, embed=_Embed(
                title="예외 발생을 감지했습니다", colour=colour, desc=f"""
                > 발생 위치: `{location}`
                > 예외 타입: `{str(type(exception))}`
                > 상세 정보: `{exception}`
                > 무시 여부: `{ignored}`
                """, footer=footer, fields=[
                    _Field(title="Traceback", content=f"```\n{e}\n```", inline=False), additional
                ]
            ), file=file
        )
        return self

    def get(self) -> _Nullable[_Handled]:
        """
        처리된 예외를 반환합니다.
        """
        return self._handled

    def clear(self) -> None:
        """
        캐시된 예외를 초기화합니다.
        """
        self._handled = None

    def throw(self) -> None:
        """
        외부 로거를 통해 예외를 로그합니다.
        """
        self._logger.log(self._handled.content)
        self._thrower.throw(self._handled)
        self.clear()
