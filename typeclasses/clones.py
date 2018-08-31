from characters import Character
from commands.library import header
from world.static_data import EYES, HAIR, CLEARANCE, SKIN

class Clone(Character):
    def at_object_creation(self):
        super(Clone, self).at_object_creation()
        self.db.stats = {"violence": 0, "brains": 0, "chutzpah": 0, "mechanics": 0}
        self.db.skills = {"athletics": 0, "guns": 0, "melee": 0, "throw": 0,
                          "science": 0, "psychology": 0, "bureaucracy": 0, "alpha complex": 0,
                          "bluff": 0, "charm": 0, "intimidate": 0, "stealth": 0,
                          "operate": 0, "engineer": 0, "program": 0, "demolitions": 0}
        self.db.moxie = 0
        self.db.max_moxie = 6
        self.db.mutant_power = None
        self.db.action_cards = []
        self.db.duty = ""
        self.db.secret_societies = []
        self.db.hair = 0
        self.db.eyes = 0
        self.db.skin = 0
        self.db.height = ""
        self.db.weight = ""
        self.db.xp = 0
        self.db.sector = ""
        self.db.gender = ""
        self.db.personality = []
        self.db.clone = 0
        self.db.chargen_complete = 0
        self.cmdset.add("commands.default_cmdsets.SheetCmdSet", permanent=True)

    def return_appearance(self, looker):
        if not looker:
            return
        equipment = [eq for eq in self.contents if eq != looker and eq.access(looker, "view")]

        message = []
        message.append(header(self.key))
        message.append("{} has {} hair, {} eyes and {} skin.  They stand at {} height and weight {} pounds.  "
                       "They wear a jumpsuit with a {} stripe.".format(self.key, HAIR.get(self.db.hair) or "no",
                        EYES.get(self.db.eyes) or "nondescript", SKIN.get(self.db.skin) or "pale", self.db.height
                        or "indeterminate", self.db.weight or "indeterminate", CLEARANCE.get(self.db.clearance)))
        message.append(header())
        if equipment:
            message.append("Equipment:")
        for eq in equipment:
            message.append(eq.key)

        return "\n".join(message)