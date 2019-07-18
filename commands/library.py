import re
from evennia.utils import evtable


HEAD_CHAR = "|015-|n"
SUB_HEAD_CHAR = "-"
MAX_WIDTH = 78


def header(header_text=None, width=MAX_WIDTH, fill_char=HEAD_CHAR):
    header_string = ""
    if header_text and len(header_text) < width:
        header_repeat = (width - (len(header_text) + 2)) / 2
        header_string = fill_char * header_repeat + " " + header_text + " " + fill_char * header_repeat
        if len(header_string) < width:
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


def clearance_color(clearance):
    if clearance == "Infrared":
        return "x"
    if clearance == "Red":
        return "r"
    if clearance == "Orange":
        return "520"
    if clearance == "Yellow":
        return "y"
    if clearance == "Green":
        return "g"
    if clearance == "Blue":
        return "b"
    if clearance == "Indigo":
        return "M"
    if clearance == "Violet":
        return "m"
    if clearance == "Ultraviolet":
        return "[W|X"


def _wrapper(caller, attr, value):
    return lambda caller: setattr(caller.ndb._menutree, attr, value)


def IsInt(n):
    try:
        int(n)
        return True
    except ValueError:
        return False


def node_formatter(nodetext, optionstext, caller=None):
    separator1 = "|002_|n" * 78 + "\n\n"
    separator2 = "\n" + "|002_|n" * 78 + "\n\nYou may type '|gq|n' or '|gquit|n' " \
                                         "at any time to quit this application.\n" + "|002_|n" * 78 + "\n\n"
    return "\n\n\n" + separator1 + nodetext + separator2 + optionstext


def options_formatter(optionlist, caller=None):
    options = []
    for key, option in optionlist:
        options.append("|w%s|n: %s" % (key, option))

    if len(options) > 6:
        if len(options) % 2 > 0:
            colA = options[:len(options) // 2]
            colB = options[len(options) // 2:]
        else:
            colA = options[:len(options) // 2]
            colB = options[len(options) // 2:]
        table = evtable.EvTable(table=[colA, colB], border=None)

        table.reformat_column(0, width=39)
        table.reformat_column(1, width=39)

        return str(table) + "\n"

    else:
        return "\n".join(options)


def text_error(text):
    replacements = {'a': '4', 'o': '0'}
