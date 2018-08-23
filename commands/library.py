import re

HEAD_CHAR = "|015-|n"
SUB_HEAD_CHAR = "-"
MAX_WIDTH = 78

def header(header_text=None, width=MAX_WIDTH, fill_char=HEAD_CHAR):
    header_string = ""
    if header_text and len(header_text) < width:
        header_repeat = (width - len(header_text)) / 2
        header_string = fill_char * header_repeat + " " + header_text + " " + fill_char * header_repeat
        if header_string < width:
            header_string += fill_char * width - len(header_string)

    else:
        header_string = fill_char * width
    return header_string

def titlecase(s):
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?",
                  lambda mo: mo.group(0)[0].upper() +
                             mo.group(0)[1:].lower(), s)

def pad_right(main, right, width):
    return "{}$pad({}, {}, r)".format(main, right, width - len(str(main)))
