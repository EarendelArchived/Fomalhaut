from discord import Embed as _Embed

from ......core import Nullable as _Nullable


class AuthorElement:
    """
    Embed에 Author를 추가합니다.

    Parameters
    -----------
    content: Optional[str]
        Author의 내용
    url: Optional[str]
        Author 클릭시 이동하는 URL
    icon: Optional[str]
        Author 아이콘 URL

    Attributes
    -----------
    content: Optional[str]
        Author의 내용
    url: Optional[str]
        Author 클릭시 이동하는 URL
    icon: Optional[str]
        Author 아이콘 URL
    """

    def __init__(self, content: _Nullable[str] = None, url: _Nullable[str] = None, icon: _Nullable[str] = None):
        self.content: _Nullable[str] = content
        self.url: _Nullable[str] = url
        self.icon: _Nullable[str] = icon

    def append(self, embed: _Embed) -> _Embed:
        """
        Author 객체를 Embed에 추가합니다

        Parameters
        ----------
        embed: Embed
            Author를 추가할 Embed 객체
        """
        return embed.set_author(name=self.content, url=self.url, icon_url=self.icon)
