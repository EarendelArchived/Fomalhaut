from multiprocessing import Process as _Proc

from discord import Client as _Instance
from discord import TextChannel as _TextCh
from discord.flags import Intents as _Intents

from .LogUtils import HandledMessage as _Handled
from ..core import Final as _Final
from ..core import Nullable as _Nullable
from ...main.settings import Settings as _Settings


class ExternalLogger(_Instance):
    """
    로거 봇을 이용하여 채널에 로그합니다.

    Parameters
    -----------
    settings: dict
        로거 봇 설정
    handled: HandledMessage
        로그할 메시지
    """

    def __init__(
            self, settings: dict, handled: _Handled
    ) -> None:
        super().__init__(intents=_Intents.all())
        self._settings: _Final[dict] = settings
        self._handled: _Final[_Handled] = handled
        self.run(self._settings['token'])

    async def on_ready(self) -> None:
        await self.wait_until_ready()
        for i in self._settings['target'].send:
            target: _Nullable[_TextCh] = self.get_channel(i)
            if target is not None:
                await target.send(embed=self._handled.embed, file=self._handled.file)
        await self.close()


class ExternalLoggerHandler:
    """
    외부 로거 봇을 핸들링하는 클래스입니다.

    Parameters
    -----------
    settings: Settings
        메인 클래스 설정
    """

    def __init__(self, settings: _Settings) -> None:
        self._settings: dict = settings.instance.logger

    def throw(self, handled: _Handled) -> None:
        _Proc(target=ExternalLogger, args=(self._settings, handled,)).start()
