"""
Commands

Commands describe the input the account can do to the game.

"""
import time
import datetime
from random import randint
from evennia import default_cmds
from evennia.utils.evmenu import EvMenu
from evennia.utils import evtable, utils, ansi, spawner
from commands.library import clearance_color, _wrapper, IsInt
from world.static_data import HEALTH, CLEARANCE, CLEARANCE_UPGRADES
from django.conf import settings
from evennia.server.sessionhandler import SESSIONS
from typeclasses.clones import Clone
from world.equipment_prototypes import EQUIPMENT


class SheetCommand(default_cmds.MuxCommand):
    """
    Displays the Character sheet.
    """

    key = "+sheet"
    aliases = ["sheet"]
    lock = "cmd:perm(Player)"
    help_category = "General"

    def func(self):
        message = []
        message.append("|w.---|n|yAlpha Complex Identity Form|n|w----------------------------------------------.|n")
        message.append("|[002|w/// PART ONE    |n|[005 |wCORE INFORMATION >>>                                         |n")

        name = "|wName: |n{}-{}-{}".format(self.caller.key, self.caller.db.clone, self.caller.db.sector)
        clearance = "|wSecurity Clearance: |n{}".format(CLEARANCE.get(self.caller.db.clearance))
        sector = "|wHome Sector: |n{}".format(self.caller.db.sector or "")
        clone = "|wClone #: |n{}".format(self.caller.db.clone)
        gender = "|wGender: |n{}".format(self.caller.db.gender)
        personality = "|wPersonality: |n{}".format(", ".join(self.caller.db.personality or []))

        table1 = evtable.EvTable(name, clearance, border=None)
        table1.reformat_column(0, width=30)
        table1.reformat_column(1, width=48)
        message.append(unicode(table1))

        table2 = evtable.EvTable(sector, clone, gender, border=None)
        table2.reformat_column(0, width=30)
        table2.reformat_column(1, width=18)
        table2.reformat_column(2, width=30)
        message.append(unicode(table2))
        message.append(" " + personality + "\n")

        message.append("|[002|w/// PART TWO    |n|[005 |wDEVELOPMENT >>>                                              |n")

        treason = "|wTreason: |n{}".format("*" * (self.caller.db.treason or 0))
        xp = "|wXP Points: |n{}".format(self.caller.db.xp or 0)
        table3 = evtable.EvTable(treason, xp, border=None)
        table3.reformat_column(0, width=30)
        table3.reformat_column(1, width=48)
        message.append(unicode(table3) + "\n")


        table4 = evtable.EvTable("", "", "", "", "", "", "", "",  border=None)
        table4.reformat_column(0, width=16)
        table4.reformat_column(1, width=3, align="r")
        table4.reformat_column(2, width=16)
        table4.reformat_column(3, width=3, align="r")
        table4.reformat_column(4, width=16)
        table4.reformat_column(5, width=3, align="r")
        table4.reformat_column(6, width=16)
        table4.reformat_column(7, width=3, align="r")

        table4.add_row("|wViolence: |n", self.caller.db.stats.get("violence"),
                       "|wBrains: |n", self.caller.db.stats.get("brains"),
                       "|wChutzpah: |n", self.caller.db.stats.get("chutzpah"),
                       "|wMechanics: |n", self.caller.db.stats.get("mechanics"))
        message.append("|[035|002 STATS >>>                                                                    " +
                       unicode(table4) + "\n")
        # message.append(unicode(table4) + "\n")



        table5 = evtable.EvTable("", "", "", "", "", "", "", "",  border=None, header=False)
        table5.reformat_column(0, width=15)
        table5.reformat_column(1, width=4, align="r")
        table5.reformat_column(2, width=16)
        table5.reformat_column(3, width=4, align="r")
        table5.reformat_column(4, width=15)
        table5.reformat_column(5, width=4, align="r")
        table5.reformat_column(6, width=15)
        table5.reformat_column(7, width=4, align="r")

        table5.add_row("|wAthletics: |n", self.caller.db.skills.get("athletics"),
                       "|wScience: |n", self.caller.db.skills.get("science"),
                       "|wBluff: |n", self.caller.db.skills.get("bluff"),
                       "|wOperate: |n", self.caller.db.skills.get("operate"))

        table5.add_row("|wGuns: |n", self.caller.db.skills.get("guns"),
                       "|wPsychology: |n", self.caller.db.skills.get("psychology"),
                       "|wCharm: |n", self.caller.db.skills.get("charm"),
                       "|wEngineer: |n", self.caller.db.skills.get("engineer"))

        table5.add_row("|wMelee: |n", self.caller.db.skills.get("melee"),
                       "|wBureaucracy: |n", self.caller.db.skills.get("bureaucracy"),
                       "|wIntimidate: |n", self.caller.db.skills.get("intimidate"),
                       "|wProgram: |n", self.caller.db.skills.get("program"))

        table5.add_row("|wThrow: |n", self.caller.db.skills.get("throw"),
                       "|wAlpha Complex: |n", self.caller.db.skills.get("alpha complex"),
                       "|wStealth: |n", self.caller.db.skills.get("stealth"),
                       "|wDemolitions: |n", self.caller.db.skills.get("demolitions"))
        message.append(
            "|[002|w/// PART THREE  |n|[005 |wSKILLS >>>                                                   |n" +
            unicode(table5) + "\n")
        # message.append(unicode(table5) + "\n")

        message.append(
            "|[002|w/// PART FOUR   |n|[005 |wWELLBEING >>>                                                |n")

        moxie = "|wMoxie: |n{}".format(self.caller.db.moxie or 0)
        health = "|wHealth: |n{}".format(HEALTH.get(self.caller.db.wounds))

        table9 = evtable.EvTable(moxie, health, border=None)
        table9.reformat_column(0, width=28)
        table9.reformat_column(1, width=50)
        message.append(unicode(table9) + "\n")

        message.append(
            "|[002|w/// PART FIVE   |n|[005 |wEQUIPMENT >>>                                                |n")

        equipment = [eq for eq in self.caller.contents]
        for eq in equipment:
            message.append(eq.key)

        message.append("\n")
        message.append("*|w---------------------------------------------------" + "|500This form is MANDATORY|w---|n*")
        self.caller.msg("\n".join(message))

class TimeCommand(default_cmds.MuxCommand):
    """
    Displays the IC date and time.
    """
    key = "+time"
    aliases = ["time"]
    lock = "cmd:perm(Player)"
    help_category = "General"

    def func(self):
        month, day = datetime.datetime.now().strftime("%B"), datetime.datetime.now().day
        self.caller.msg("|[002|w/// ALPHA COMPLEX TIME SERVICE                                                |n")
        self.caller.msg("|wCurrent Date and Time:|n {} {}, 214 {}"
                        .format(month, day,datetime.datetime.now().strftime("%I:%M:%S %P")))
        self.caller.msg("\n|[035|002 Notable Epochs >>>                                                           |n")
        self.caller.msg("|wInvention of the Hot Cold Fusion Reactor:|n April 28, 214")
        self.caller.msg("|wDeath of famous programmer ANI-12-FTT-2:|n November 5, 214")
        self.caller.msg("|wIntroduction of Dazzling Blue Raspberry PoppyFizz soda:|n January 2, 214")
        self.caller.msg("|w100th anniversary of Dazzling Blue Raspberry PoppyFizz soda:|n January 2, 214")

class OOCCommand(default_cmds.MuxCommand):
    """
    Send an OOC message just to the people in your current room.
    Usage:
        ooc [:, ;]<text>
    """

    key = "ooc"
    aliases = []
    lock = "cmd:all()"
    help_category = "General"

    def func(self):
        if not self.args:
            self.caller.msg("Huh?")

        prefix = "|w<|n|005OOC|n|w>|n"

        speech = self.args.strip()

        if speech[0] == ":":
            speech_text = speech[1:]
            self.caller.location.msg_contents("%s %s %s" % (prefix, self.caller.name, speech_text))
        elif speech[0] == ";":
            speech_text = speech[1:]
            self.caller.location.msg_contents("%s %s%s" % (prefix, self.caller.name, speech_text))
        else:
            self.caller.location.msg_contents("%s %s says, \"%s\"" % (prefix, self.caller.name, speech))

class WhoCommand(default_cmds.MuxCommand):
    """
    Shows the currently connected players.
    Usage:
        who
        +who
    """

    key = "+who"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        session_list = SESSIONS.get_sessions()

        table = evtable.EvTable(" |w|uName:|n", "|w|uIdle:|n", "|w|uConn:|n", "|w|uClearance:|n", table=None,
                                border=None, width=78)

        for session in session_list:
            player = session.get_account()
            idle = time.time() - session.cmd_last_visible
            conn = time.time() - session.conn_time
            clearance = session.get_puppet().db.clearance
            flag = None
            if player.locks.check_lockstring(player, "dummy:perm(Admin)"):
                flag = "|y!|n"
            elif player.locks.check_lockstring(player, "dummy:perm(Builder)"):
                flag = "|g&|n"
            elif player.locks.check_lockstring(player, "dummy:perm(Helper)"):
                flag = "|r$|n"
            else:
                flag = " "
            table.add_row(flag + utils.crop(player.name), utils.time_format(idle, 0),
                          utils.time_format(conn, 0), "|{}{}|n".format(clearance_color(CLEARANCE.get(clearance)),
                                                                       CLEARANCE.get(clearance)))

        table.reformat_column(0, width=24)
        table.reformat_column(1, width=12)
        table.reformat_column(2, width=12)
        table.reformat_column(3, width=30)

        self.caller.msg("|w_|n" * 78)
        title = ansi.ANSIString("|[002|w|u{}|n".format(settings.SERVERNAME))
        self.caller.msg(title.center(78, '^').replace('^',"|[002|w_|n"))

        self.caller.msg(table)
        self.caller.msg("|w_|n" * 78)
        self.caller.msg("Total Connected: %s" % SESSIONS.account_count())
        whotable = evtable.EvTable("", "", "", header=False, border=None)
        whotable.reformat_column(0, width=26)
        whotable.reformat_column(1, width=26)
        whotable.reformat_column(2, width=26)
        whotable.add_row("|y!|n - Administrators", "|g&|n - Storytellers", "|r$|n - Player Helpers")
        self.caller.msg(whotable)
        self.caller.msg("|w_|n" * 78 + "\n")

class CheckCommand(default_cmds.MuxCommand):
    """
    Checks a skill and returns the number of successes and the result of the Computer Die.

    Usage:

        |w+check <skill>+<stat>[+ or - <mod>]

        |yExample: |n +check guns+violence or +check science+brains+2
    """

    key = "+check"
    locks = "cmd:perm(Player)"
    help_category = "General"

    def func(self):
        caller = self.caller
        stats = caller.db.stats.keys()
        skills = caller.db.skills.keys()
        pos_mod = 0
        neg_mod = 0

        if "+" not in self.args:
            caller.msg("|rERROR:|n Invalid input.  |w+check <skill>+<stat>[+/- <mod>]|n")
            return
        args = [arg.strip() for arg in self.args.split("+")]

        if len(args) > 2:
            if not IsInt(args[2]):
                caller.msg("|rERROR:|n Invalid modifier.  Check modifiers must be an integer.  Try again.")
                return
            else:
                pos_mod = int(args[2])
        elif "-" in args[1]:
            neg_args = [arg.strip() for arg in args[1].split("-")]

            args[1] = neg_args[0]
            if not IsInt(neg_args[1]):
                caller.msg("|rERROR:|n Invalid modifier.  Check modifiers must be an integer.  Try again.")
                return
            else:
                neg_mod = int(neg_args[1]) * -1

        if args[0] not in skills:
            caller.msg("|rERROR:|n {} is not a valid skill.  Please select a valid skill and try again.".format(args[0]))
            return
        elif args[1] not in stats:
            caller.msg("|rERROR:|n {} is not a valid stat.  Please select a valid stat and try again.".format(args[1]))
            return
        else:
            selected_skill = caller.db.skills.get(args[0])
            if selected_skill < 0:
                selected_skill = 0
            selected_stat = caller.db.stats.get(args[1])
            if selected_stat < 0:
                selected_stat = 0

            successes = 0
            print("selected_stat: {}".format(selected_stat))
            print("selected_skill: {}".format(selected_skill))
            print("Positive Mod: {}".format(pos_mod))
            print("Negative Mod: {}".format(neg_mod))
            for i in range(selected_stat + selected_skill + pos_mod + neg_mod):
                result = randint(1, 6)
                if result > 4:
                    successes += 1

            computer_die = randint(1, 6)

            if computer_die == 6:
                caller.location.msg_contents("|bDICE:|n Number of successes: {}  |yCOMPUTER DIE|n".format(successes))
            else:
                caller.location.msg_contents("|bDICE:|n Number of successes: {}".format(successes))

class XPAwardCommand(default_cmds.MuxCommand):
    """
    Grants XP awards to a character.

    Usage:
        |w+award <name>=<amount>|n
    """

    key = "+award"
    locks = "cmd:perm(Admin)"
    help_category = "Admin"

    def func(self):
        if not self.args:
            self.caller.msg("|rERROR:|n Invalid input.  Usage is |w+award <name>=<amount>|n  Please try again.")
            return

        if "=" not in self.args:
            self.caller.msg("|rERROR:|n Invalid input.  Usage is |w+award <name>=<amount>|n  Please try again.")
            return

        if not self.lhs or not self.rhs:
            self.caller.msg("|rERROR:|n Invalid input.  Usage is |w+award <name>=<amount>|n  Please try again.")
            return

        char, amount = self.lhs, int(self.rhs)

        if Clone.objects.filter(db_key__iexact=char).exists():
            char = self.caller.search(char, global_search=True)
            char.db.xp += amount
            self.caller.msg("|bSYSTEM:|n {} XP points granted to {}".format(amount, char.key))
            char.msg("|bSYSTEM:|n You have been granted {} XP points by {}".format(amount, self.caller.key))

class CatalogCommand(default_cmds.MuxCommand):
    """
    A menu system for spending earned XP points.

    Usage:
        |w+advance|n
    """

    key = "+catalog"
    locks = "cmd:perm(Player)"
    help_category = "General"

    def func(self):
        EvMenu(self.caller, "commands.command",
               startnode="menu_start_node",
               cmdset_mergetype="Replace",
               node_formatter=node_formatter,
               options_formatter=options_formatter,
               cmd_on_exit="look")


# XP point costs:
# Recover Moxie: 50 XP points per point > Calming Alpha Wave moderator
# Increase Moxie: 200 per new level (Maximum 8)

def menu_start_node(caller):
    text = "Welcome to the Cerebral Coretech Alpha Complex XP point award catalog!  Many years ago, in the year 214, " \
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
               {"desc": "Purchase Clones", "goto": "buy_clones"})
    return text, options

def upgrade_clearance(caller):
    text = "The Peter Principle: People tend to be promoted to their own level of incompetence.\n\nWith enough time, " \
           "patience and luck, clones like you can rise through the ranks of security clearances.  Legend has it " \
           "that TOM-92 (who doesn't exist) was once an Infrared.  See the list of security clearances below along " \
           "with the associated XP Point costs.  And remember those costs are cumulative.\n\nExample: To go from " \
           "Infrared to Red costs 500 XP Points.  Likewise to go from Red to Orange costs 1000 XP Points.  Therefore " \
           "to go from Infrared to Orange costs a total of 1500 XP Points.\n\n|wCurrent Clearance:|n {}"\
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

    text += unicode(table)

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

    options += ({"key": "back", "desc": "Go Back", "goto": "menu_start_node"},)

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

    for skill, value in caller.db.skills.iteritems():
        if value < 5:
            options += ({"desc": skill, "exec": _wrapper(caller, "selected_skill", skill), "goto": "upgrade_skills"},)

    options += ({"key": "back", "desc": "Go Back", "goto": "menu_start_node"},)
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
    for stat, value in caller.db.stats.iteritems():
        if value < 3:
            options += ({"desc": stat, "exec": _wrapper(caller, "selected_stat", stat), "goto": "upgrade_stats"},)

    options += ({"key": "back", "desc": "Go Back", "goto": "menu_start_node"},)
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
           "memory stored in your Cerebral Coretech.  For 500 XP Points, I will upload new, exciting memories to your " \
           "hippocampus.  But I've found that too many pleasant memories makes clones anxious and unhappy about the " \
           "present.  And since |yHAPPINESS IS MANDATORY|n there are limits placed on the amount of memories available."

    options = ()
    if caller.db.moxie != caller.db.max_moxie:
        options = ({"desc": "Restore Moxie", "exec": exec_restore_moxie, "goto": "upgrade_moxie"},)

    if caller.db.max_moxie < 8:
        options = ({"desc": "Upgrade Moxie", "exec": exec_upgrade_moxie, "goto": "upgrade_moxie"},)

    options += ({"key": "back", "desc": "Go Back", "goto": "menu_start_node"},)
    return text, options

def exec_restore_moxie(caller, caller_input):
    if caller.db.xp >= 50:
        caller.db.xp = caller.db.xp - 50
        caller.db.moxie += 1
    else:
        caller.msg("|rERROR:|n You do not have enough XP to restore Moxie.")

def exec_upgrade_moxie(caller, caller_input):
    if caller.db.xp >= 500:
        caller.db.xp = caller.db.xp - 500
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
           "mission assigned equipment you weill receive to help you on your vital missions for the Computer and the " \
           "Alpha Complex.  The fate of our home is in your hands.  God, I wish I could upgrade my Moxie."
    options = ()

    for name, dic in EQUIPMENT.iteritems():
        options += ({"desc": "{} - {}".format(name, dic.get("cost")), "exec": _wrapper(caller, "selected_equipment", dic)},)
    return text, options

def exec_purchase_equipment(caller, caller_input):
    if caller.db.xp >= caller_input.get("cost"):
        caller.db.xp = caller.db.xp - caller_input.get("cost")
        caller_input["location"] = caller.dbref
        spawner.spawn(caller_input)
    else:
        caller.msg("|rERROR:|n You cannot afford that piece of equipment.")

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
            colA = options[:len(options) / 2 + 1]
            colB = options[len(options) / 2 + 1:]
        else:
            colA = options[:len(options) / 2]
            colB = options[len(options) / 2:]
        table = evtable.EvTable(table=[colA, colB], border=None)

        table.reformat_column(0, width=39)
        table.reformat_column(1, width=39)

        return str(table) + "\n"

    else:
        return "\n".join(options)
