from evennia import default_cmds

class ChargenCommand(default_cmds.MuxCommand):
    """
    Begins the Chargen process.
    """

    key = "initiate"
    lock = "cmd:perm(Player)"