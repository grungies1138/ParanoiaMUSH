import datetime
from typeclasses.objects import Object
from evennia import DefaultScript, create_message
from evennia.utils.utils import lazy_property
from evennia import default_cmds
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
        post = create_message(sender, message, receivers=self, header=title)
        post.tags.add("post")
        post.tags.add(self.key, category="board")
        self.posts.add(post)

    def delete_post(self, post):
        self.posts.delete(post)


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

    def add(self, post):
        self.db.posts.append(post)

    def delete(self, post):
        self.db.posts.remove(post)


class AddBoardCmd(default_cmds.MuxCommand):
    """
    Admin only command to create Bulletin Boards.

    Usage:
        |w+boards/create <name>|n
    """

    key = "+boards"
    locks = "cmd:perm(Admin)"
    help_category = "BBS"

    def func(self):
        if 'create' in self.switches:
            boards = Board.objects.all()
            self.caller.msg(", ".join(list(boards)))
        else:
            pass


class BBSCmdSet(default_cmds.CharacterCmdSet):
    key = "BBSCommands"
    priority = 2

    def at_cmdset_creation(self):
        self.add(AddBoardCmd())
