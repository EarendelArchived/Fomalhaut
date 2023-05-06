from json import JSONDecodeError as _JSONErr

from ..common.BasicAPICache import BasicAPICache as _Interface
from ...basicio.BasicIOHandler import BasicIOHandler as _Handler
from ...core import Nullable as _Nullable
from ...instance import Instance as _Instance


class MojangCache(_Interface):
    def __init__(self, instance: _Instance, success: bool = True):
        super().__init__(instance, "MojangCache", _Handler.from_cache("mojang", "data.json"), success)
        self.release: _Nullable[str] = None
        self.snapshot: _Nullable[str] = None

        try:
            cache: _Nullable[dict] = self.handler.read()
            if cache is not None:
                self.release = cache["release"]
                self.snapshot = cache["snapshot"]
        except (KeyError, _JSONErr):
            self.handler.write({"release": None, "snapshot": None})

    async def update(self, latest: str, snapshot: str):
        self.release = latest
        self.snapshot = snapshot
        self.success = True
        return await self.save()

    async def save(self):
        try:
            self.handler.write({"release": self.release, "snapshot": self.snapshot})
        except Exception as e:
            self.success = False
            await self.instance.throw(e, "save")
        return self
