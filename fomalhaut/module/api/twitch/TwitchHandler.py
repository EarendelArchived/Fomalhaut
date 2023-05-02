from datetime import datetime as _datetime

from discord import File as _Attachment

from .TwitchCache import TwitchCache as _Cache
from .TwitchListener import TwitchListener as _Listener
from ...core import Final as _Final
from ...core import Nullable as _Nullable
from ...datetime import Timezone as _Timezone
from ...datetime import calculateable_with_iso as _iso
from ...datetime import strfdelta as _strfdelta
from ...instance import Instance as _Instance
from ...instance.handlers.interface.BasicInterface import BasicThrowableInterface as _Interface
from ...instance.handlers.message.embed import AuthorElement as _Author
from ...instance.handlers.message.embed import ColourElement as _Colour
from ...instance.handlers.message.embed import Embed as _Embed
from ...instance.handlers.message.embed import FieldElement as _Field


class TwitchHandler(_Interface):
    """
    트위치 API를 통해 방송 정보를 가져오는 핸들러입니다.

    Parameters
    -----------
    instance: Instance
        인스턴스

    Attributes
    -----------
    _listener: Listener
        트위치 API 리스너
    """

    def __init__(self, instance: _Instance):
        super().__init__(instance, "TwitchHandler")
        self._listener: _Final[_Listener] = _Listener(instance)

    async def _handle_not_streaming(self, cache: _Cache) -> _Cache:
        """
        방송이 종료되었을 때 임베드를 수정합니다.

        Parameters
        ----------
        cache: TwitchCache
            캐시
        """
        try:
            if not cache.handled_id and cache.start is not None:
                await self.instance.send_to(
                    "", edit_target=cache.handled_id,
                    embed=_Field(
                        "종료", _Timezone.KST.apply(_datetime.now()).strftime("%Y년 %m월 %d일 %p %I:%M:%S")
                    ).append(
                        _Field(
                            "업타임", _strfdelta(_iso(_datetime.now()) - cache.start)
                        ).append(cache.handled_embed)
                    )
                )
            return await cache.not_streaming()
        except Exception as e:
            await self.throw(e, "handle.notStreaming")
            return await cache.fail()

    async def handle(self, cache: _Cache, force: bool = False) -> _Cache:
        """
        API 리스너를 통해 방송 정보를 공지합니다.

        Parameters
        ----------
        cache: TwitchCache
            캐시
        force: bool
            강제 공지 여부
        """
        try:
            try:
                handled: dict = await self._listener.handle()
            except Exception as e:
                await self.throw(e, "handle.getResponse")
                return await cache.fail()

            try:
                handled = handled["data"][0]
            except (KeyError, IndexError):
                return await self._handle_not_streaming(cache)
            except Exception as e:
                await self.throw(e, "handle.handleResponse")
                return await cache.fail()
            else:
                if handled["type"] != 'live':
                    return await self._handle_not_streaming(cache)

                start: _datetime = _datetime.fromisoformat(handled["started_at"])
                settings: dict = self.instance.settings

                flag: bool = type(cache.start) is _datetime and start > cache.start

                if flag or force:
                    embed: _Embed = _Embed(
                        title=handled["title"], url=f"https://twitch.tv/{settings['twitch'].target}",
                        colour=_Colour(0x9147FF), profile=settings['profile_art'], footer=self.instance.footer,
                        author=_Author(
                            handled['user_name'],
                            f"https://twitch.tv/{settings['twitch'].target}",
                            self._listener.settings.icon
                        ),
                        fields=[
                            _Field("시작", _Timezone.KST.apply(start).strftime("%Y년 %m월 %d일 %p %I:%M:%S")),
                            _Field("게임", handled['game_name'], True),
                            _Field("시청자 수", handled['viewer_count'], True),
                            _Field("태그", ", ".join(handled['tags']))
                        ]
                    )

                    message = settings['twitch'].message
                    if message != "":
                        message += "\n"
                    message += f"https://twitch.tv/{settings['twitch'].target}"

                    return await cache.update(start, await self.instance.send_to(
                        message, settings['twitch'].send, embed=embed, file=(await self._handle_img(cache))
                    ), embed)

                return await cache.update(start)
        except Exception as e:
            await self.throw(e, "handle")
            return await cache.fail()

    async def _handle_img(self, cache: _Cache) -> _Nullable[_Attachment]:
        """
        트위치 API에서 방송 이미지를 가져와 저장합니다.

        Parameters
        ----------
        cache: TwitchCache
            캐시
        """
        try:
            target: str = self.instance.settings['twitch'].target
            cache.img_handler.writebyte(await self._listener.handler.handle(
                f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{target}-1920x1080.jpg",
                return_type=self._listener.handler.ReturnType.BYTE
            ))
            return _Attachment(cache.img_handler.path, "attachment.png")
        except Exception as e:
            await self.throw(e, "handleImg")
            return None
