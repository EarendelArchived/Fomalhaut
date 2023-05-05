from datetime import datetime as _datetime
from json import JSONDecodeError as _JSONErr

from ..common.BasicAPICache import BasicAPICache as _Interface
from ...basicio.BasicIOHandler import BasicIOHandler as _Handler
from ...core import Self as _Self
from ...core import Final as _Final
from ...core import Nullable as _Nullable
from ...instance import Instance as _Instance
from ....main.settings.component.YouTubeComponent import YouTubeComponent as _Target

_video_id: _Final[str] = "video_id"
_upload_date: _Final[str] = "upload_date"


class YouTubeCache(_Interface):
    """
    유튜브 API의 캐시 정보를 관리합니다.

    Parameters
    -----------
    instance: Instance
        인스턴스
    success: Optional[bool]
        API 정상 작동 여부

    Attributes
    -----------
    thumbnail_handler: BasicIOHandler
        썸네일 이미지를 관리하는 핸들러
    video_id: Nullable[str]
        최신 비디오 ID
    upload_date: Nullable[datetime]
        최신 비디오의 업로드 날짜
    """

    def __init__(self, instance: _Instance, target: _Target, success: bool = True) -> None:
        super().__init__(
            instance, "YouTubeCache",
            _Handler.from_cache(f"youtube/{target.target}", "data.json"), success
        )
        self.thumbnail_handler: _Handler = _Handler.from_cache(
            f"youtube/{target.target}", "thumbnail.png"
        )
        self.video_id: _Nullable[str] = None
        self.upload_date: _Nullable[_datetime] = None

        try:
            cache: _Nullable[dict] = self.handler.read()
            if cache is not None:
                self.video_id = cache[_video_id]
                self.upload_date = cache[_upload_date]
        except (KeyError, _JSONErr):
            self.handler.write({_video_id: None, _upload_date: None})

    async def update(self, video_id: str, upload_date: _datetime) -> _Self:
        """
        캐시 정보를 업데이트합니다.

        Parameters
        ----------
        video_id: str
            핸들링된 비디오의 ID
        upload_date: str
            핸들링된 비디오의 업로드 날짜
        """
        self.success = True
        self.video_id = video_id
        self.upload_date = upload_date
        return await self.save()

    async def save(self) -> _Self:
        """
        캐시를 저장합니다
        """
        try:
            video_id: _Nullable[str] = self.video_id if type(self.video_id) == str else None
            upload_date: _Nullable[str] = self.upload_date.isoformat() if type(self.upload_date) == _datetime else None
            self.handler.write({_video_id: video_id, _upload_date: upload_date})
        except Exception as e:
            self.success = False
            await self.instance.throw(e, "save")
        return self
