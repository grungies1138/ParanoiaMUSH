import re
import random
from evennia import default_cmds, utils
from evennia.utils.evmenu import EvMenu
from evennia.utils import evtable
from world.static_data import EYES, HAIR, SKIN, PERSONALITY, MUTANT_POWERS, SECRET_SOCIETIES

HELP = "Chargen"

class ChargenCommand(default_cmds.MuxCommand):
    """
    Begins the Chargen process.
    """

    key = "initiate"
    lock = "cmd:perm(Player)"
    help_category = HELP

    def func(self):
        self.caller.msg("Cerebral Coretech unit installed.")
        utils.delay(1, self.initial_message, caller=self.caller)

    def initial_message(self, caller):
        self.caller.msg("Booting initial configuration setup menu...")
        utils.delay(1, self.call_menu, caller=caller)

    def call_menu(self, caller):
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
               {"desc": "Customize", "goto": "chargen_custom_landing"})

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
    text = "Welcome to the Customization and Configuration Portal.  Here you will create your clone's individual " \
           "configuration.  Everything from the skills they have to the hair on their head, if any.  Please choose " \
           "from the options below to begin your journey."

    options = ({"desc": "Personal", "goto": "chargen_personal"},
               {"desc": "Skills", "goto": "chargen_skills"},
               {"desc": "Finalize", "goto": "finalize_chargen"})

    return text, options

def chargen_skills(caller):
    text = "Skills are how well your clone can do... stuff.  While I would love it if all of the citizens of Alpha " \
           "Complex were trained experts in all fields of study, attempts to do so have resulted in undesirable " \
           "mutations.  And since mutants are traitors and traitors are caught, sterilized and destroyed, well, we " \
           "won't talk about that.  Anyway, in order to mitigate the risk of mutation, for every skill you choose to " \
           "increase, another skill, chosen at random, will be decreased by the same level.  Now, let's get you " \
           "learned!\n\n"

    next_skill_level = 0

    skills = caller.db.skills.values()

    if 5 not in skills:
        next_skill_level = 5
    elif 4 not in skills:
        next_skill_level = 4
    elif 3 not in skills:
        next_skill_level = 3
    elif 2 not in skills:
        next_skill_level = 2
    elif 1 not in skills:
        next_skill_level = 1

    if next_skill_level > 0:
        text += "Your next skill can be set to |w+{}|n.  Please choose the skill to set to this value.  If you " \
                "don't see a skill listed below, that means it's been selected for the negative modifier.  Type " \
                "|w+sheet|n at any time to review your skill layout.".format(next_skill_level)
        setattr(caller.ndb._menutree, 'next_skill_level', next_skill_level)
    else:
        text += "All your skills have been set.  If you don't like your choices, you may reset them.  " \
                "But this will reset all of your choices."

    options = ()

    for skill, value in caller.db.skills.iteritems():
        if value == 0:
            options += ({"key": skill, "desc": skill, "exec": set_skill, "goto": "chargen_skills"},)

    options += ({"key": "reset", "desc": "Reset all skills", "exec": reset_skills, "goto": "chargen_skills"},
                {"key": "back", "desc": "Go Back", "goto": "chargen_custom"})

    return text, options

def reset_skills(caller):
    for skill in caller.db.skills:
        caller.db.skills[skill] = 0

def set_skill(caller, caller_input):
    selected_skill = caller_input.strip().lower()
    next_skill_level = caller.ndb._menutree.next_skill_level

    caller.db.skills[selected_skill] = next_skill_level

    skills = {key for (key, value) in caller.db.skills.iteritems() if value == 0}

    caller.db.skills[random.choice(list(skills))] = next_skill_level * -1

def chargen_personal(caller):
    # text = "These are the personal customization options and your current configuration.  To choose a custom setting, " \
    #        "or to change a setting once it is set, simply select the option below to be taken to the customization " \
    #        "screen."
    text = "These are the personal customization options and your current configuration.  To choose a custom setting, " \
           "or to change a setting once it is set, simply select the option below to be taken to the customization " \
           "screen.\n\n"

    text += "|wEyes:|n {}".format(EYES.get(caller.db.eyes))

    text += "\n|wHair:|n {}".format(HAIR.get(caller.db.hair))

    text += "\n|wHeight:|n {}".format(caller.db.height)

    text += "\n|wWeight:|n {}".format(caller.db.weight)

    text += "\n|wSkin:|n {}".format(SKIN.get(caller.db.skin))

    text += "\n|wPersonality:|n {}".format(", ".join(caller.db.personality))

    text+= "\n|wGender:|n {}".format(caller.db.gender)

    text += "\n|wHome Sector:|n {}".format(caller.db.sector)

    text += "\n\nPlease select an option to customize."

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

    if not caller.db.sector:
        options += ({"desc": "Home Sector", "goto": "select_sector"},)
    else:
        options += ({"desc": "|xHome Sector|n", "goto": "select_sector"},)

    if caller.db.eyes > 0 and caller.db.hair > 0 and caller.db.height and caller.db.weight and caller.db.skin \
            and caller.db.personality and caller.db.gender:
        options += ({"desc": "Back", "goto": "chargen_custom"},)

    return text, options

def select_sector(caller):
    text = "Alpha Complex is a large a diverse structure.  There are many sections of the superstructure and, " \
           "seemingly, no end.  Sectors are home!  Usually, because you are here means that there is a population " \
           "need in one or several of the sectors.  This means you cna choose!  Simply type the designation for the " \
           "sector you wish to be from.\n\nWhat?  You don't know what sector to choose?  To be honest, it doesn't " \
           "really matter all that much.  Many citizens simply enter a sector at random.  To do that, just enter " \
           "three characters, a dash and two numbers.  Like this: |wOMG-13|n or |wWTF-69|n"

    options = ({"key": "_default", "exec": set_sector, "goto": "chargen_personal"})

    return text, options

def set_sector(caller, caller_input):
    sec = caller_input.strip().upper()
    regex = re.compile(r'^(?P<sector>[A-Z]{3}-\d{1,2})$')
    match = regex.match(sec)

    if match:
        caller.db.sector = match.group("sector")
    else:
        caller.msg("|rERROR:|n Invalid input.  Try again.")

def select_gender(caller):
    text = "Hello citizen.  I, your friend the Computer, can help you select a gender.  Gender has been deemed too " \
           "provocative to be uncensored.  Humans tend to have difficulties when it comes to gender roles and " \
           "stereotypes.  Therefore, I have censored all references to gender both in files and within your visual " \
           "field.  However, clones often feel the need to express a gender of their choosing.  In order to make you " \
           "more happy, remember that |rHappiness is Mandatory|n, please enter the gender of your choosing.  Since I " \
           "maintain full control over procreation, this is essentially pointless and merely bit of \'window " \
           "dressing\'.  Enjoy!"

    options = ({"key": "_default", "exec": set_gender, "goto": "chargen_personal"},)
    options += ({"key": "back", "desc": "Back", "goto": "chargen_personal"},)

    return text, options

def set_gender(caller, caller_input):
    caller.db.gender = caller_input.strip().lower()

def select_personality(caller):
    text = ""
    if len(caller.db.personality) == 3:
        text += "You have already selected three personality traits.  No one likes someone with too much " \
                "personality.  You may choose to remove one and replace it with another, but otherwise you are " \
                "done here."
    else:
        text += "Through advanced neural sequencing, I, your friend, the Computer, can even help you determine the type " \
           "of personality you wish to have! After all, a positive outlook help improve happiness for you and your " \
                "fellow citizens.  And |rHappiness is mandatory|n.\n\nPlease select one of the following traits.\n\n"

        text += ", ".join(PERSONALITY.iterkeys())

    options = ()

    options += ({"key": "_default", "exec": set_personality, "goto": "select_personality"},)

    if len(caller.db.personality) > 0:
        options += ({"desc": "Remove", "goto": "remove_personality"},)

    options += ({"key": "back", "desc": "Back", "goto": "chargen_personal"},)

    return text, options

def remove_personality(caller):
    text = "Please select the personality trait you wish to remove from your clone."

    options = ()

    for per in caller.db.personality:
        options += ({"key": per, "exec": del_personality, "goto": "select_personality"},)

    return text, options

def del_personality(caller, caller_input):
    per = caller_input.strip().lower()

    if per not in PERSONALITY:
        caller.msg("|rERROR:|n Invalid input.  Try again.")
    else:
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
        options += ({"desc": SKIN[s], "exec": set_skin, "goto": "chargen_personal"},)

    options += ({"key": "back", "desc": "Back", "goto": "chargen_personal"},)

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

    options = ({"key": "_default", "exec": set_weight, "goto": "chargen_personal"},)
    options += ({"key": "back", "desc": "Back", "goto": "chargen_personal"},)

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

    options = ({"key": "_default", "exec": set_height, "goto": "chargen_personal"},)
    options += ({"key": "back", "desc": "Back", "goto": "chargen_personal"},)

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
        options += ({"desc": HAIR[h], "exec": set_hair, "goto": "chargen_personal"},)
    options += ({"key": "back", "desc": "Back", "goto": "chargen_personal"},)

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
        options += ({"desc": EYES[e], "exec": set_eyes, "goto": "chargen_personal"},)

    options += ({"key": "back", "desc": "Back", "goto": "chargen_personal"},)

    return text, options

def set_eyes(caller, caller_input):
    eyes_input = int(caller_input.strip())

    if eyes_input in EYES:
        caller.db.eyes = eyes_input
    else:
        caller.msg("|rERROR:|n Invalid input.  Try again.")


def finalize_chargen(caller):
    text = "So you want to finish your clone?  Well, not is a good time to review things.  make sure to type " \
           "|w+sheet|n and look it over.  Make sure you are satisfied with everything.  If not, type |wback|n and " \
           "just fix it for God's sake!\n\nOtherwise type |wconfirm|n to confirm you are satisfied and finish up " \
           "your clone configuration."

    options = ({"key": "confirm", "desc": "Confirm Configuration", "exec": finalize_finish, "goto": "exit"},
               {"key": "back", "desc": "Go Back", "goto": "chargen_custom"})

    return text, options


def finalize_finish(caller, caller_input):
    """
    TODO: Set the following items:
    Choose Mutant Powers
    """
    violence = calculate_violence(caller)
    brains = calculate_brains(caller)
    chutzpah = calculate_chutzpah(caller)
    mechanics = calculate_mechanics(caller)

    if violence > 0:
        caller.db.stats["violence"] = violence
    else:
        caller.db.stats["violence"] = 0

    if brains > 0:
        caller.db.stats["brains"] = brains
    else:
        caller.db.stats["brains"] = 0

    if chutzpah > 0:
        caller.db.stats["chutzpah"] = chutzpah
    else:
        caller.db.stats["chutzpah"] = 0

    if mechanics > 0:
        caller.db.stats["mechanics"] = mechanics
    else:
        caller.db.stats["mechanics"] = 0

    new_stats = {key: value for key, value in zip(caller.db.stats.keys(), random.sample(caller.db.stats.values(), len(caller.db.stats.values())))}
    caller.db.stats = new_stats

    caller.db.moxie = 6
    caller.db.mutant_power = random.choice(MUTANT_POWERS.keys())
    caller.db.secret_societies.append[random.choice(SECRET_SOCIETIES.keys())]


def exit(caller):
    text = ""

    options = ()
    return text, options


########################################################################################################################
# UTILITY
########################################################################################################################

def calculate_violence(caller):
    violence = [caller.db.skills.get("athletics"), caller.db.skills.get("guns"), caller.db.skills.get("melee"),
                     caller.db.skills.get("throw")]
    return max(violence)

def calculate_brains(caller):
    brains = [caller.db.skills.get("science"), caller.db.skills.get("psychology"), caller.db.skills.get("bureaucracy"),
              caller.db.skills.get("alpha complex")]
    return max(brains)

def calculate_chutzpah(caller):
    chutzpah = [caller.db.skills.get("bluff"), caller.db.skills.get("charm"), caller.db.skills.get("intimidate"),
                caller.db.skills.get("stealth")]
    return max(chutzpah)

def calculate_mechanics(caller):
    mechanics = [caller.db.skills.get("operate"), caller.db.skills.get("engineer"), caller.db.skills.get("program"),
                 caller.db.skills.get("demolitions")]
    return max(mechanics)


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
