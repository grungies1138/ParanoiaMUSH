from typeclasses.objects import Object
from evennia import DefaultScript
from evennia.utils.utils import lazy_property
import datetime
from evennia.comms.models import Msg


class Board(Object):
    def at_object_creation(self):
        self.scripts.add('typeclasses.board.PostHandler', key='posts')

        # Messages are deleted in this number of days.  Or 0 for no timeout.
        self.db.timeout = 0

    @lazy_property
    def posts(self):
        return [s for s in self.scripts.get(key='posts') if s.is_valid()][0]

    def add_post(self, title, message, sender):
        pass

    def delete_post(self, post):
        pass


class PostHandler(DefaultScript):
    def at_script_creation(self):
        self.db.posts = []
        self.interval = 60 * 60 * 24
        self.start_delay = 60 * 60 * 24
        self.persistent = True
        self.key = "{}_script".format(self.obj.key)

    def at_repeat(self):
        today = datetime.datetime.now()
        if self.db.timeout > 0:
            for post in self.db.posts:
                delta = today - post.date_sent
                if delta.days > self.db.timeout:
                    self.db.posts.remove(post)
                    post.delete()
