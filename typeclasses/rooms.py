"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia import DefaultRoom
from commands.library import header
from evennia.utils import evtable
from clones import Clone


class Room(DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """
    def return_appearance(self, looker):
        message = []
        message.append(header(self.key))
        message.append(self.db.desc)
        message.append(header())

        chars = self.list_characters()
        objects = self.list_non_characters()
        colored_objects = []
        for obj in objects:
            colored_objects.append("|135%s|n" % obj.key)

        exits = []
        if self.exits:
            for exit in self.exits:
                if exit.access(looker, "view"):
                    exits.append("|w<|n|b%s|n|w>|n - %s" % (exit.key, exit.destination))

        table = evtable.EvTable("|wCharacters and Objects:|n", "|wExits:|n", table=[chars + colored_objects, exits],
                                border=None)
        table.reformat_column(0, width=39, align="l")
        message.append(table)
        message.append("\n")

        message2 = []
        for line in message:
            message2.append(unicode(line))

        return "\n".join(message2)

    def list_characters(self):
        return sorted([char for char in self.contents if char.is_typeclass(Clone, exact=False)])
