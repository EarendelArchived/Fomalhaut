from json import loads as _json
from socket import gaierror as _socketerr

import requests as _request
from bs4 import BeautifulSoup as _Soup
from urllib3 import exceptions as _urlexc

from ...core import Enum as _Enum
from ...core import Final as _Final
from ...core import Nullable as _Nullable
from ...core import Or as _Or
from ...instance import Instance as _Instance
from ...instance.handlers.interface.BasicInterface import BasicThrowableInterface as _Interface


class BasicWebHandler(_Interface):
    """
    웹 요청을 처리합니다.

    Parameters
    -----------
    instance: Instance
        인스턴스

    Attributes
    -----------
    _session: requests.Session
        웹패킷 요청 세션
    """

    class HandleType(_Enum):
        """
        웹 요청 타입입니다.

        Attributes
        -----------
        GET: int
            GET 요청
        POST: int
            POST 요청
        """
        GET = 0
        POST = 1

    class ReturnType(_Enum):
        """
        웹 요청 결과 타입입니다.

        Attributes
        -----------
        TEXT: int
            텍스트
        JSON: int
            JSON
        SOUP: int
            BeautifulSoup
        BYTE: int
            바이트
        """
        TEXT = -1
        JSON = 0
        SOUP = 1
        BYTE = 2

    def __init__(self, instance: _Instance):
        super().__init__(instance, "BasicWebHandler")
        self._session: _Final[_request] = _request.Session()

    async def handle(
            self, url: str, handle_type: HandleType = HandleType.GET, return_type: ReturnType = ReturnType.JSON,
            header: _Nullable[dict] = None
    ) -> _Nullable[_Or[str, dict, bytes, _Soup]]:
        """
        웹 요청을 처리합니다.

        Parameters
        ----------
        url: str
            요청할 URL
        handle_type: HandleType
            요청 타입
        return_type: ReturnType
            반환 타입
        header: Optional[dict]
            요청 헤더
        """
        try:
            handled: _request
            match handle_type:
                case self.HandleType.GET:
                    handled = self._session.get(url, headers=header)
                case self.HandleType.POST:
                    handled = self._session.post(url, headers=header)
                case _:
                    raise AttributeError("Invalid handle type")
        except (
                OSError, ConnectionError, ConnectionResetError, _urlexc.NewConnectionError, _urlexc.ProtocolError,
                _urlexc.MaxRetryError, _socketerr
        ):
            return
        except Exception as e:
            await self.instance.throw(e, "handle")
            return

        match return_type:
            case self.ReturnType.TEXT:
                return handled.text

            case self.ReturnType.JSON:
                try:
                    return handled.json()
                except _request.JSONDecodeError as e:
                    try:
                        return _json(handled.text.split('\n')[0])
                    except Exception as ex:
                        await self.instance.throw(e, "parse")
                        await self.instance.throw(ex, "parse.retry")
                        return
                except Exception as e:
                    await self.instance.throw(e, "parse")
                    return

            case self.ReturnType.SOUP:
                return _Soup(handled.text, "xml")

            case self.ReturnType.BYTE:
                return handled.content

            case _:
                raise AttributeError("Invalid parse type")
