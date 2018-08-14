"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia import DefaultRoom
from commands.library import header
from evennia.utils import evtable


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
        message.append(self.desc)
        message.append(header())
        return "\n".join(message)
