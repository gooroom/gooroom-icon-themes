#!/usr/bin/env python3
"""Gooroom-Candy 판의 구름 고유 아이콘을 Candy 문법(48x48, 굵기 4 둥근 선, 선형 그라데이션)으로 만든다.

usage: gen_gooroom_candy.py OUT_DIR
OUT_DIR/apps/scalable/*.svg · OUT_DIR/categories/scalable/*.svg 를 쓴다.
"""
import os
import sys

PALETTE = {
    "pp": [(88, 0, 226), (255, 0, 230)],
    "bt": [(84, 51, 255), (32, 189, 255), (165, 254, 203)],
    "og": [(255, 65, 108), (255, 175, 64)],
    "tg": [(0, 201, 167), (146, 254, 157)],
    "pb": [(196, 0, 255), (0, 146, 255)],
    "yo": [(255, 204, 0), (255, 72, 0)],
    "cm": [(0, 176, 255), (204, 0, 255)],
    "rp": [(255, 0, 128), (121, 40, 202)],
}
STROKE = 'fill="none" stroke="url(#g)" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"'

GEAR_ARROWS = ('<circle cx="19" cy="27" r="5"/><circle cx="19" cy="27" r="10"/>'
               '<path d="M19 13 V17 M19 37 V41 M5 27 H9 M29 27 H33 M9.1 17.1 L11.9 19.9 M26.1 34.1 L28.9 36.9 '
               'M9.1 36.9 L11.9 34.1 M26.1 19.9 L28.9 17.1"/>'
               '<path d="M34 5 V21 M30 9 L34 5 L38 9 M40 27 V43 M36 39 L40 43 L44 39"/>')
PERSON_ARROWS = ('<circle cx="17" cy="16" r="7"/><path d="M4 42 C4 33 10 28 17 28 C24 28 30 33 30 42"/>'
                 '<path d="M34 5 V21 M30 9 L34 5 L38 9 M40 27 V43 M36 39 L40 43 L44 39"/>')
QUESTION = '<path d="M18.5 18.5 A5.5 5.5 0 1 1 26 23.6 C24.6 24.3 24 25.4 24 27 V29"/><path d="M24 35 h0"/>'

ICONS = {
    "apps": {
        "gooroom-browser": ("bt", '<circle cx="24" cy="24" r="13"/>'
                                  '<path d="M8.5 31.5 C3 36.5 5 40 13 38.5 C21 37 34 30 40.5 23.5 C46 18 44 12.5 37 13.5"/>'),
        "gooroom-guide": ("og", '<path d="M24 12 C19 8.5 11 8 5 9.5 V38 C11 36.5 19 37 24 40.5 C29 37 37 36.5 43 38 V9.5 '
                                'C37 8 29 8.5 24 12 Z"/><path d="M24 12 V40.5"/>'),
        "gooroom-usbctl": ("tg", '<rect x="15" y="4" width="18" height="14" rx="2"/><path d="M20 10 h0 M28 10 h0"/>'
                                 '<rect x="10" y="18" width="28" height="26" rx="5"/><path d="M24 26 V36 M19.5 31 L24 26 L28.5 31"/>'),
        "gooroomupdater": ("pp", '<path d="M40 22 A16 16 0 0 0 11.5 13"/><path d="M8 26 A16 16 0 0 0 36.5 35"/>'
                                 '<path d="M11 5.5 V13.5 H19"/><path d="M37 42.5 V34.5 H29"/>'),
        "kr.gooroom.Software": ("cm", '<path d="M9 15 H39 L37 43 H11 Z"/><path d="M17 20 V12 A7 7 0 0 1 31 12 V20"/>'),
        "kr.gooroom.System.Backup": ("yo", GEAR_ARROWS),
        "gooroom-user-auto-backup": ("yo", GEAR_ARROWS),
        "kr.gooroom.User.Backup": ("pb", PERSON_ARROWS),
        "gooroom-user-backup": ("pb", PERSON_ARROWS),
        "gooroom-client-server-register": ("bt", '<rect x="4" y="9" width="28" height="20" rx="2.5"/><path d="M2 36 H24"/>'
                                                 '<rect x="31" y="18" width="14" height="25" rx="2.5"/><path d="M38 38 h0"/>'),
        "gooroom-feedback-client": ("rp", '<path d="M10 6 H38 A5 5 0 0 1 43 11 V29 A5 5 0 0 1 38 34 H20 L10 42 V34 '
                                          'A5 5 0 0 1 5 29 V11 A5 5 0 0 1 10 6 Z"/>'
                                          '<path d="M24 12 L26.4 17 L31.8 17.6 L27.8 21.2 L28.9 26.5 L24 23.8 L19.1 26.5 '
                                          'L20.2 21.2 L16.2 17.6 L21.6 17 Z"/>'),
        "grac-editor": ("tg", '<rect x="4" y="7" width="40" height="14" rx="7"/><circle cx="37" cy="14" r="3"/>'
                              '<rect x="4" y="27" width="40" height="14" rx="7"/><circle cx="11" cy="34" r="3"/>'),
        "unknown-app": ("cm", '<path d="M11 4 H29 L39 14 V44 H11 Z"/><path d="M29 4 V14 H39"/>'
                              '<g transform="translate(1 6)">' + QUESTION + '</g>'),
    },
    "categories": {
        "system-help": ("bt", '<circle cx="24" cy="24" r="20"/>' + QUESTION),
    },
}


def svg(palette, body):
    stops = PALETTE[palette]
    n = len(stops)
    stop_xml = "".join(f'<stop offset="{i * 100 // (n - 1)}%" style="stop-color:rgb{c}"/>'
                       for i, c in enumerate(stops))
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48pt" height="48pt">'
            f'<linearGradient id="g" x1="2" y1="2" x2="46" y2="46" gradientUnits="userSpaceOnUse">{stop_xml}'
            f'</linearGradient><g {STROKE}>{body}</g></svg>\n')


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    out = sys.argv[1]
    n = 0
    for ctx, icons in ICONS.items():
        d = os.path.join(out, ctx, "scalable")
        os.makedirs(d, exist_ok=True)
        for name, (pal, body) in icons.items():
            with open(os.path.join(d, name + ".svg"), "w") as f:
                f.write(svg(pal, body))
            n += 1
    print(f"{n} icons -> {out}")


if __name__ == "__main__":
    main()
