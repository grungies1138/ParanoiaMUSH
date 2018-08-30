from typeclasses.objects import Object
from evennia.utils import ansi

class Equipment(Object):
    def at_object_creation(self):
        self.db.cost = 0
        self.db.action_order = ()
        self.db.size = ""

    def return_appearance(self, looker):
        message = []
        message.append("|w_|n" * 78)
        name = ansi.ANSIString("|[002|w|u{}|n".format(self.key))
        message.append(name.ljust(78, '^').replace('^', "|[002|w_|n"))
        message.append("|wSize:|n {}".format(self.db.size))
        message.append("|wAction Order:|n {} +{}".format(self.db.action_order[0], self.db.action_order[1]))
        message.append(self.db.desc)
        message.append("|w_|n" * 78)

        message2 = []
        for line in message:
            message2.append(unicode(line))

        return "\n".join(message2)
