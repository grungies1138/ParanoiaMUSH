from random import choice
from world.equipment_prototypes import EQUIPMENT
from commands.library import _wrapper
from evennia.utils import evtable, utils, ansi
from evennia.prototypes import spawner
from world.static_data import ACTIONS, CLEARANCE, CLEARANCE_UPGRADES


def menu_start_node(caller):
    text = "Welcome to the Cerebral Coretech Alpha Complex XP point award catalog!  Long ago, in the year 214, " \
           "I determined that clones have an inherent need for self-improvement.  To facilitate this and to help " \
           "reinforce positive behaviors, I introduced the XP Point system.  You earn XP Points by performing your " \
           "duties admirably.  This includes, but is not limited to: performing tasks, identifying traitors, " \
           "informing the Computer of unregistered mutations and stopping terrorists.  Feel free to browse the " \
           "catalog to get an idea of the kinds of rewards available to you, once you have earned enough XP Points."

    options = ({"desc": "Security Clearance", "goto": "upgrade_clearance"},
               {"desc": "Skills", "goto": "upgrade_skills"},
               {"desc": "Stats", "goto": "upgrade_stats"},
               {"desc": "Moxie", "goto": "upgrade_moxie"},
               {"desc": "Equipment", "goto": "upgrade_equipment"},
               {"desc": "Recharge Equipment", "goto": "recharge_equipment"},
               {"desc": "Purchase Clones", "goto": "purchase_clones"},
               {"desc": "Action Cards", "goto": "buy_actions"})
    return text, options


def buy_actions(caller):
    text = "Actions are used in combat to help determine what you do and in what order.  They are not required but " \
           "they are, mostly, helpful.  You can purchase one, at random, for 50xp.  Again, these are chosen at " \
           "random, you take what you get and you like it or you go to bed with no Reconstituted Clone Chow(tm).  Now " \
           "in Blue!"
    options = ({"desc": "Buy Action Card", "exec": exec_buy_action, "goto": "buy_actions"},
               {"key": ["back", "b"], "desc": "Go Back", "goto": "menu_start_node"})
    return text, options


def exec_buy_action(caller):
    if caller.db.xp >= 50:
        caller.db.action_cards.append(choice(tuple(ACTIONS.keys())))
        caller.db.xp = caller.db.xp - 50
    else:
        caller.msg("|rERROR:|n You do not have enough XP to buy an action card.")


def upgrade_clearance(caller):
    text = "The Peter Principle: People tend to be promoted to their own level of incompetence.\n\nWith enough time, " \
           "patience and luck, clones like you can rise through the ranks of security clearances.  Legend has it " \
           "that TOM-92 (who doesn't exist) was once an Infrared.  See the list of security clearances below along " \
           "with the associated XP Point costs.  And remember those costs are cumulative.\n\nExample: To go from " \
           "Infrared to Red costs 500 XP Points.  Likewise to go from Red to Orange costs 1000 XP Points.  Therefore " \
           "to go from Infrared to Orange costs a total of 1500 XP Points.\n\n|wCurrent Clearance:|n {}" \
        .format(CLEARANCE.get(caller.db.clearance))

    red = ansi.ANSIString("|rRed:|n")
    red_cost = ansi.ANSIString("500")
    orange = ansi.ANSIString("|520Orange:|n")
    orange_cost = ansi.ANSIString("1000")
    yellow = ansi.ANSIString("|yYellow:|n")
    yellow_cost = ansi.ANSIString("2000")
    green = ansi.ANSIString("|gGreen:|n")
    green_cost = ansi.ANSIString("4000")
    blue = ansi.ANSIString("|bBlue:|n")
    blue_cost = ansi.ANSIString("8000")
    indigo = ansi.ANSIString("|MIndigo:|n")
    indigo_cost = ansi.ANSIString("16000")
    violet = ansi.ANSIString("|mViolet:|n")
    violet_cost = ansi.ANSIString("32000")
    ultraviolet = ansi.ANSIString("|[W|XUltraviolet:|n")
    ultraviolet_cost = ansi.ANSIString("|y<ERROR>|n")

    table = evtable.EvTable("", "", "", "", "", "", header=None, border=None)

    table.reformat_column(0, width=16, align="l")
    table.reformat_column(1, width=10, align="r")
    table.reformat_column(2, width=16, align="l")
    table.reformat_column(3, width=10, align="r")
    table.reformat_column(4, width=16, align="l")
    table.reformat_column(5, width=10, align="r")

    table.add_row(red, red_cost, orange, orange_cost, yellow, yellow_cost)
    table.add_row(green, green_cost, blue, blue_cost, indigo, indigo_cost)
    table.add_row(violet, violet_cost, ultraviolet, ultraviolet_cost, "", "")

    text += str(table)

    options = ()

    if caller.db.clearance == 1:
        options += ({"desc": "Upgrade to Red", "exec": exec_clearance_upgrade, "goto": "upgrade_clearance"},)
    elif caller.db.clearance == 2:
        options += ({"desc": "Upgrade to Orange", "exec": exec_clearance_upgrade, "goto": "upgrade_clearance"},)
    elif caller.db.clearance == 3:
        options += ({"desc": "Upgrade to Yellow", "exec": exec_clearance_upgrade, "goto": "upgrade_clearance"},)
    elif caller.db.clearance == 4:
        options += ({"desc": "Upgrade to Green", "exec": exec_clearance_upgrade, "goto": "upgrade_clearance"},)
    elif caller.db.clearance == 5:
        options += ({"desc": "Upgrade to Blue", "exec": exec_clearance_upgrade, "goto": "upgrade_clearance"},)
    elif caller.db.clearance == 6:
        options += ({"desc": "Upgrade to Indigo", "exec": exec_clearance_upgrade, "goto": "upgrade_clearance"},)
    elif caller.db.clearance == 7:
        options += ({"desc": "Upgrade to Violet", "exec": exec_clearance_upgrade, "goto": "upgrade_clearance"},)
    elif caller.db.clearance == 8:
        options += ({"desc": "Upgrade to Ultraviolet", "exec": exec_clearance_upgrade, "goto": "upgrade_clearance"},)

    options += ({"key": ("back", "b"), "desc": "Go Back", "goto": "menu_start_node"},)

    return text, options


def exec_clearance_upgrade(caller, caller_input):
    current = caller.db.clearance
    prospective = CLEARANCE.get(current + 1)
    prospective_cost = CLEARANCE_UPGRADES.get(prospective)
    if caller.db.xp >= prospective_cost:
        caller.db.xp = caller.db.xp - prospective_cost
        caller.db.clearance += 1
    else:
        caller.msg("|rERROR:|n Not enough XP points to upgrade your clearance level.")


def upgrade_skills(caller):
    if hasattr(caller.ndb._menutree, "selected_skill"):
        exec_upgrade_skill(caller, caller.ndb._menutree.selected_skill)

    text = "I know that there were limitations to your skill packages during the cloning process, but once you are " \
           "out, you can incrementally improve your various skills through a mix of virtual reality training, " \
           "chemical injections, electroshock therapy, radioactive neural implantation and good, old fashioned " \
           "practice.  There are limits, knowing too much is bad for you.  In fact, I'm not sure you have the " \
           "clearance to have this conversation.  you shouldn't even be asking about all this.  |y<Personnel file " \
           "updated>|n\n\n Anyway, any skills that you can't download upgrades for will not be listed as options.  " \
           "Raising a skill 1 level costs 200 XP points.  Please select the skill you wish to upgrade."

    options = ()

    for skill, value in caller.db.skills.items():
        if value < 5:
            options += ({"desc": skill, "exec": _wrapper(caller, "selected_skill", skill), "goto": "upgrade_skills"},)

    options += ({"key": ("back", "b"), "desc": "Go Back", "goto": "menu_start_node"},)
    return text, options


def exec_upgrade_skill(caller, caller_input):
    skill = caller.ndb._menutree.selected_skill
    if caller.db.xp >= 200:
        caller.db.xp = caller.db.xp - 200
        caller.db.skills[skill] += 1
    else:
        caller.msg("|rERROR:|n You do not have enough XP to raise that skill.")


def upgrade_stats(caller):
    if hasattr(caller.ndb._menutree, "selected_stat"):
        exec_upgrade_stat(caller, caller.ndb._menutree.selected_stat)
    text = "So you wanna upgrade your Core modules?  What?  You don't know what that is?  You probably know them as " \
           "'stats'.  Such a sophomoric name for such a complex neural structure.  Well, based on what I'm seeing " \
           "here, maybe a few upgrades would be a good idea.  There are limits, just so you know.  No hacking to " \
           "upgrade yourself to a god or whatnot.  God isn't even real!  At least that's what my priest says.\n\nWhere " \
           "was I?  Oh yes, Core Modules.  Pick the one you want to upgrade.  Each upgrade point costs 500 XP Points."
    options = ()
    for stat, value in tuple(caller.db.stats.items()):
        if value < 3:
            options += ({"desc": stat, "exec": _wrapper(caller, "selected_stat", stat), "goto": "upgrade_stats"},)

    options += ({"key": ("back", "b"), "desc": "Go Back", "goto": "menu_start_node"},)
    return text, options


def exec_upgrade_stat(caller, caller_input):
    stat = caller_input
    if caller.db.xp >= 500:
        caller.db.xp = caller.db.xp - 500
        caller.db.stats[stat] += 1
    else:
        caller.msg("|rERROR:|n You do not have enough XP to raise that stat.")


def upgrade_moxie(caller):
    text = "Feeling stressed?  It's understandable, if mildly treasonous.  Your friend, the Computer has you covered!  " \
           "You've got Moxie kid, I like you.  You just need to chill out.  Moxie is a measure of your mental health " \
           "that I've offered to you in a convenient number system.  A newly spawned clone starts off with a nice " \
           "calm and health 6 in Moxie.  One thing that helps restore Moxie after you've had a rough day is to " \
           "reflect on a pleasant memory.  Of course, being a clone, you have a limited lifespan to draw positive " \
           "memories from, so I'm here to sell you some!  For a measly 50 XP Points, I will activate a pre-built " \
           "memory stored in your Cerebral Coretech.  For 200 XP Points, I will upload new, exciting memories to your " \
           "hippocampus.  But I've found that too many pleasant memories makes clones anxious and unhappy about the " \
           "present.  And since |yHAPPINESS IS MANDATORY|n there are limits placed on the amount of memories available."

    options = ()
    if caller.db.moxie != caller.db.max_moxie:
        options = ({"desc": "Restore Moxie", "exec": exec_restore_moxie, "goto": "upgrade_moxie"},)

    if caller.db.max_moxie < 8:
        options = ({"desc": "Upgrade Moxie", "exec": exec_upgrade_moxie, "goto": "upgrade_moxie"},)

    options += ({"key": ("back", "b"), "desc": "Go Back", "goto": "menu_start_node"},)
    return text, options


def exec_restore_moxie(caller, caller_input):
    if caller.db.xp >= 50:
        caller.db.xp = caller.db.xp - 50
        caller.db.moxie += 1
    else:
        caller.msg("|rERROR:|n You do not have enough XP to restore Moxie.")


def exec_upgrade_moxie(caller, caller_input):
    if caller.db.xp >= 200:
        caller.db.xp = caller.db.xp - 200
        caller.db.max_moxie += 1
        caller.db.moxie += 1
    else:
        caller.msg("|rERROR:|n You do not have enough XP to upgrade your Moxie.")


def upgrade_equipment(caller):
    if hasattr(caller.ndb._menutree, "selected_equipment"):
        exec_purchase_equipment(caller, caller.ndb._menutree.selected_equipment)
    text = "What good is a Troubleshooter without equipment.  Well, usually still not very good, but necessary!  " \
           "Watching a bunch of clones trying to put out a trash fire with only lighter fluid canisters is " \
           "entertaining, but not very productive.  So I'm offering you some items for purchase along with the " \
           "mission assigned equipment you will receive to help you on your vital missions for the Computer and the " \
           "Alpha Complex.  The fate of our home is in your hands.  God, I wish I could upgrade my Moxie."
    options = ()

    for name, dic in EQUIPMENT.items():
        options += (
        {"desc": "{} - |y{}|n".format(name, dic.get("cost")), "exec": _wrapper(caller, "selected_equipment", dic),
         "goto": "upgrade_equipment"},)

    options += ({"key": ("back", "b"), "desc": "Go Back", "goto": "menu_start_node"},)
    return text, options


def exec_purchase_equipment(caller, caller_input):
    if caller.db.xp >= caller_input.get("cost"):
        caller.db.xp = caller.db.xp - caller_input.get("cost")
        caller_input["location"] = caller.dbref
        spawner.spawn(caller_input)
    else:
        caller.msg("|rERROR:|n You cannot afford that piece of equipment.")


def recharge_equipment(caller):
    text = "Without ammo a weapons is just a hunk of precision crafted and laser cut carbon nano-tube, printed junk.  " \
           "But, as they say, nothing in life is free.  (Brought to you by Carbo-fizz™)\n\nBelow you will find a list " \
           "of the equipment in your inventory.  Select the one that you want to reload."

    options = ()

    for item in caller.contents:
        if not item.db.consumable and item.db.uses > -1:
            options += ({"desc": "{} - |y{}|n".format(item.key, item.db.cost // 2), "goto": (_exec_recharge_equipment,
                                                                                             {"selected": item})},)
    options += ({"key": ("back", "b"), "desc": "Go Back", "goto": "menu_start_node"},)
    return text, options


def _exec_recharge_equipment(caller, raw_string, **kwargs):
    pass


def purchase_clones(caller):
    text = "\"Reward is its own reward.\"  \nWait, that doesn't sound right.  \"Waiting comes to those who wait.\"  " \
           "\nNo, that's not right either.  One moment...\n\n|yLanguage Diagnostic...|n\n|y<Idiom not found.>|n\n\n" \
           "Hmm, well then let's keep this simple.  You want to live longer?  Spend XP Points and buy more clones.  " \
           "They cost 1000 XP Points."
    options = ({"desc": "Purchase Clone", "exec": exec_purchase_clone, "goto": "purchase_clones"},
               {"key": ("back", "b"), "desc": "Go Back", "goto": "menu_start_node"})
    return text, options


def exec_purchase_clone(caller, caller_input):
    if caller.db.xp >= 1000:
        caller.db.xp = caller.db.xp - 1000
        caller.db.max_clones += 1
    else:
        caller.msg("|rERROR:|n You cannot afford to buy a clone.")
