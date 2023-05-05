from .YouTubeHandler import YouTubeHandler as _Handler
from ...core import Callable as _Type
from ...core import Functional as _Func
from ...instance import Instance as _Instance
from ...instance.handlers.interface.BasicInterface import BasicThrowableInterface as _Interface


def handleable() -> _Type:
    return tuple[str, _Handler]


class YouTubeMultiHandler(_Interface):
    def __init__(self, instance: _Instance):
        super().__init__(instance, "YouTubeMultiListener")
        self.target: list[tuple[str, _Handler]] = []

    def append(self, func: _Func) -> None:
        name, target = func()
        self.target.append((name, _Handler(self.instance, target)))

    async def handle(self, name: str, force: bool = False) -> bool:
        for i in self.target:
            if i[0] == name:
                return (await i[1].handle(force)).cache.success
        return False
