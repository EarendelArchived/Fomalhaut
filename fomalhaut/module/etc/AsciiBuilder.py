UPPERCASE = list('𝖠𝖡𝖢𝖣𝖤𝖥𝖦𝖧𝖨𝖩𝖪𝖫𝖬𝖭𝖮𝖯𝖰𝖱𝖲𝖳𝖴𝖶𝖷𝖸𝖹')
LOWERCASE = list('𝖺𝖻𝖼𝖽𝖾𝖿𝗀𝗁𝗂𝗃𝗄𝗅𝗆𝗇𝗈𝗉𝗊𝗋𝗌𝗍𝗎𝗏𝗐𝗑𝗒𝗓')


def to_gothic(from_: str) -> str:
    value = ""
    for i in list(from_):
        try:
            j = ord(i)
            if 64 < j < 91:
                value += UPPERCASE[j - 65]
            elif 96 < j < 123:
                value += LOWERCASE[j - 97]
            else:
                value += j
        except TypeError:
            value += i
    return value
