from datetime import datetime as _datetime
from json import dumps as _to_json
from json import JSONDecodeError as _JSONErr

from ..common.BasicAPICache import BasicAPICache as _Interface
from ...basicio.BasicIOHandler import BasicIOHandler as _Handler
from ...core import Any as _Any
from ...core import Self as _Self
from ...core import Final as _Final
from ...core import Nullable as _Nullable
from ...instance import Instance as _Instance
from ...instance.handlers.message.embed import Embed as _Embed

_start: _Final[str] = "start"
_id: _Final[str] = "id"
_embed: _Final[str] = "embed"


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
    id: list[list[int]]
        이전에 처리된 공지 메세지 ID 목록
    embed: Nullable[Embed]
        이전에 처리된 공지 메세지 임베드
    success: bool
        API 정상 작동 여부
    stream: bool
        방송 중 여부
    start: Optional[datetime]
        방송 시작 시간
    """

    def __init__(self, instance: _Instance, target: str, success: bool = True) -> None:
        super().__init__(
            instance, "TwitchCache", _Handler.from_cache(f"twitch/{target}", "data.json"),
            success
        )
        self.img_handler: _Handler = _Handler.from_cache(f"twitch/{target}", "img.png")
        self.id: list[list[int]] = []
        self.embed: _Nullable[_Embed] = None
        self.stream: bool = False
        self.start: _Nullable[_datetime] = None

        try:
            cache: _Nullable[dict] = self.handler.read()

            start: _Any = cache.get(_start)
            if type(start) == str:
                self.start = _datetime.fromisoformat(start)
            elif start is not None:
                raise TypeError(f"TwitchCache.{_start} is not str or None, but {type(start)}")

            cache_id: _Any = cache.get(_id)
            if type(cache_id) == list:
                self.id = cache_id
            elif cache_id is not None:
                raise TypeError(f"TwitchCache.{_id} is not list, but {type(cache_id)}")

            embed: _Any = cache.get(_embed)
            if type(embed) == dict:
                self.embed = _Embed.from_dict(embed)
            elif embed is not None:
                raise TypeError(
                    f"TwitchCache.{_embed} is not dict or None, but {type(embed)}"
                )
        except _JSONErr:
            print("Cached Json is corrupted or none, resetting.")
            self.handler.write(f'{{"{_start}": "{None}", "{_id}": [], "{_embed}": "{None}"}}')

    # Overrides
    async def fail(self) -> _Self:
        """
        API가 처리에 실패했음을 반환합니다.
        """
        self.embed = None
        self.id = []
        return await super().fail()

    async def update(
            self, start: _datetime, cache_id: _Nullable[list[list[int]]] = None, embed: _Nullable[_Embed] = None
    ) -> _Self:
        """
        캐시 정보를 업데이트합니다.

        Parameters
        ----------
        start: datetime
            방송 시작 시간
        cache_id: Optional[list[list[int]]]
            출력된 방송 공지 메세지의 ID 리스트
        embed: Optional[Embed]
            출력된 방송 공지 메세지의 임베드
        """
        self.id = self.id if cache_id is None else cache_id
        self.embed = self.embed if embed is None else embed
        self.stream = True
        self.start = start
        return await self.save()

    async def not_streaming(self) -> _Self:
        """
        방송 중이 아님을 반환합니다.
        """
        self.id = []
        self.embed = None
        self.stream = False
        return await self.save()

    async def save(self) -> _Self:
        """
        캐시를 저장합니다.
        """
        try:
            start: str = self.start.isoformat() if type(self.start) == _datetime else None
            embed: str = _to_json(self.embed.to_dict()) if type(self.embed) == _Embed else f"\"{None}\""
            self.handler.write(
                f'{{"{_start}": "{start}", "{_id}": {self.id}, "{_embed}": {embed}}}'
            )
        except Exception as e:
            self.success = False
            await self.throw(e, "save")
        return self
