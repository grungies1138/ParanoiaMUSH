import re
from evennia import default_cmds
from evennia.utils.evmenu import EvMenu
from evennia.utils import evtable
from world.static_data import EYES, HAIR, SKIN, PERSONALITY

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
    text = ""
    if len(caller.db.personality) == 3:
        text += "You have already selected three personality traits.  No one likes someone with too much " \
                "personality.  You may choose to remove one and replace it with another, but otherwise you are " \
                "done here."
    else:
        text += "Through advanced neural sequencing, I, your friend, the Computer, can even help you determine the type " \
           "of personality you wish to have!  Please select one of following positive traits.  After all, a positive" \
           " outlook help improve happiness for you and your fellow citizens.  And |rHappiness is mandatory|n.\n\n"

    text += ", ".join(PERSONALITY.iterkeys())

    options = ()

    options += ({"key": "_default", "exec": set_personality, "goto": "chargen_custom"},)

    if len(caller.db.personality) > 0:
        options += ({"desc": "Remove", "goto": "remove_personality"},)

    options += ({"key": "back", "desc": "Back", "goto": "chargen_custom"},)

    return text, options


def remove_personality(caller):
    text = "Please select the personality trait you wish to remove from your clone."

    options = ()

    for per in caller.db.personality:
        options += ({"desc": per, "exec": del_personality, "goto": "select_personality"},)

    return text, options


def del_personality(caller, caller_input):
    per = caller_input.strip().lower()
    if per in caller.db.personality:
        caller.db.personality.remove(per)


def set_personality(caller, caller_input):
    per = caller_input.strip().lower()
    if per not in PERSONALITY:
        caller.msg("|rERROR:|n Invalid input.  Try again.")
    elif per in caller.db.personality:
        caller.msg("|rERROR:|n You have already selected that trait.  Please choose another.")
    else:
        caller.db.personality.append(per)


def select_skin(caller):
    text = "Humans are a tapestry of colors and shades of many varieties.  To offer you the optimal skin color " \
           "experience I have reduced the number of shades to 7!  Please select one below.\n\n"

    options = ()

    for s in SKIN:
        options += ({{"desc": SKIN[s], "exec": set_skin, "goto": "chargen_custom"}},)

    return text, options


def set_skin(caller, caller_input):
    skin = int(caller_input.strip())
    if skin in SKIN:
        caller.db.skin = skin
    else:
        caller.msg("|rERROR:|n Invalid input.  Try again.")


def select_weight(caller):
    text = "Please enter the weight you wish to be.  You may select a number of pounds or kilograms. " \
           "\n\n|wExample:|n if you wish to be 112 pounds, enter: |y112lbs|n or for being 67 kilograms, enter:" \
           " |y67kgs|n\n\n|rNOTE:|n Selecting a weight to small or too large can result in undesirable mutations.  " \
           "Therefore, the following limitations are in effect:\n\n|wMetric:|n 45kgs - 100kgs\n|wImperial:|n 100lbs - " \
           "220lbs"

    options = ({"key": "_default", "exec": set_weight, "goto": "chargen_custom"},)

    return text, options


def set_weight(caller, caller_input):
    weight = caller_input.strip().lower()
    regex = re.compile(r'^(?P<number>\d{2,3})(?P<string>kgs|lbs)$')
    match = regex.match(weight)
    if match:
        number, measure = int(match.group('number')), match.group('string')

    if measure and measure == "kgs":
        if number < 45 or number > 100:
            caller.msg("|rERROR:|n That weight is not within the specified parameter limits.  Please try again.")
        else:
            caller.db.weight = weight

    if measure and measure == "lbs":
        if number < 100 or number > 220:
            caller.msg("|rERROR:|n That weight is not within the specified parameter limits.  Please try again.")
        else:
            caller.db.weight = weight


def select_height(caller):
    text = "Please enter the height you wish to be.  You may select a number of inches or centimeters." \
           "\n\n\t|wExample:|n if you wish to be 1.5 meters tall, enter: |y150cm|n or for being 5'8\" enter: |y68in|n" \
           "\n\n|rNOTE:|n Selecting a height too small or too large can result in undesirable mutation.  Therefore " \
           "the following limitations are in effect.\n\n|wMetric:|n 135cm - 210cm\n|wImperial:|n 53in - 82in\n\n"

    options = ({"key": "_default", "exec": set_height, "goto": "chargen_custom"},)

    return text, options


def set_height(caller, caller_input):
    height = caller_input.strip().lower()
    regex = re.compile(r'^(?P<number>\d{2,3})(?P<string>cm|in)$')
    match = regex.match(height)
    if match:
        number, measure = int(match.group('number')), match.group('string')


    if measure == "cm":
        if number < 135 or number > 210:
            caller.msg("|rERROR:|n That height is not within the specified parameter limits.  Please try again.")
        else:
            caller.db.height = height

    if measure == "in":
        if number < 53 or number > 82:
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
