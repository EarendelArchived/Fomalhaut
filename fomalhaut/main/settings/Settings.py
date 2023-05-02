from .component import BaseTwitchComponent as _BaseTwitch
from .component import BaseYouTubeComponent as _BaseYouTube
from .component import EnvironmentHandler as _Env
from .component import LogComponent as _Log
from .component import TokenComponent as _Token
from .component import TwitchComponent as _Twitch
from .component import YouTubeComponent as _YouTube
from ...module.core import Final as _Final


class Settings:
    """
    전역 설정

    Attributes
    -----------
    instance: Settings._InstanceSettings
        인스턴스 설정
    api: Settings._APISettings
        API 설정
    """

    def __init__(self) -> None:
        handler: _Env = _Env()

        self.instance: _Final[Settings._InstanceSettings] = Settings._InstanceSettings(handler)
        self.api: _Final[Settings._APISettings] = Settings._APISettings(handler)

    def get(self, type: str, group: str, name: str) -> dict:
        """
        설정 요소를 불러옵니다.

        Parameters
        ----------
        type: str
            설정 그룹 유형 (instance, api)
        group
            설정 그룹
        name
            설정 대상 이름
        """
        match type:
            case "instance":
                return getattr(self.instance, group)[name]
            case "api":
                return getattr(self.api, group)[name]
            case _:
                raise ValueError("Unknown settings type")

    class _InstanceSettings:
        """
        인스턴스 설정

        Parameters
        -----------
        handler: EnvironmentHandler
            시스템 환경 변수 캐시 핸들러

        Attributes
        -----------
        logger: Final[dict]
            전역 기록 설정
        mdd: Final[dict]
            MDD 설정
        broadcast: Final[dict]
            트위치 스트리머 봇 설정
        earendel: Final[dict]
            Earendel 팀 인스턴스 설정
        """

        def __init__(self, handler: _Env) -> None:
            token: _Token = _Token(handler)

            self.logger: _Final[dict] = {
                "token": token.get("logger"),
                "target": _Log(
                    send=[1095728069043552337]
                )
            }

            self.mdd: _Final[dict] = {
                "MDD": {
                    "token": token.get("MDD", True)
                },

                "MCC": {
                    "token": token.get("MCC", True),
                    "profile_art": "https://cdn.discordapp.com/attachments/1002906305947779072/1096361853506031636"
                                   "/channels4_profile.jpg",
                    "youtube": _YouTube(
                        target="-N4fGYpAmvfn2Y02WlAV9A",
                        target_id="armung",
                        message="**새로운 영상이 업로드 되었습니다!**",
                        description="구독 좋아요 :)",
                        send=[1095728069043552337]
                    )
                },

                "News": {
                    "token": token.get("News", True)
                }
            }

            self.broadcast: _Final[dict] = {
                "Heyst": {
                    "token": token.get("Heyst", True),
                    "profile_art": "https://cdn.discordapp.com/attachments/1002906305947779072/1096062447997165729"
                                   "/unnamed.jpg",
                    "twitch": _Twitch(
                        target="heyst1000",
                        message="<@&959530237299945524> **헤이스트님이 생방송을 시작했습니다!**",
                        offline="<@&959530237299945524> 헤이스트님의 방송이 {}에 종료되었습니다.",
                        send=[1095728069043552337]
                    ),
                    "youtube": _YouTube(
                        target="aiyyjmlyH70au7pzKE4jnQ",
                        target_id="heyst99",
                        message="<@&959530104634101821> **헤이스트님 유튜브에 영상이 업로드 되었습니다!**",
                        description="",
                        send=[1095728069043552337]
                    )
                },

                "Pablo": {
                    "token": token.get("Pablo", True),
                    "profile_art": "https://cdn.discordapp.com/attachments/1002906305947779072/1096062447682601020"
                                   "/ceb6f1fc70b9ff1944e1eb0112329eb0.webp",
                    "twitch": _Twitch(
                        target="pablo_kr_",
                        message="<@&1076385255486926929> **파블로님이 생방송을 시작했습니다!**",
                        offline="<@&1076385255486926929> 파블로님의 방송이 {}에 종료되었습니다.",
                        send=[1095728069043552337]
                    )
                }
            }

            self.earendel: _Final[dict] = {
                "Earendel": {
                    "token": token.get("Earendel", True),
                },

                "Fomalhaut": {
                    "token": token.get("Fomalhaut", True),
                    "kurzgesagt": {
                        "profile_art": "",
                        "config": _YouTube(
                            target="sXVk37bltHxD1rDPwtNM8Q",
                            target_id="kurzgesagt",
                            message="",
                            description="",
                            send=[1102836058414125087]
                        )
                    },
                    "kurzgesagt_kr": {
                        "profile_art": "",
                        "config": _YouTube(
                            target="8rKCy_tipwTEY3RdkNCKmw",
                            target_id="kurzgesagt_kr",
                            message="",
                            description="",
                            send=[1102836058414125087]
                        )
                    },
                    "veritasium": {
                        "profile_art": "",
                        "config": _YouTube(
                            target="OgK3J7WTOl5f5Fd51kcoSg",
                            target_id="veritasium_kor",
                            message="",
                            description="",
                            send=[1102836058414125087]
                        )
                    }
                },

                "Plazma": {
                    "token": token.get("Plazma", True),
                },

                "AlphaBot": {
                    "token": token.get("AlphaBot", True),
                }
            }

    class _APISettings:
        """
        전역 API 설정

        Parameters
        -----------
        handler: EnvironmentHandler
            시스템 환경 변수 캐시 핸들러

        Attributes
        -----------
        twitch: Final[BaseTwitchComponent]
            전역 트위치 API 설정
        """

        def __init__(self, handler: _Env) -> None:
            self.twitch: _Final[_BaseTwitch] = _BaseTwitch.default(
                handler=handler,
                icon="https://cdn.discordapp.com/attachments/1002906305947779072/1067802864791076974/twitch.png"
            )

            self.youtube: _Final[_BaseYouTube] = _BaseYouTube(
                icon="https://cdn.discordapp.com/attachments/1002906305947779072/1096361793972088923/youtube.png"
            )
