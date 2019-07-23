from typeclasses.objects import Object
from evennia import DefaultScript
from evennia.utils.utils import lazy_property
from evennia.comms.models import Msg


class Board(Object):
    def at_object_creation(self):
        self.scripts.add('typeclasses.board.PostHandler', key='posts')

    @lazy_property
    def posts(self):
        return [s for s in self.scripts.get(key='posts') if s.is_valid()][0]


class PostHandler(DefaultScript):
    def at_script_creation(self):
        self.db.posts = []
