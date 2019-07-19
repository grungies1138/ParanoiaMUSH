from typeclasses.objects import Object
from evennia.utils import ansi

class Equipment(Object):
    def at_object_creation(self):
        self.db.cost = 0
        self.db.action_order = ()
        self.db.size = ""
        self.db.level = 0
        self.db.uses = -1
        self.db.consumable = False

    def return_appearance(self, looker):
        message = []
        message.append("|w_|n" * 78)
        name = ansi.ANSIString("|[002|w|u{}|n".format(self.key))
        message.append(name.ljust(78, '^').replace('^', "|[002|w_|n"))
        message.append("|wSize:|n {}".format(self.db.size))
        message.append("|wLevel:|n {}".format(self.db.level))
        if self.db.uses > -1:
            message.append("|wUses Remaining:|n {}".format(self.db.uses))
        message.append("|wConsumable:|n {}".format(self.db.consumable))
        message.append("|wAction Order:|n {} +{}".format(self.db.action_order[0], self.db.action_order[1]))
        message.append(self.db.desc)
        message.append("|w_|n" * 78)

        message2 = []
        for line in message:
            message2.append(line)

        return "\n".join(str(m) for m in message2)

    def __str__(self):
        return "Name: {} - Action Order: {}\nDesc: {}".format(self.key, self.db.action_order, self.db.desc)
