from discord import File as _File

from ..core import Final as _Final
from ..core import Nullable as _Nullable
from ..instance.handlers.message.embed import Embed as _Embed


class LogUtils:
    """
    로그를 관리합니다.

    Parameters
    -----------
    prefix: str
        대상의 이름
    """

    def __init__(self, prefix: str) -> None:
        super().__init__()
        self._prefix: str = prefix

    def log(self, content: str) -> None:
        """
        로그를 출력합니다.

        Parameters
        ----------
        content: str
            출력할 내용
        """
        print(f"[{self._prefix}] {content}")


class HandledMessage:
    """
    인스턴스 자체 로거를 통해 로그할 수 있도록 처리된 정보입니다.

    Parameters
    -----------
    content: str
        로그 내용
    embed: Embed
        로그 내용을 포함한 Embed
    file: Optional[discord.File]
        로그 내용을 포함한 File

    Attributes
    -----------
    content: str
        로그 내용
    embed: Embed
        로그 내용을 포함한 Embed
    file: Optional[discord.File]
        로그 내용을 포함한 File
    """

    def __init__(self, content: str, embed: _Embed, file: _Nullable[_File] = None):
        self.content: _Final[str] = content
        self.embed: _Final[_Embed] = embed
        self.file: _Final[_Nullable[_File]] = file
