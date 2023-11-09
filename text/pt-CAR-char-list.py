#!/usr/bin/env python3

V = ['a', 'e', 'ə', 'ɛ', 'i', 'o', 'ɔ', 'u']
U = [
    '',
    '\u0300', # combining grave accent
    '\u0301', # combining acute accent
    '\u0302', # combining circumflex
    # b'\\u0303', # combining tilde above
    '\u0304', # combining macron
    '\u0308', # combining diaeresis
    # b'\\u030c', # combining caron
    # b'\\u030d', # combining vert. line above
    # b'\\u1dc4', # combining macron-acute
    # b'\\u1dc5', # combining grave-macron
    # b'\\u1dc6', # combining macron-grave
    # b'\\u1dc7', # combining acute-macron
]
L = [
    '',
    '\u0327', # combining cedilla
]

chars = []
for v in V:
    for u in U:
        for l in L:
            item = f"{v}{u}{l}/{v.upper()}{u}{l}"
            chars.append(item)

print(len(chars))
print(' '.join(chars))
