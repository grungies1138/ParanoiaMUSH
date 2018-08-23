"""
Commands

Commands describe the input the account can do to the game.

"""
import datetime
from evennia import Command as BaseCommand
from evennia import default_cmds
from evennia.utils import evtable
from world.static_data import HEALTH


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
        clearance = "|wSecurity Clearance: |n{}".format(self.caller.db.clearance or "")
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
    Displays the IC time.
    """

    key = "+time"
    aliases = ["time"]
    lock = "cmd:perm(Player)"
    help_category = "General"

    def func(self):
        month, day = datetime.datetime.now().strftime("%B"), datetime.datetime.now().day
        self.caller.msg("|[002|w/// ALPHA COMPLEX TIME SERVICE                                                |N")
        self.caller.msg("|wCurrent Date and Time:|n {} {}, 214 {}".format(month, day, datetime.datetime.now().strftime("%X")))