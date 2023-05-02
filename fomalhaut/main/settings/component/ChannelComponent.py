from ....module.core import Final as _Final


class LogComponent:
    """
    메세지가 전송되는 채널을 관리하는 설정 요소입니다.

    Parameters
    -----------
    send: list[int]
        메세지가 전송될 채널의 ID 목록입니다.

    Attributes
    -----------
    send: Final[list[int]]
        메세지가 전송될 채널의 ID 목록입니다.
    """

    def __init__(self, send: list[int]) -> None:
        self.send: _Final[list[int]] = send


class PartnershipComponent:
    """
    파트너쉽 명령어를 읽어오는 채널을 관리하는 설정 요소입니다.

    Parameters
    -----------
    read: list[int]
        명령어를 읽을 채널의 ID 목록입니다.

    Attributes
    -----------
    read: Final[list[int]]
        명령어를 읽을 채널의 ID 목록입니다.
    """

    def __init__(self, read: list[int]) -> None:
        self.read: _Final[list[int]] = read


class NoticeComponent:
    """
    공지사항 채널을 관리하는 설정 요소입니다.

    Parameters
    -----------
    read: list[int]
        공지 명령어를 읽을 채널의 ID 목록입니다.
    send: list[int]
        공지를 전송할 채널의 ID 목록입니다.

    Attributes
    -----------
    read: Final[list[int]]
        공지 명령어를 읽을 채널의 ID 목록입니다.
    send: Final[list[int]]
        공지를 전송할 채널의 ID 목록입니다.
    """

    def __init__(self, read: list[int], send: list[int]) -> None:
        self.read: _Final[list[int]] = read
        self.send: _Final[list[int]] = send
