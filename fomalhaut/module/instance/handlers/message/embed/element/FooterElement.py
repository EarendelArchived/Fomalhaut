from discord import Embed as _Embed

from ......core import Nullable as _Nullable


class FooterElement:
    """
    Embed에 Footer를 추가합니다.

    Parameters
    -----------
    content: Optional[str]
        Footer의 내용
    icon: Optional[str]
        Footer 아이콘 URL

    Attributes
    -----------
    content: Optional[str]
        Footer의 내용
    icon: Optional[str]
        Footer 아이콘 URL
    """

    def __init__(self, content: _Nullable[str] = None, icon: _Nullable[str] = None):
        self.content: _Nullable[str] = content
        self.icon: _Nullable[str] = icon

    def append(self, embed: _Embed) -> _Embed:
        """
        Footer 객체를 Embed에 추가합니다

        Parameters
        ----------
        embed: Embed
            Footer를 추가할 Embed 객체
        """
        return embed.set_footer(text=self.content, icon_url=self.icon)
