import time
import datetime
from random import randint
from evennia import default_cmds
from evennia.utils.evmenu import EvMenu
from evennia.utils import evtable, utils, ansi
from commands.library import clearance_color, IsInt, node_formatter, options_formatter, titlecase
from world.static_data import HEALTH, CLEARANCE, ACTIONS, MUTANT_POWERS, SECRET_SOCIETIES
from django.conf import settings
from evennia.server.sessionhandler import SESSIONS
from typeclasses.clones import Clone
from commands.chargen_commands import reset_random


class SheetCommand(default_cmds.MuxCommand):
    """
    Displays the Character sheet.

    Usage:
        |w+sheet|n - Normal Character sheet

        |w+sheet/secret|n - Shows Mutant powers and Secret societies

        |w+sheet/actions|n - Shows available actions.  Including Action Cards and Mutant powers.

    Admin Only:
        All versions of |w+sheet|n listed above with a name at the end.

        |w+sheet <name>|n
        |w+sheet/actions <name>|n
        |w+sheet/secret <name>|n
    """

    key = "+sheet"
    aliases = ["sheet"]
    locks = "cmd:perm(Player)"
    help_category = "General"

    def func(self):
        caller = None
        if self.args:
            if self.caller.locks.check_lockstring(self.caller, "dummy:perm(Admin)"):
                if Clone.objects.filter(db_key__iexact=self.args).exists():
                    caller = self.caller.search(self.args)
                else:
                    self.caller.msg("|rERROR:|n Invalid player name.  Try again.")
                    return
            else:
                self.caller.msg("|rERROR:|n You are not authorized to use that command.")
                return
        else:
            caller = self.caller
        if not self.switches:
            message = []
            message.append("|w.---|n|yAlpha Complex Identity Form|n|w----------------------------------------------.|n")
            message.append("|[002|w/// PART ONE    |n|[005 |wCORE INFORMATION >>>                                         |n")

            name = "|wName: |n{}-{}-{}".format(caller.key, caller.db.clone, caller.db.sector)
            clearance = "|wSecurity Clearance: |n{}".format(CLEARANCE.get(caller.db.clearance))
            sector = "|wHome Sector: |n{}".format(caller.db.sector or "")
            clone = "|wClone #: |n{} / {}".format(caller.db.clone, caller.db.max_clones)
            gender = "|wGender: |n{}".format(caller.db.gender)
            personality = "|wPersonality: |n{}".format(", ".join(caller.db.personality or []))

            table1 = evtable.EvTable(name, clearance, border=None)
            table1.reformat_column(0, width=30)
            table1.reformat_column(1, width=48)
            message.append(table1)

            table2 = evtable.EvTable(sector, clone, gender, border=None)
            table2.reformat_column(0, width=30)
            table2.reformat_column(1, width=18)
            table2.reformat_column(2, width=30)
            message.append(table2)
            message.append(" " + personality + "\n")

            message.append("|[002|w/// PART TWO    |n|[005 |wDEVELOPMENT >>>                                              |n")

            treason = "|wTreason: |n{}".format("*" * (caller.db.treason or 0))
            xp = "|wXP Points: |n{}".format(caller.db.xp or 0)
            table3 = evtable.EvTable(treason, xp, border=None)
            table3.reformat_column(0, width=30)
            table3.reformat_column(1, width=48)
            message.append(table3)
            message.append("\n")

            table4 = evtable.EvTable("", "", "", "", "", "", "", "",  border=None)
            table4.reformat_column(0, width=16)
            table4.reformat_column(1, width=3, align="r")
            table4.reformat_column(2, width=16)
            table4.reformat_column(3, width=3, align="r")
            table4.reformat_column(4, width=16)
            table4.reformat_column(5, width=3, align="r")
            table4.reformat_column(6, width=16)
            table4.reformat_column(7, width=3, align="r")

            table4.add_row("|wViolence: |n", caller.db.stats.get("violence"),
                           "|wBrains: |n", caller.db.stats.get("brains"),
                           "|wChutzpah: |n", caller.db.stats.get("chutzpah"),
                           "|wMechanics: |n", caller.db.stats.get("mechanics"))
            message.append("|[035|002 STATS >>>                                                                    " +
                           str(table4))
            message.append("\n")

            table5 = evtable.EvTable("", "", "", "", "", "", "", "",  border=None, header=False)
            table5.reformat_column(0, width=15)
            table5.reformat_column(1, width=4, align="r")
            table5.reformat_column(2, width=16)
            table5.reformat_column(3, width=4, align="r")
            table5.reformat_column(4, width=15)
            table5.reformat_column(5, width=4, align="r")
            table5.reformat_column(6, width=15)
            table5.reformat_column(7, width=4, align="r")

            table5.add_row("|wAthletics: |n", caller.db.skills.get("athletics"),
                           "|wScience: |n", caller.db.skills.get("science"),
                           "|wBluff: |n", caller.db.skills.get("bluff"),
                           "|wOperate: |n", caller.db.skills.get("operate"))

            table5.add_row("|wGuns: |n", caller.db.skills.get("guns"),
                           "|wPsychology: |n", caller.db.skills.get("psychology"),
                           "|wCharm: |n", caller.db.skills.get("charm"),
                           "|wEngineer: |n", caller.db.skills.get("engineer"))

            table5.add_row("|wMelee: |n", caller.db.skills.get("melee"),
                           "|wBureaucracy: |n", caller.db.skills.get("bureaucracy"),
                           "|wIntimidate: |n", caller.db.skills.get("intimidate"),
                           "|wProgram: |n", caller.db.skills.get("program"))

            table5.add_row("|wThrow: |n", caller.db.skills.get("throw"),
                           "|wAlpha Complex: |n", caller.db.skills.get("alpha complex"),
                           "|wStealth: |n", caller.db.skills.get("stealth"),
                           "|wDemolitions: |n", caller.db.skills.get("demolitions"))
            message.append(
                "|[002|w/// PART THREE  |n|[005 |wSKILLS >>>                                                   |n" +
                str(table5))
            message.append("\n")
            # message.append(unicode(table5) + "\n")

            message.append(
                "|[002|w/// PART FOUR   |n|[005 |wWELLBEING >>>                                                |n")

            moxie = "|wMoxie: |n{} / {}".format(caller.db.moxie, caller.db.max_moxie)
            health = "|wHealth: |n{}".format(HEALTH.get(caller.db.wounds))

            table9 = evtable.EvTable(moxie, health, border=None)
            table9.reformat_column(0, width=28)
            table9.reformat_column(1, width=50)
            message.append(table9)
            message.append("\n")

            message.append(
                "|[002|w/// PART FIVE   |n|[005 |wEQUIPMENT >>>                                                |n")

            equipment = [eq for eq in caller.contents]
            for eq in equipment:
                message.append(eq.key)

            message.append("\n")
            message.append("*|w---------------------------------------------------" + "|500This form is MANDATORY|w---|n*")
            message2 = []
            for line in message:
                message2.append(line)
            self.caller.msg("\n".join(str(m) for m in message2))
        elif "actions" in self.switches:
            message = []
            message.append("|w.---|n|yAction Summary Form|n|w------------------------------------------------------.|n")
            message.append("|[035|002 ACTIONS >>>                                                                  ")
            action_table = evtable.EvTable("|wAction:|n", "|wAction Order:|n", "|wReaction:|n", "|wDescription:|n", border=None)

            action_table.reformat_column(0, width=17, valign="t")
            action_table.reformat_column(1, width=15, valign="t")
            action_table.reformat_column(2, width=11, valign="t")
            action_table.reformat_column(3, width=35, valign="t")

            for act in caller.db.action_cards:
                action = ACTIONS.get(act)
                action_table.add_row(titlecase(act), action.get("action_order"), "Y" if action.get("reaction") == 1 else "N", action.get("desc"))

            message.append(action_table)
            message.append("\n|[035|002 MUTANT POWERS >>>                                                            |n")

            mutant_table = evtable.EvTable("|wPower:|n", "|wAction Order:|n", "|wDescription:|n", border=None)

            mutant_table.reformat_column(0, width=20, valign="t")
            mutant_table.reformat_column(1, width=15, valign="t")
            mutant_table.reformat_column(2, width=43, valign="t")

            mutant = MUTANT_POWERS.get(caller.db.mutant_power)
            mutant_table.add_row(titlecase(caller.db.mutant_power), mutant.get("action_order"), mutant.get("description"))
            message.append("*" + "|w-|n" * 76 + "*")
            message.append(mutant_table + "\n")
            self.caller.msg("\n".join(message))
        elif "secret" in self.switches:
            message = []
            message.append("|w.---|n|ySecret Information Form|n|w--------------------------------------------------.|n")
            message.append("|[035|002 MUTANT POWERS >>>                                                             ")
            mutant_table = evtable.EvTable("|wPower:|n", "|wAction Order:|n", "|wDescription:|n", border=None)

            mutant_table.reformat_column(0, width=20, valign="t")
            mutant_table.reformat_column(1, width=15, valign="t")
            mutant_table.reformat_column(2, width=43, valign="t")

            mutant = MUTANT_POWERS.get(caller.db.mutant_power)
            mutant_table.add_row(titlecase(caller.db.mutant_power), mutant.get("action_order"), mutant.get("description"))

            message.append(mutant_table + "\n")
            message.append("|[035|002 SECRET SOCIETIES >>>                                                          ")

            ss_table = evtable.EvTable("|wSociety:|n", "|wKeywords:|n", "|wBeliefs|n:", "|wGoals|n:", border=None)

            ss_table.reformat_column(0, width=15, valign="t")
            ss_table.reformat_column(1, width=13, valign="t")
            ss_table.reformat_column(2, width=25, valign="t")
            ss_table.reformat_column(3, width=25, valign="t")

            for soc in caller.db.secret_societies:
                society = SECRET_SOCIETIES.get(soc)
                ss_table.add_row(titlecase(soc), ", ".join(society.get("keywords")), society.get("beliefs"), society.get("goals"))

            message.append(ss_table)
            message.append("*" + "|w-|n" * 76 + "*")
            self.caller.msg("\n".join(message))

class TimeCommand(default_cmds.MuxCommand):
    """
    Displays the IC date and time.
    """
    key = "+time"
    aliases = ["time"]
    locks = "cmd:perm(Player)"
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
    locks = "cmd:all()"
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
        EvMenu(self.caller, "commands.catalog_menu",
               startnode="menu_start_node",
               cmdset_mergetype="Replace",
               node_formatter=node_formatter,
               options_formatter=options_formatter,
               cmd_on_exit="look")

class DieCommand(default_cmds.MuxCommand):
    """
    Increments your clone number and resets your health.  If you are out of clones, it will reset your character
    sheet and teleport you to the Incubation Chamber to start a new character generation sequence.

    Usage:
        |w+die|n
    """

    key = "+die"
    locks = "cmd:perm(Player)"
    help_category = "General"

    def func(self):
        if not self.caller.db.die:
            self.caller.msg("|bSYSTEM:|n Are you absolutely sure you want to die?  Have you begged the GM and offered "
                            "'favors' or other bribes?  If you are sure, type |w+die|n again.")
            self.caller.db.die = 1
        else:
            del self.caller.db.die
            if self.caller.db.clone < self.caller.db.max_clones:
                self.caller.msg("|bSYSTEM:|n Incrementing and dispatching clone.")
                self.caller.db.clone += 1
            else:
                self.caller.msg("|bSYSTEM:|n You are dead bro.  Your usefulness is not over, however.  Your body will "
                                "be recycled and reused in other ways.  Incidentally, try our new product at the mess "
                                "hall, Beefy Cakes(tm)  Now made with real meat!")
                reset_random(self.caller)
                start = self.caller.search("Incubation Chamber", global_search=True)
                self.caller.move_to(start)
                self.caller.db.chargen_complete = 0
                self.caller.db.max_clones = 6
                self.caller.db.max_moxie = 6

class PlayActionCommand(default_cmds.MuxCommand):
    """
    Menu to allow a player to select the action they want to take.  This includes Action Cards, Mutant Powers and Equipment.

    Usage:
        |w+actions|n

        |YAlso see: |n|yhelp Combat|n
    """

    key = "+actions"
    locks = "cmd:perm(Player)"
    help_category = "Combat"

    def func(self):
        EvMenu(self.caller, "commands.action_menu",
               startnode="menu_start_node",
               cmdset_mergetype="Replace",
               node_formatter=node_formatter,
               options_formatter=options_formatter,
               cmd_on_exit="look")

class SpendMoxieCommand(default_cmds.MuxCommand):
    """
    Reduces the number of Moxie by one.  Usually used in association with using Mutant Powers, adding dice to a
    roll and other uses as determined by the GM or Storyteller.

    Usage:
        |w+spend Moxie|n
    """
