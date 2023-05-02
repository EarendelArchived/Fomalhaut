from discord.app_commands import Group as _Group

from ...settings import Settings as _Settings
from ....module.api.twitch.TwitchCache import TwitchCache as _Cache
from ....module.api.twitch.TwitchHandler import TwitchHandler as _APIHandler
from ....module.core import Nullable as _Nullable
from ....module.instance import Itr as _Itr
from ....module.instance import Instance as _Instance
from ....module.instance.handlers.message.embed import Embed as _Embed
from ....module.instance.handlers.message.embed import ColourElement as _Colour
from ....module.instance.handlers.ActivityHandler import ActivityHandler as _Activity


class BasicTwitchInstance(_Instance):
    """
    일반 Twitch 인스턴스를 생성합니다.

    Parameters
    -----------
    settings: Settings
        설정
    name: str
        인스턴스 이름
    activity: ActivityHandler
        활동 핸들러

    Attributes
    -----------
    api_handler: Optional[TwitchHandler]
        API 핸들러
    cache: Optional[TwitchCache]
        캐시
    """

    def __init__(
            self, settings: _Settings, name: str, activity: _Activity
    ):
        self.api_handler: _Nullable[_APIHandler] = None
        self.cache: _Nullable[_Cache] = None
        super().__init__(settings, "broadcast", name, activity)

    async def on_ready(self) -> None:
        """
        인스턴스가 준비되면 호출됩니다.
        """
        try:
            self.api_handler = _APIHandler(self)
            self.cache = _Cache(self)
            await super().on_ready()
        except Exception as e:
            await self.throw(e, "ready")

    async def handle_api(self, force: bool = False) -> _Cache:
        """
        API를 호출합니다.

        Parameters
        -----------
        force: Optional[bool]
            강제 출력 여부
        """
        self.cache = await self.api_handler.handle(self.cache, force=force)
        return self.cache

    def schedules(self) -> None:
        @self.schedule
        async def this() -> bool:
            return (await self.handle_api()).success

    def commands(self) -> None:
        @self.group("send_manually", "수동으로 공지사항을 전송합니다.")
        def this(g: _Group) -> None:
            @g.command(name="twitch", description="수동으로 방송 공지사항을 보냅니다.")
            async def that(i: _Itr) -> None:
                async def main() -> None:
                    await self.handle_api(True)
                    if self.cache.success:
                        if self.cache.stream:
                            await i.followup.send(embed=_Embed(
                                title="성공적으로 방송 알림을 보냈습니다.", colour=_Colour.green()
                            ))
                        else:
                            await i.followup.send(embed=_Embed(
                                title="방송 중이 아닙니다.", colour=_Colour.yellow()
                            ))
                await self.process(i, main)
