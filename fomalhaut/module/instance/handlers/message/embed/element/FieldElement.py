from discord import Embed as _Embed

from ......core import Nullable as _Nullable


class FieldElement:
    """
    Embed에 Field를 추가합니다.

    Parameters
    -----------
    title: Optional[str]
        Field의 제목
    content: Optional[str]
        Field의 내용
    inline: bool
        여러 Field를 한 줄에 표시할지에 대한 여부

    Attributes
    -----------
    title: Optional[str]
        Field의 제목
    content: Optional[str]
        Field의 내용
    inline: bool
        여러 Field를 한 줄에 표시할지에 대한 여부
    """

    def __init__(self, title: _Nullable[str] = None, content: _Nullable[str] = None, inline: bool = False):
        self.title: _Nullable[str] = title
        self.content: _Nullable[str] = content
        self.inline: bool = inline

    def append(self, embed: _Embed) -> _Embed:
        """
        Field 객체를 Embed에 추가합니다

        Parameters
        ----------
        embed: Embed
            Field를 추가할 Embed 객체
        """
        return embed.add_field(name=self.title, value=self.content, inline=self.inline)
