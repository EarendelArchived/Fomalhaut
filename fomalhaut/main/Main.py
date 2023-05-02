from .broadcast import *
from .earendel import *
from .mdd import *
from .settings import Settings as _Settings
from ..module.core.Runtime import Runtime as _Runtime


class Main:
    """
    모든 봇 작업을 시작합니다.
    """

    def __init__(self) -> None:
        runtime: _Runtime = _Runtime(_Settings())
        runtime.start(MinecraftNews)
        runtime.start(MDD)
        runtime.start(MCC)
        runtime.start(Heyst)
        runtime.start(Pablo)
        runtime.start(Earendel)
        runtime.start(Fomalhaut)
        runtime.start(Plazma)
        runtime.start(AlphaBot)
