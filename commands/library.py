import random
import string

HEAD_CHAR = "|015%s|n".format(random.choice(string.printable))
SUB_HEAD_CHAR = "-"
MAX_WIDTH = 78

def header(header_text=None, width=MAX_WIDTH, fill_char=HEAD_CHAR):
    header_string = ""
    if header_text and len(header_text) < width:
        header_repeat = (width - len(" " + header_text + " ")) / 2
        header_string = fill_char * header_repeat + header_text + fill_char * header_repeat
        if header_string < width:
            header_string += fill_char * width - len(header_string)

    else:
        header_string = fill_char * width
    return header_string