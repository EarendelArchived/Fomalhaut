from ......core import Final as _Final
from ......core import Self as _Self


class ColourElement:
    """
    Embed에 사용할 색상을 정의합니다.

    Parameters
    -----------
    value: int
        HEX 코드로 표현된 색상 값

    Attributes
    -----------
    value: int
        HEX 코드로 표현된 색상 값
    """

    def __init__(self, value: int):
        self.value: _Final[int] = value

    @classmethod
    def teal(cls) -> _Self:
        return cls(0x1ABC9C)

    @classmethod
    def dark_teal(cls) -> _Self:
        return cls(0x11806A)

    @classmethod
    def brand_green(cls) -> _Self:
        return cls(0x57F287)

    @classmethod
    def green(cls) -> _Self:
        return cls(0x2ECC71)

    @classmethod
    def dark_green(cls) -> _Self:
        return cls(0x1F8B4C)

    @classmethod
    def blue(cls) -> _Self:
        return cls(0x3498DB)

    @classmethod
    def dark_blue(cls) -> _Self:
        return cls(0x206694)

    @classmethod
    def purple(cls) -> _Self:
        return cls(0x9B59B6)

    @classmethod
    def dark_purple(cls) -> _Self:
        return cls(0x71368A)

    @classmethod
    def magenta(cls) -> _Self:
        return cls(0xE91E63)

    @classmethod
    def dark_magenta(cls) -> _Self:
        return cls(0xAD1457)

    @classmethod
    def gold(cls) -> _Self:
        return cls(0xF1C40F)

    @classmethod
    def dark_gold(cls) -> _Self:
        return cls(0xC27C0E)

    @classmethod
    def orange(cls) -> _Self:
        return cls(0xE67E22)

    @classmethod
    def dark_orange(cls) -> _Self:
        return cls(0xA84300)

    @classmethod
    def brand_red(cls) -> _Self:
        return cls(0xED4245)

    @classmethod
    def red(cls) -> _Self:
        return cls(0xE74C3C)

    @classmethod
    def dark_red(cls) -> _Self:
        return cls(0x992D22)

    @classmethod
    def lighter_grey(cls) -> _Self:
        return cls(0x95A5A6)

    lighter_gray = lighter_grey

    @classmethod
    def dark_grey(cls) -> _Self:
        return cls(0x607D8B)

    dark_gray = dark_grey

    @classmethod
    def light_grey(cls) -> _Self:
        return cls(0x979C9F)

    light_gray = light_grey

    @classmethod
    def darker_grey(cls) -> _Self:
        return cls(0x546E7A)

    darker_gray = darker_grey

    @classmethod
    def og_blurple(cls) -> _Self:
        return cls(0x7289DA)

    @classmethod
    def blurple(cls) -> _Self:
        return cls(0x5865F2)

    @classmethod
    def greyple(cls) -> _Self:
        return cls(0x99AAB5)

    @classmethod
    def dark_theme(cls) -> _Self:
        return cls(0x313338)

    @classmethod
    def fuchsia(cls) -> _Self:
        return cls(0xEB459E)

    @classmethod
    def yellow(cls) -> _Self:
        return cls(0xFEE75C)

    @classmethod
    def dark_embed(cls) -> _Self:
        return cls(0x2B2D31)

    @classmethod
    def light_embed(cls) -> _Self:
        return cls(0xEEEFF1)
