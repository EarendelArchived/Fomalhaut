from datetime import datetime

from discord import Embed as _Embed

from .element import AuthorElement as _Author
from .element import ColourElement as _Color
from .element import FieldElement as _Field
from .element import FooterElement as _Footer
from .....core import Self as _Self
from .....core import Nullable as _Nullable


class Embed(_Embed):
    """
    Embed를 생성합니다.

    Parameters
    -----------
    title: Optional[str]
        Embed 제목
    desc: Optional[str]
        Embed 설명
    url: Optional[str]
        Embed 제목 클릭 시 이동하는 URL
    colour: Optional[Colour]
        Embed 색상
    image: Optional[str]
        Embed 이미지
    profile: Optional[str]
        Embed 프로필 이미지
    timestamp: DateTime
        Embed 타임스탬프
    author: Optional[Author]
        Embed 작성자
    footer: Optional[Footer]
        Embed Footer
    fields: Optional[list[Field]]
        Embed 필드
    """

    def __init__(
            self, title: _Nullable[str] = None, desc: _Nullable[str] = None, url: _Nullable[str] = None,
            colour: _Nullable[_Color] = None, image: _Nullable[str] = "attachment://attachment.png",
            profile: _Nullable[str] = None, timestamp: datetime = datetime.now(), author: _Nullable[_Author] = None,
            footer: _Nullable[_Footer] = None, fields: _Nullable[list[_Field]] = None
    ):
        super().__init__(
            colour=colour, title=title, url=url, timestamp=timestamp, description=desc
        )

        self.set_image(url=image).set_thumbnail(url=profile)

        if author is not None:
            author.append(self)

        if footer is not None:
            footer.append(self)

        if fields is not None:
            for i in fields:
                if i is not None:
                    i.append(self)

    @classmethod
    def from_dict(cls, data: dict) -> _Self:
        return super().from_dict(data)

    def to_dict(self) -> dict:
        return super().to_dict()
