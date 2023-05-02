from discord import Member as _Member
from discord import VoiceChannel as _VoiceCh

from ...settings import Settings as _Settings
from ....module.instance import Itr as _Itr
from ....module.instance import Instance as _Instance
from ....module.instance.handlers.message.embed import Embed as _Embed
from ....module.instance.handlers.message.embed import FieldElement as _Field
from ....module.instance.handlers.message.embed import ColourElement as _Colour
from ....module.instance.handlers.ActivityHandler import ActivityHandler as _Activity


class Earendel(_Instance):
    """
    지금 무슨 노래 듣고 계세요?
    뉴진스의 하입보이요

    Parameters
    -----------
    settings: Settings
        설정
    """

    def __init__(self, settings: _Settings):
        super().__init__(settings, "earendel", "Earendel", _Activity("idle", "playing", "프로그래밍"))

    def commands(self) -> None:
        @self.tree.command(name="what_song", description="지금 무슨 노래 듣고 계세요?")
        async def this(i: _Itr) -> None:
            await self.process(i, i.followup.send("뉴진스의 하입보이요"))

        @self.tree.command(name="mention_everyone", description="통화방에 접속하지 않은 모든 멤버분들을 DM으로 멘션합니다.")
        async def this(i: _Itr, ch: _VoiceCh) -> None:
            async def that() -> None:
                connected: list[_Member] = ch.members
                mentioned: list[_Member] = []
                for j in i.guild.members:
                    if not j.bot and j != self.user and j not in connected:
                        await j.send(f"{j.mention} 회의가 진행중이에요!")
                        mentioned.append(j)
                await i.followup.send(_Embed(
                    title="접속하지 않은 모든 멤버를 멘션했어요.", colour=_Colour.green(), fields=[
                        _Field("멘션한 멤버", ", ".join([j.mention for j in mentioned]) or "없음", inline=False)
                    ]
                ))
            await self.process(i, that)
