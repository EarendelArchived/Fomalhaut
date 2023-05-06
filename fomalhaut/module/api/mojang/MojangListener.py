from .MojangCache import MojangCache as _Cache
from ..common.BasicWebHandler import BasicWebHandler as _Handler
from ...core import Final as _Final
from ...instance import Instance as _Instance
from ...instance.handlers.interface.BasicInterface import BasicThrowableInterface as _Interface


class MojangListener(_Interface):
    def __init__(self, instance: _Instance):
        super().__init__(instance, "MojangListener")
        self.cache: _Final[_Cache] = _Cache(instance)
        self.handler: _Final[_Handler] = _Handler(instance)

    async def handle(self, force: bool = False):
        try:
            try:
                response: dict = await self.handler.handle(
                    "https://launchermeta.mojang.com/mc/game/version_manifest.json"
                )
            except Exception as e:
                await self.throw(e, "handle.getResponse")
                return

            try:
                release: str = response["latest"]["release"]
                snapshot: str = response["latest"]["snapshot"]

            except Exception as e:
                await self.throw(e, "handle.getResponse")
                return

            try:
                cache: _Cache = self.cache
                if (
                    (type(release) == str and release != cache.release) or force
                ):

