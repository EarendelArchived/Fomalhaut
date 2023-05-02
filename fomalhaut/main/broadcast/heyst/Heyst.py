from ..common.BasicTwitchInstance import BasicTwitchInstance as _Instance
from ...settings import Settings as _Settings
from ....module.api.youtube.YouTubeCache import YouTubeCache as _Cache
from ....module.api.youtube.YouTubeHandler import YouTubeHandler as _Handler
from ....module.core import Nullable as _Nullable
from ....module.instance import Itr as _Itr
from ....module.instance.handlers.message.embed import Embed as _Embed
from ....module.instance.handlers.message.embed import ColourElement as _Colour
from ....module.instance.handlers.ActivityHandler import ActivityHandler as _Activity


class Heyst(_Instance):
    """
    트위치 스트리머 Heyst님의 봇 인스턴스를 생성합니다.

    Parameters
    -----------
    settings: Settings
        설정
    """

    def __init__(self, settings: _Settings):
        self.yt_handler: _Nullable[_Handler] = None
        self.yt_cache: _Nullable[_Cache] = None
        super().__init__(settings, "Heyst", _Activity("dnd", "playing", "1처형 펜타킬"))

    async def on_ready(self) -> None:
        """
        인스턴스가 준비되면 호출됩니다.
        """
        self.yt_handler = _Handler(self, self.settings['youtube'], self.settings['profile_art'])
        await super().on_ready()

    def schedules(self) -> None:
        @self.schedule
        async def this() -> bool:
            return (await self.yt_handler.handle()).cache.success

    def commands(self) -> None:
        super().commands()

        @self.tree.get_command("send_manually").command(name="youtube", description="수동으로 영상 업로드 공지를 보냅니다.")
        async def this(i: _Itr) -> None:
            async def that() -> None:
                if (await self.yt_handler.handle(True)).cache.success:
                    await i.followup.send(
                        embed=_Embed(title="성공적으로 방송 알림을 보냈습니다.", colour=_Colour.green())
                    )
            await self.process(i, that)
