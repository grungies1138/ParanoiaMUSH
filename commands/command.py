"""
Commands

Commands describe the input the account can do to the game.

"""

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
        table5.reformat_column(0, width=16)
        table5.reformat_column(1, width=4, align="r")
        table5.reformat_column(2, width=16)
        table5.reformat_column(3, width=4, align="r")
        table5.reformat_column(4, width=16)
        table5.reformat_column(5, width=4, align="r")
        table5.reformat_column(6, width=16)
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



# -------------------------------------------------------------
#
# The default commands inherit from
#
#   evennia.commands.default.muxcommand.MuxCommand.
#
# If you want to make sweeping changes to default commands you can
# uncomment this copy of the MuxCommand parent and add
#
#   COMMAND_DEFAULT_CLASS = "commands.command.MuxCommand"
#
# to your settings file. Be warned that the default commands expect
# the functionality implemented in the parse() method, so be
# careful with what you change.
#
# -------------------------------------------------------------

# from evennia.utils import utils
#
#
# class MuxCommand(Command):
#     """
#     This sets up the basis for a MUX command. The idea
#     is that most other Mux-related commands should just
#     inherit from this and don't have to implement much
#     parsing of their own unless they do something particularly
#     advanced.
#
#     Note that the class's __doc__ string (this text) is
#     used by Evennia to create the automatic help entry for
#     the command, so make sure to document consistently here.
#     """
#     def has_perm(self, srcobj):
#         """
#         This is called by the cmdhandler to determine
#         if srcobj is allowed to execute this command.
#         We just show it here for completeness - we
#         are satisfied using the default check in Command.
#         """
#         return super(MuxCommand, self).has_perm(srcobj)
#
#     def at_pre_cmd(self):
#         """
#         This hook is called before self.parse() on all commands
#         """
#         pass
#
#     def at_post_cmd(self):
#         """
#         This hook is called after the command has finished executing
#         (after self.func()).
#         """
#         pass
#
#     def parse(self):
#         """
#         This method is called by the cmdhandler once the command name
#         has been identified. It creates a new set of member variables
#         that can be later accessed from self.func() (see below)
#
#         The following variables are available for our use when entering this
#         method (from the command definition, and assigned on the fly by the
#         cmdhandler):
#            self.key - the name of this command ('look')
#            self.aliases - the aliases of this cmd ('l')
#            self.permissions - permission string for this command
#            self.help_category - overall category of command
#
#            self.caller - the object calling this command
#            self.cmdstring - the actual command name used to call this
#                             (this allows you to know which alias was used,
#                              for example)
#            self.args - the raw input; everything following self.cmdstring.
#            self.cmdset - the cmdset from which this command was picked. Not
#                          often used (useful for commands like 'help' or to
#                          list all available commands etc)
#            self.obj - the object on which this command was defined. It is often
#                          the same as self.caller.
#
#         A MUX command has the following possible syntax:
#
#           name[ with several words][/switch[/switch..]] arg1[,arg2,...] [[=|,] arg[,..]]
#
#         The 'name[ with several words]' part is already dealt with by the
#         cmdhandler at this point, and stored in self.cmdname (we don't use
#         it here). The rest of the command is stored in self.args, which can
#         start with the switch indicator /.
#
#         This parser breaks self.args into its constituents and stores them in the
#         following variables:
#           self.switches = [list of /switches (without the /)]
#           self.raw = This is the raw argument input, including switches
#           self.args = This is re-defined to be everything *except* the switches
#           self.lhs = Everything to the left of = (lhs:'left-hand side'). If
#                      no = is found, this is identical to self.args.
#           self.rhs: Everything to the right of = (rhs:'right-hand side').
#                     If no '=' is found, this is None.
#           self.lhslist - [self.lhs split into a list by comma]
#           self.rhslist - [list of self.rhs split into a list by comma]
#           self.arglist = [list of space-separated args (stripped, including '=' if it exists)]
#
#           All args and list members are stripped of excess whitespace around the
#           strings, but case is preserved.
#         """
#         raw = self.args
#         args = raw.strip()
#
#         # split out switches
#         switches = []
#         if args and len(args) > 1 and args[0] == "/":
#             # we have a switch, or a set of switches. These end with a space.
#             switches = args[1:].split(None, 1)
#             if len(switches) > 1:
#                 switches, args = switches
#                 switches = switches.split('/')
#             else:
#                 args = ""
#                 switches = switches[0].split('/')
#         arglist = [arg.strip() for arg in args.split()]
#
#         # check for arg1, arg2, ... = argA, argB, ... constructs
#         lhs, rhs = args, None
#         lhslist, rhslist = [arg.strip() for arg in args.split(',')], []
#         if args and '=' in args:
#             lhs, rhs = [arg.strip() for arg in args.split('=', 1)]
#             lhslist = [arg.strip() for arg in lhs.split(',')]
#             rhslist = [arg.strip() for arg in rhs.split(',')]
#
#         # save to object properties:
#         self.raw = raw
#         self.switches = switches
#         self.args = args.strip()
#         self.arglist = arglist
#         self.lhs = lhs
#         self.lhslist = lhslist
#         self.rhs = rhs
#         self.rhslist = rhslist
#
#         # if the class has the account_caller property set on itself, we make
#         # sure that self.caller is always the account if possible. We also create
#         # a special property "character" for the puppeted object, if any. This
#         # is convenient for commands defined on the Account only.
#         if hasattr(self, "account_caller") and self.account_caller:
#             if utils.inherits_from(self.caller, "evennia.objects.objects.DefaultObject"):
#                 # caller is an Object/Character
#                 self.character = self.caller
#                 self.caller = self.caller.account
#             elif utils.inherits_from(self.caller, "evennia.accounts.accounts.DefaultAccount"):
#                 # caller was already an Account
#                 self.character = self.caller.get_puppet(self.session)
#             else:
#                 self.character = None
