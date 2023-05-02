import sys

from fomalhaut.main.broadcast import *
from fomalhaut.main.earendel import *
from fomalhaut.main.mdd import *
from fomalhaut.main.settings import Settings as _Settings
from fomalhaut.module.core import Callable as _Callable

settings: _Settings = _Settings()


def call(main: _Callable) -> None:
    main(settings)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        match sys.argv[1]:
            case 'mcnews':
                call(MinecraftNews)
            case 'mdd':
                call(MDD)
            case 'mcc':
                call(MCC)
            case 'heyst':
                call(Heyst)
            case 'pablo':
                call(Pablo)
            case 'earendel':
                call(Earendel)
            case 'fomalhaut':
                call(Fomalhaut)
            case 'plazma':
                call(Plazma)
            case 'alphabot':
                call(AlphaBot)
            case _:
                print('Usage: python testscript.py [mcnews|mdd|mcc|heyst|pablo|earendel|fomalhaut|plazma|alphabot]')
    else:
        print('Usage: python testscript.py [mcnews|mdd|mcc|heyst|pablo|earendel|fomalhaut|plazma|alphabot]')
