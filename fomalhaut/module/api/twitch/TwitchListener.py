from ..common.BasicWebHandler import BasicWebHandler as _Handler
from ...core import Final as _Final
from ...instance import Instance as _Instance
from ...instance.handlers.interface.BasicInterface import BasicThrowableInterface as _Interface
from ...instance.handlers.message.embed import FieldElement as _Field
from ....main.settings.component.TwitchComponent import BaseTwitchComponent as _Settings


class TwitchListener(_Interface):
    """
    트위치 API에서 정보를 불러오는 클래스입니다.

    Parameters
    -----------
    instance: Instance
        인스턴스

    Attributes
    -----------
    settings: TwitchComponent
        트위치 API 설정
    handler: BasicWebHandler
        웹 요청을 처리하는 핸들러
    """

    def __init__(self, instance: _Instance):
        super().__init__(instance, "TwitchListener")
        self.settings: _Final[_Settings] = instance.main.api.twitch
        self.handler: _Final[_Handler] = _Handler(instance)

    async def handle(self) -> dict:
        """
        트위치 API에서 정보를 불러옵니다.
        """
        try:
            oauth: str = await self._oauth()
            if oauth != "":
                handled: dict = await self.handler.handle(
                    f"https://api.twitch.tv/helix/streams?user_login={self.instance.settings['twitch'].target}",
                    header={
                        "Client-Id": self.settings.cli_id,
                        "Authorization": f"Bearer {oauth}"
                    }
                )
                if type(handled) == dict:
                    return handled
                else:
                    raise TypeError(f"Respond is not dict, but {type(handled)}")
        except Exception as e:
            await self.throw(e, "handle")
            return {}

    async def _oauth(self) -> str:
        """
        트위치 API에서 OAuth 토큰을 불러옵니다.
        """
        try:
            try:
                handled: dict = await self.handler.handle(
                    f"https://id.twitch.tv/oauth2/token?grant_type=client_credentials&client_id={self.settings.cli_id}"
                    f"&client_secret={self.settings.secret}", _Handler.HandleType.POST
                )
                if type(handled) != dict:
                    raise TypeError(f"Respond is not dict, but {type(handled)}")
            except Exception as e:
                await self.throw(e, "HandleOAuth.getResponse")
                return ""

            try:
                return handled["access_token"]
            except KeyError as e:
                async def throw() -> str:
                    await self.throw(
                        e, f"handleOAuth.handle", additional=_Field("Respond", f"```\n{str(handled)}\n```")
                    )
                    return ""

                try:
                    if handled["status"] == 500:
                        return await self._oauth()
                    return await throw()
                except KeyError:
                    return await throw()
                except Exception as ex:
                    await self.throw(ex, "handleOAuth.handle.parseStatus")
                    return await throw()
            except Exception as e:
                await self.throw(e, "handleOAuth.handle")
                return ""

        except Exception as e:
            await self.throw(e, "handleOAuth")
            return ""
