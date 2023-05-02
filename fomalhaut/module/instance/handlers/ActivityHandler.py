from discord.enums import ActivityType as _Type
from discord.enums import Status as _Status


class ActivityHandler:
    """
    인스턴스의 활동을 핸들링합니다.

    Parameters
    -----------
    status: str
        인스턴스의 온라인 상태
    type: str
        인스턴스의 활동 유형
    content: str
        인스턴스의 활동 내용

    Attributes
    -----------
    status: Status
        인스턴스의 온라인 상태
    type: ActivityType
        인스턴스의 활동 유형
    content: str
        인스턴스의 활동 내용
    """

    def __init__(
            self, status: str, type: str, content: str
    ):
        self.status: _Status = _Status(status)
        self.content: str = content

        match type:
            case "playing":
                self.type: _Type = _Type.playing
            case "streaming":
                self.type: _Type = _Type.streaming
            case "listening":
                self.type: _Type = _Type.listening
            case "watching":
                self.type: _Type = _Type.watching
            case "competing":
                self.type: _Type = _Type.competing
            case _:
                raise ValueError("Invalid Activity Type")
