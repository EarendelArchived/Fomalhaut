from json import loads as _as_json
from json import dumps as _to_json
from os import makedirs as _md
from os.path import dirname as _dir
from os.path import exists as _exist

from discord import File as _File

from ..core import Or as _Or
from ..core import Self as _Self
from ..core import Enum as _Enum
from ..core import Final as _Final
from ..core import Nullable as _Nullable


class BasicIOHandler:
    """
    기본 파일 입출력을 제어합니다.

    Parameters
    -----------
    path: str
        파일 경로
    file: str
        파일 이름

    Attributes
    -----------
    path: str
        파일 경로
    """

    class FileType(_Enum):
        """
        파일을 읽어올 때 반환할 값의 형태를 정의합니다.

        Attributes
        -----------
        TEXT: int
            텍스트
        JSON: int
            JSON
        """
        TEXT = -1
        JSON = 0

    def __init__(self, path: str, file: str) -> None:
        path = f"{_dir(__file__)}/../../../{path}"
        self.path: _Final[str] = f"{path}/{file}"
        if not _exist(self.path):
            if not _exist(path):
                _md(path)
            open(self.path, 'x').close()

    def read(self, file_type: FileType = FileType.JSON) -> _Or[str, dict]:
        """
        파일 내용을 읽어옵니다.

        Parameters
        ----------
        file_type: FileType
            읽어온 파일의 값을 반환하는 형태
        """
        value: str
        with open(self.path, 'r') as f:
            value = f.read()
            f.close()

        match file_type:
            case self.FileType.TEXT:
                return value
            case self.FileType.JSON:
                return _as_json(value)
            case _:
                raise ValueError("Invalid read type")

    def readbyte(self) -> bytes:
        """
        바이너리 파일을 읽습니다.
        """
        value: bytes
        with open(self.path, 'rb') as f:
            value = f.read()
            f.close()
        return value

    def write(self, content: _Or[str, dict], file_type: _Nullable[FileType] = FileType.JSON) -> _Self:
        """
        파일을 씁니다.

        Parameters
        ----------
        content: Union[str, dict]
            파일에 쓸 내용
        file_type: Nullable[FileType]
            파일 형태
        """
        match file_type:
            case self.FileType.JSON:
                if type(content) != dict:
                    raise TypeError("Invalid content type")
                content = _to_json(content)
            case self.FileType.TEXT:
                if type(content) != str:
                    raise TypeError("Invalid content type")
            case _:
                raise ValueError("Invalid write type")

        with open(self.path, 'w') as f:
            f.write(content)
            f.close()
        return self

    def writebyte(self, content: bytes) -> _Self:
        """
        바이너리 파일을 씁니다.

        Parameters
        ----------
        content: bytes
            파일에 쓸 내용
        """
        with open(self.path, 'wb') as f:
            f.write(content)
            f.close()
        return self

    @classmethod
    def as_attachment(cls, content: str) -> _File:
        """
        문자열을 discord.File로 변환합니다.

        Parameters
        ----------
        content: str
            첨부 파일의 내용
        """
        return _File(
            cls.from_cache(".", "attachment.txt").write(content, cls.FileType.TEXT).path, filename="attachment.txt"
        )

    @classmethod
    def from_cache(cls, path: str, file: str) -> _Self:
        return cls(f".cache/{path}", file)
