from evennia import default_cmds
from evennia.utils.evmenu import EvMenu
from evennia.utils import evtable
from world.static_data import EYES, HAIR

HELP = "Chargen"

class ChargenCommand(default_cmds.MuxCommand):
    """
    Begins the Chargen process.
    """

    key = "initiate"
    lock = "cmd:perm(Player)"
    help_category = HELP

    def func(self):
        EvMenu(self.caller, "commands.chargen_commands",
               startnode="menu_start_node",
               cmdset_mergetype="Replace",
               node_formatter=node_formatter,
               options_formatter=options_formatter,
               cmd_on_exit=exit_message)


def menu_start_node(caller):
    text = "Initiating Clone Replication and Configuration Subroutine...\n"
    text += "Subroutine initiated.\n\n"
    text += "Welcome, new Citizen!  I am the Computer.  I am your friend.  You are about to enter Alpha Complex. " \
            "Humanity's home since the year |y<REDACTED>|n.  Long ago, I helped save the human race from the " \
            "devastation caused by |y<DATA NOT FOUND>|n when the |y<CORRUPTION DETECTED>|n swarming.  Anyway, let's " \
            "get you all set up, shall we?\n\nPlease select an option below."

    options = ({"desc": "Randomize", "goto": "chargen_random"},
               {"desc": "Customize", "goto": "chargen_custom"},)

    return text, options

def chargen_random(caller):
    pass


def chargen_custom(caller):
    text = "You've selected: |yRANDOMIZE|n.\n\nInitiating randomization...\n\n|rError:|n Randomization algorithm " \
           "fault detected.  Defaulting to customization mode.\n\nPlease select an option to customize."

    options = ()

    if caller.db.eyes:
        options += ({"desc": "Eyes", "goto": "select_eyes"},)
    else:
        options += ({"desc": "|xEyes|n", "goto": "select_eyes"},)

    return text, options


def select_eyes(caller):
    text = "Please select from one of the following choices for eye color.\n\n"


    options = ()

    for e in EYES:
        options += ({"desc": EYES[e], "exec": "set_eyes", "goto": "chargen_custom"},)

    return text, options

def set_eyes(caller, caller_input):
    # eyes_input = caller_input.strip()
    print("Test")

    # if eyes in EYES:
    #     caller.db.eyes = eyes
    # else:
    #     caller.msg("Invalid input.  Try again.")


def node_formatter(nodetext, optionstext, caller=None):
    separator1 = "|002_|n" * 78 + "\n\n"
    separator2 = "\n" + "|002_|n" * 78 + "\n\nYou may type '|gq|n' or '|gquit|n' " \
                                         "at any time to quit this application.\n" + "|002_|n" * 78 + "\n\n"
    return separator1 + nodetext + separator2 + optionstext

def options_formatter(optionlist, caller=None):
    options = []
    for key, option in optionlist:
        options.append("|w%s|n: %s" % (key, option))

    if len(options) > 6:
        if len(options) % 2 > 0:
            colA = options[:len(options) / 2 + 1]
            colB = options[len(options) / 2 + 1:]
        else:
            colA = options[:len(options) / 2]
            colB = options[len(options) / 2:]
        table = evtable.EvTable(table=[colA, colB], border=None)

        table.reformat_column(0, width=40)
        table.reformat_column(1, width=40)

        return str(table) + "\n"

    else:
        return "\n".join(options)


def exit_message(caller, menu):
    caller.msg("Exiting Clone Setup.  Goodbye.")
