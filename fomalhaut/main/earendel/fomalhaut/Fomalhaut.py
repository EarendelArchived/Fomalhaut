from discord import Guild as _Guild
from discord import ChannelType as _CHType
from discord import CategoryChannel as _CatCh
from discord.abc import GuildChannel as _GuildCh
from discord.app_commands import Group as _Group

from ...settings import Settings as _Settings
from ....module.core import Nullable as _Nullable
from ....module.etc.AsciiBuilder import to_gothic as _gothic
from ....module.instance import Instance as _Instance
from ....module.instance import Itr as _Itr
from ....module.instance.handlers.message.embed import Embed as _Embed
from ....module.instance.handlers.message.embed import ColourElement as _Colour
from ....module.instance.handlers.ActivityHandler import ActivityHandler as _Activity
from ....module.api.twitch.TwitchHandler import TwitchHandler as _TwitchHandler
from ....module.api.youtube.YouTubeMultiHandler import handleable as _handleable
from ....module.api.youtube.YouTubeMultiHandler import YouTubeMultiHandler as _Handler


class Fomalhaut(_Instance):
    """
    아쎄이!

    Parameters
    -----------
    settings: Settings
        설정
    """

    def __init__(self, settings: _Settings):
        self.handler: _Handler = _Handler(self)
        self.testhandler: _Nullable[_TwitchHandler] = None
        super().__init__(settings, "earendel", "Fomalhaut", _Activity("idle", "playing", "프로그래밍"))
        
    async def on_ready(self) -> None:
        @self.handler.append
        def this() -> _handleable():
            return "kurzgesagt", self.settings['kurzgesagt']['config']

        @self.handler.append
        def this() -> _handleable():
            return (
                "kurzgesagt_kr", self.settings['kurzgesagt_kr']['config']
            )

        @self.handler.append
        def this() -> _handleable():
            return "veritasium", self.settings['veritasium']['config']

        await super().on_ready()

    def schedules(self) -> None:
        @self.schedule
        async def this() -> bool:
            return await self.handler.handle("kurzgesagt")

        @self.schedule
        async def this() -> bool:
            return await self.handler.handle("kurzgesagt_kr")

        @self.schedule
        async def this() -> bool:
            return await self.handler.handle("veritasium")

    def commands(self) -> None:
        @self.tree.command(name="create", description="고딕을 이름으로 한 채널을 생성합니다.")
        async def this(
                i: _Itr, name: str, ch_type: _CHType, reason: str, category: _CatCh = None, position: int = None
        ) -> None:
            async def that() -> None:
                async def make() -> _Nullable[_GuildCh]:
                    g: _Guild = i.guild
                    n: str = _gothic(name)
                    match ch_type:
                        case _CHType.text:
                            return await g.create_text_channel(n, reason=reason, category=category, position=position)
                        case _CHType.voice:
                            return await g.create_voice_channel(n, reason=reason, category=category, position=position)
                        case _CHType.category:
                            return await g.create_category(n, reason=reason, position=position)
                        case _CHType.news:
                            return await g.create_text_channel(n, reason=reason, category=category, news=True)
                        case _CHType.stage_voice:
                            return await g.create_stage_channel(n, reason=reason, category=category, position=position)
                        case _CHType.forum:
                            return await g.create_forum(n, reason=reason, position=position, category=category)
                        case _:
                            await i.followup.send(embed=_Embed(
                                title="잘못된 채널 형태를 입력받았습니다!",
                                desc=f"`{ch_type}` 은(는) 존재하지 않거나 지원하지 않는 채널 형태입니다.",
                                colour=_Colour.red()
                            ))
                            return

                result: _Nullable[_GuildCh] = await make()
                if result is not None:
                    await i.followup.send(f"{result.mention} 을(를) 생성했습니다.")
            await self.process(i, that)

        @self.group("send_manually", "수동으로 영상 공지를 전송합니다.")
        def this(g: _Group) -> None:
            async def process_manual_send(i: _Itr, target: str) -> None:
                if await self.handler.handle(target, True):
                    await i.followup.send(embed=_Embed(
                            title="성공적으로 영상 업로드 알림을 보냈습니다.", colour=_Colour.green()
                        ))

            @g.command(name="kurzgesagt", description="쿠르츠게작트 메인 채널 영상 알림을 전송합니다.")
            async def that(i: _Itr) -> None:
                async def main() -> None:
                    await process_manual_send(i, "kurzgesagt")
                await self.process(i, main)

            @g.command(name="kurzgesagt_kr", description="쿠르츠게작트 한국 채널 영상 알림을 전송합니다.")
            async def that(i: _Itr) -> None:
                async def main() -> None:
                    await process_manual_send(i, "kurzgesagt_kr")
                await self.process(i, main)

            @g.command(name="veritasium", description="베리타시움 한국 채널 영상 알림을 전송합니다.",)
            async def that(i: _Itr) -> None:
                async def main() -> None:
                    await process_manual_send(i, "veritasium")
                await self.process(i, main)
