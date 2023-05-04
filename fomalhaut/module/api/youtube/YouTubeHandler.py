from datetime import datetime as _datetime

import bs4 as _bs
from discord import File as _Attachment

from .YouTubeCache import YouTubeCache as _Cache
from ..common.BasicWebHandler import BasicWebHandler as _Handler
from ...basicio import BasicIOHandler as _IOHandler
from ...core import Self as _Self
from ...core import Final as _Final
from ...core import Nullable as _Nullable
from ...instance import Instance as _Instance
from ...instance.handlers.interface.BasicInterface import BasicThrowableInterface as _Interface
from ...instance.handlers.message.embed import Embed as _Embed
from ...instance.handlers.message.embed.element import AuthorElement as _Author
from ...instance.handlers.message.embed.element import ColourElement as _Colour
from ...instance.handlers.message.embed.element import FieldElement as _Field
from ....main.settings.component import YouTubeComponent as _Target
from ....main.settings.component import BaseYouTubeComponent as _Settings


class YouTubeHandler(_Interface):
    """
    유튜브 API를 통해 영상 정보를 가져오는 핸들러입니다.

    Parameters
    -----------
    instance: Instance
        인스턴스
    """

    def __init__(self, instance: _Instance, target: _Target):
        super().__init__(instance, "YouTubeListener")
        self._settings: _Final[_Settings] = instance.main.api.youtube
        self._handler: _Final[_Handler] = _Handler(instance)
        self._null: _Final[bytes] = _IOHandler("fomalhaut/module/api/youtube", "null.png").readbyte()
        self.cache: _Cache = _Cache(instance, target)

        self._target: _Final[_Target] = target
        self._rss: _Final[str] = f"https://www.youtube.com/feeds/videos.xml?channel_id=UC{target.target}"

    async def _handle_thumbnail(self, video_id: str, cache: _Cache) -> _Nullable[_Attachment]:
        """
        영상 ID에 대한 유효한 썸네일을 가져와 첨부 파일로 변환합니다.

        Parameters
        -----------
        video_id: str
            영상 ID
        cache: YouTubeCache
            캐시
        """
        try:
            url: str = f"https://img.youtube.com/vi/{video_id}"
            handled: bytes = await self._handler.handle(
                f"{url}/maxresdefault.jpg", return_type=self._handler.ReturnType.BYTE
            )

            if handled == self._null:
                handled = await self._handler.handle(f"{url}/hqdefault.jpg", return_type=self._handler.ReturnType.BYTE)

            cache.thumbnail_handler.writebyte(handled)
            return _Attachment(cache.thumbnail_handler.path, filename="attachment.jpg")
        except Exception as e:
            await self.instance.throw(e, "handle.thumbnail")
            return

    async def handle(self, force: bool = False) -> _Self:
        """
        유튜브 API에서 정보를 불러와 처리합니다.

        Parameters
        ----------
        force: Optional[bool]
            강제 게시 여부
        """
        try:
            try:
                response: _bs.element.Tag = (
                    await self._handler.handle(self._rss, return_type=self._handler.ReturnType.SOUP)
                ).feed.entry
            except Exception as e:
                await self.throw(e, "handle.getResponse")
                await self.cache.fail()
                return self

            try:
                video_id: str = response.id.get_text().split(":")[-1]
                upload_date: _datetime = _datetime.fromisoformat(response.published.get_text())
            except Exception as e:
                await self.throw(e, "handle.getVideoInfo")
                await self.cache.fail()
                return self

            try:
                cache: _Cache = self.cache
                if (
                        (video_id != cache.video_id and
                         (type(cache.upload_date) == _datetime and upload_date > cache.upload_date))
                        or force
                ):
                    embed: _Embed = _Embed(
                        title=response.title.get_text(), url=f"https://youtu.be/{video_id}", colour=_Colour(0xFD0000),
                        desc=self._target.description, profile=self._target.profile_art,
                        image="attachment://attachment.jpg", footer=self.instance.footer, author=_Author(
                            content=response.author.find("name").get_text(),
                            url=f"https://www.youtube.com/@{self._target.target_id}", icon=self._settings.icon
                        ), fields=[
                            _Field("업로드", upload_date.strftime("%Y년 %m월 %d일 %p %I:%M:%S"), True),
                            _Field("조회수", response.find("media:statistics").get("views"), True),
                            _Field("좋아요", response.find("media:starRating").get("count"), True)
                        ]
                    )

                    message: str = self._target.message
                    if message != "":
                        message += "\n"
                    message += f"https://youtu.be/{video_id}"

                    await cache.update(video_id, upload_date)
                    await self.instance.send_to(
                        message, self._target.send, embed=embed,
                        file=(await self._handle_thumbnail(video_id, cache))
                    )
                else:
                    await cache.update(video_id, upload_date)
                self.cache = cache
                return self
            except Exception as e:
                await self.throw(e, "handle.send")
                await self.cache.fail()
                return self
        except Exception as e:
            await self.throw(e, "handle")
            await self.cache.fail()
            return self
