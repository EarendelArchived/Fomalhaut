from ..common.BasicNoticeInstance import BasicNoticeInstance as _Instance
from ...settings import Settings as _Settings
from ....module.api.youtube.YouTubeCache import YouTubeCache as _Cache
from ....module.api.youtube.YouTubeHandler import YouTubeHandler as _Handler
from ....module.core import Nullable as _Nullable
from ....module.instance import Itr as _Itr
from ....module.instance.handlers.message.embed import Embed as _Embed
from ....module.instance.handlers.message.embed import ColourElement as _Colour
from ....module.instance.handlers.ActivityHandler import ActivityHandler as _Activity


class MCC(_Instance):
    """
    MCC 공지봇 인스턴스를 생성합니다.

    Parameters
    -----------
    settings: Settings
        설정
    """

    def __init__(self, settings: _Settings):
        self.api_handler: _Nullable[_Handler] = None
        self.cache: _Nullable[_Cache] = None
        super().__init__(settings, "MCC", _Activity("dnd", "playing", "MCC에서 공지"))

    async def on_ready(self) -> None:
        """
        인스턴스가 준비되면 호출됩니다.
        """
        self.api_handler = _Handler(self, self.settings['youtube'])
        await super().on_ready()

    def schedules(self) -> None:
        @self.schedule
        async def this() -> bool:
            return (await self.api_handler.handle()).cache.success

    def commands(self) -> None:
        @self.tree.command(name="send_manually", description="수동으로 영상 업로드 공지를 보냅니다.")
        async def this(i: _Itr) -> None:
            async def that() -> None:
                if (await self.api_handler.handle(True)).cache.success:
                    await i.followup.send(embed=_Embed(
                        title="성공적으로 영상 업로드 알림을 보냈습니다.", colour=_Colour.green()
                    ))
            await self.process(i, that)
