import re
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

########################################################################################################################
# RANDOMIZE
########################################################################################################################
def chargen_random(caller):
    pass


def chargen_custom_landing(caller):
    text = "You've selected: |yRANDOMIZE|n.\n\nInitiating randomization...\n\n|rError:|n Randomization algorithm " \
           "fault detected.  Defaulting to customization mode."

    options = ({"desc": "Continue", "goto": "chargen_custom"},)

    return text, options


def chargen_custom(caller):
    text = "These are the customization options and your current configuration.  To choose a custom setting, or to " \
           "change a setting once it is set, simply select the option below to be taken to the customization screen." \
           "\n\n|wGender:|n {}\n|wEyes:|n {}\n|wHair:|n {}\n|wHeight:|n {}\n|wWeight:|n {}\n|wSkin:|n {}\n|wPersonality:|n {}" \
           "\n\nPlease select an option to customize.".format(caller.db.gender, EYES.get(caller.db.eyes), HAIR.get(caller.db.hair),
                                                              caller.db.height, caller.db.weight, caller.db.skin,
                                                              ", ".join(caller.db.personality))

    options = ()

    if caller.db.eyes == 0:
        options += ({"desc": "Eyes", "goto": "select_eyes"},)
    else:
        options += ({"desc": "|xEyes|n", "goto": "select_eyes"},)


    if caller.db.hair == 0:
        options += ({"desc": "Hair", "goto": "select_hair"},)
    else:
        options += ({"desc": "|xHair|n", "goto": "select_hair"},)


    if not caller.db.height:
        options += ({"desc": "Height", "goto": "select_height"},)
    else:
        options += ({"desc": "|xHeight|n", "goto": "select_height"},)


    if not caller.db.weight:
        options += ({"desc": "Weight", "goto": "select_weight"},)
    else:
        options += ({"desc": "|xWeight|n", "goto": "select_weight"},)


    if not caller.db.skin:
        options += ({"desc": "Skin", "goto": "select_skin"},)
    else:
        options += ({"desc": "|xSkin|n", "goto": "select_skin"},)


    if not caller.db.personality:
        options += ({"desc": "Personality", "goto": "select_personality"},)
    else:
        options += ({"desc": "|xPersonality|n", "goto": "select_personality"},)


    if not caller.db.gender:
        options += ({"desc": "Gender", "goto": "select_gender"},)
    else:
        options += ({"desc": "|xGender|n", "goto": "select_gender"},)

    return text, options


def select_gender(caller):
    pass


def set_gender(caller, caller_input):
    pass


def select_personality(caller):
    pass


def set_personality(caller, caller_input):
    pass


def select_skin(caller):
    pass


def set_skin(caller, caller_input):
    pass


def select_weight(caller):
    pass


def set_weight(caller, caller_input):
    pass


def select_height(caller):
    text = "Please enter the height you wish to be.  You may select a number of inches or centimeters." \
           "\n\n\t|wExample:|n if you wish to be 1.5 meters tall, enter: |y150cm|n or for being 5'8\" enter: |y68in|n" \
           "\n\n|rNOTE:|n selecting a height too small or too large can result in undesirable mutation.  Therefore " \
           "there are limitations set.  See the limitations for each unit of measure below.\n\n|wMetric:|n 150cm - " \
           "210cm\n|wImperial:|n 53in - 70in\n\n"

    options = ({"key": "_default", "exec": set_height, "goto": "chargen_custom"},)

    return text, options


def set_height(caller, caller_input):
    height = caller_input.strip().lower()
    regex = re.compile(r'^(?P<number>\d{2,3})(?P<string>cm|in)$')
    match = regex.match(height)
    if match:
        number, measure = match.group('number'), match.group('string')

    print("Number: {}".format(number))
    print("Measure: {}".format(measure == "cm"))


    if measure == "cm":
        if number < 150 or number > 210:
            caller.msg("|rERROR:|n That height is not within the specified parameter limits.  Please try again.")
        else:
            caller.db.height = height

    if measure == "in":
        if number < 53 or number > 70:
            caller.msg("|rERROR:|n That height is not within the specified parameter limits.  Please try again.")
        else:
            caller.db.height = height


def select_hair(caller):
    text = "Please select from one of the following options for hair color and style.\n\n"

    options = ()

    for h in HAIR:
        options += ({"desc": HAIR[h], "exec": set_hair, "goto": "chargen_custom"},)

    return text, options


def set_hair(caller, caller_input):
    hair = int(caller_input.strip())
    if hair in HAIR:
        caller.db.hair = hair
    else:
        caller.msg("|rERROR:|n Invalid input.  Try again.")


def select_eyes(caller):
    text = "Please select from one of the following choices for eye color.\n\n"


    options = ()

    for e in EYES:
        options += ({"desc": EYES[e], "exec": set_eyes, "goto": "chargen_custom"},)

    return text, options

def set_eyes(caller, caller_input):
    eyes_input = int(caller_input.strip())

    if eyes_input in EYES:
        caller.db.eyes = eyes_input
    else:
        caller.msg("|rERROR:|n Invalid input.  Try again.")


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
