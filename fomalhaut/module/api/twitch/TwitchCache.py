from datetime import datetime as _datetime
from json import JSONDecodeError as _JSONErr

from ..common.BasicAPICache import BasicAPICache as _Interface
from ...basicio.BasicIOHandler import BasicIOHandler as _Handler
from ...core import Nullable as _Nullable
from ...core import Self as _Self
from ...instance import Instance as _Instance
from ...instance.handlers.message.embed import Embed as _Embed


class TwitchCache(_Interface):
    """
    트위치 API의 캐시 정보를 관리합니다.

    Parameters
    -----------
    instance: Instance
        인스턴스
    success: bool
        API 정상 작동 여부

    Attributes
    -----------
    img_handler: BasicIOHandler
        썸네일 이미지를 관리하는 핸들러
    handled_id: list[list[int]]
        이전에 처리된 공지 메세지 ID 목록
    handled_embed: Nullable[Embed]
        이전에 처리된 공지 메세지 임베드
    success: bool
        API 정상 작동 여부
    stream: bool
        방송 중 여부
    start: Optional[datetime]
        방송 시작 시간
    """

    def __init__(self, instance: _Instance, success: bool = True) -> None:
        super().__init__(
            instance, "TwitchCache", _Handler.from_cache(f"twitch/{instance.settings['twitch'].target}", "data.json"),
            success
        )
        self.img_handler: _Handler = _Handler.from_cache(f"twitch/{instance.settings['twitch'].target}", "img.png")
        self.handled_id: list[list[int]] = []
        self.handled_embed: _Nullable[_Embed] = None
        self.stream: bool = False
        self.start: _Nullable[_datetime] = None

        try:
            cache: _Nullable[dict] = self.handler.read()

            if type(cache.get("start")) == _datetime:
                self.start = cache['start']
            elif type(cache.get("start")) is not None:
                raise TypeError("TwitchCache.start is not datetime or None")

            if type(cache.get("handled_id")) == list:
                self.handled_id = cache['handled_id']
            else:
                raise TypeError("TwitchCache.handled_id is not list")

            if type(cache.get("handled_embed")) == _Embed:
                self.handled_embed = cache['handled_embed']
            elif type(cache.get("handled_embed")) is not None:
                raise TypeError("TwitchCache.handled_embed is not Embed or None")
        except _JSONErr:
            self.handler.write(f'{{"start": {None}, "handled_id": [], "handled_embed": {None}}}')

    # Overrides
    async def fail(self) -> _Self:
        """
        API가 처리에 실패했음을 반환합니다.
        """
        self.handled_embed = None
        self.handled_id = []
        return await super().fail()

    async def update(
            self, start: _datetime, msg_id: list[list[int]] = None, embed: _Embed = None
    ) -> _Self:
        """
        캐시 정보를 업데이트합니다.

        Parameters
        ----------
        start: datetime
            방송 시작 시간
        msg_id: Optional[list[list[int]]]
            출력된 방송 공지 메세지의 ID 리스트
        embed: Optional[Embed]
            출력된 방송 공지 메세지의 임베드
        """
        self.handled_id = [] if msg_id is None else msg_id
        self.handled_embed = embed
        self.stream = True
        self.start = start
        return await self.save()

    async def not_streaming(self) -> _Self:
        """
        방송 중이 아님을 반환합니다.
        """
        self.handled_id = []
        self.handled_embed = None
        self.stream = False
        return await self.save()

    async def save(self) -> _Self:
        """
        캐시를 저장합니다.
        """
        try:
            start: str = self.start.isoformat() if type(self.start) == _datetime else None
            self.handler.write(f'{{"start": "{start}", "id": {self.handled_id}, "embed": "{self.handled_embed}"}}')
        except Exception as e:
            self.success = False
            await self.throw(e, "save")
        return self
