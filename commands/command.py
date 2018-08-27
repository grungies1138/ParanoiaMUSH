"""
Commands

Commands describe the input the account can do to the game.

"""
import time
import datetime
from evennia import Command as BaseCommand
from evennia import default_cmds
from evennia.utils import evtable, utils
from world.static_data import HEALTH, CLEARANCE
from django.conf import settings
from evennia.server.sessionhandler import SESSIONS


class Command(BaseCommand):
    """
    Inherit from this if you want to create your own command styles
    from scratch.  Note that Evennia's default commands inherits from
    MuxCommand instead.

    Note that the class's `__doc__` string (this text) is
    used by Evennia to create the automatic help entry for
    the command, so make sure to document consistently here.

    Each Command implements the following methods, called
    in this order (only func() is actually required):
        - at_pre_cmd(): If this returns True, execution is aborted.
        - parse(): Should perform any extra parsing needed on self.args
            and store the result on self.
        - func(): Performs the actual work.
        - at_post_cmd(): Extra actions, often things done after
            every command, like prompts.

    """
    pass

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

        name = "|wName: |n{}".format(self.caller.key)
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

        table = evtable.EvTable(" "," |[002|wName:|n", "|[002|wIdle:|n", "|[002|wConn:|n", "|[002|wClearance:|n", table=None,
                                border=None, width=78)

        for session in session_list:
            player = session.get_account()
            idle = time.time() - session.cmd_last_visible
            conn = time.time() - session.conn_time
            if session.get_puppet():
                clearance = session.get_puppet().db.clearance
            else:
                clerarance = 1
            flag = None
            if player.locks.check_lockstring(player, "dummy:perm(Admin)"):
                flag = "|y!|n"
            elif player.locks.check_lockstring(player, "dummy:perm(Builder)"):
                flag = "|g&|n"
            elif player.locks.check_lockstring(player, "dummy:perm(Helper)"):
                flag = "|r$|n"
            else:
                flag = " "
            table.add_row(flag, utils.crop(player.name), utils.time_format(idle, 0),
                          utils.time_format(conn, 0), CLEARANCE.get(clearance))

        table.reformat_column(0, width=2)
        table.reformat_column(0, width=24)
        table.reformat_column(1, width=12)
        table.reformat_column(2, width=12)
        table.reformat_column(3, width=28)

        self.caller.msg("|b-|n" * 78)
        self.caller.msg("|y{}|n".center(78).format(settings.SERVERNAME))
        self.caller.msg("|b-|n" * 78)
        self.caller.msg(table)
        self.caller.msg("|b-|n" * 78)
        self.caller.msg("Total Connected: %s" % SESSIONS.account_count())
        whotable = evtable.EvTable("", "", "", header=False, border=None)
        whotable.reformat_column(0, width=26)
        whotable.reformat_column(1, width=26)
        whotable.reformat_column(2, width=26)
        whotable.add_row("|y!|n - Administrators", "|g&|n - Storytellers", "|r$|n - Player Helpers")
        self.caller.msg(whotable)
        self.caller.msg("|b-|n" * 78)
