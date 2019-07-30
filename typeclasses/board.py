import datetime
from typeclasses.objects import Object
from evennia import DefaultScript, create_message, create_object
from evennia.utils.utils import lazy_property
from evennia import default_cmds
from evennia.comms.models import Msg
from evennia.utils import evtable


HELP_CATEGORY = "BBS"
STORAGE_OBJECT = "BBStorage"
_HEAD_CHAR = "|015-|n"
_SUB_HEAD_CHAR = "-"
_WIDTH = 78


class Board(Object):
    def at_object_creation(self):
        self.scripts.add('typeclasses.board.PostHandler', key='posts')

        # Messages are deleted in this number of days.  Or 0 for no timeout.
        self.db.timeout = 0
        self.db.subscribers = []
        self.locks.add("read:perm(Player);post:perm(Player)")

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
        self.start_delay = True
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


class BBReadCmd(default_cmds.MuxCommand):
    """
    This command enables the user to read boards as a whole as well as browsing its Posts and viewing posts
    individually.

    Usage:
        |w+bbread|n - lists all available boards that you are authorized to view.
        |w+bbread <#>|n - displays all the posts in the selected board.
        |w+bbread <#>/<#>|n - displays a specific post on the selected board.

    """

    key = "+bbread"
    locks = "cmd:perm(Player)"
    help_category = HELP_CATEGORY

    def func(self):
        if not self.args:
            boards = list(Board.objects.all())
            for b in boards:
                if not b.access(self.caller, 'read'):
                    boards.remove(b)
            self.caller.msg("Available Bulletin Boards:")
            table = evtable.EvTable("#", "Name", "Last Post", "Posts", "U", border="header", table=None,
                                    header_line_char=_SUB_HEAD_CHAR, width=_WIDTH)
            index = 1
            for board in boards:
                last = None
                if len(board.posts.db.posts) > 0:
                    last = board.posts.db.posts[-1].date_sent
                table.add_row(index, board.key, last, len(board.posts.db.posts), 1)

            table.reformat_column(0, width=3)
            table.reformat_column(1, width=34)
            table.reformat_column(2, width=25)
            table.reformat_column(3, width=4)
            table.reformat_column(4, width=12)

            message2 = []
            message2.append(table)

            self.caller.msg("\n".join(str(m) for m in message2))


class BBPostCmd(default_cmds.MuxCommand):
    """
    This command begins writing a post to the specified board.

    Usage:
        |w+bbpost <#>/<title>|n - Start a post on board <#> with the title of <title>.

    """
    key = "+bbpost"
    locks = "cmd:perm(Player)"
    help_category = HELP_CATEGORY

    def func(self):
        pass


class BBCmd(default_cmds.MuxCommand):
    """
    Once a post is started, this command allows the user to add content to the post.

    Usage:
        |w+bb <text>|n - Add content to a currently started post.
    """

    key = "+bb"
    locks = "cmd:perm(Player)"
    help_category = HELP_CATEGORY

    def func(self):
        pass


class BBProofCmd(default_cmds.MuxCommand):
    """
    Command to review a post being actively composed.

    Usage:
        |w+bbproof|n - review active post
    """

    key = "+bbproof"
    locks = "cmd:perm(Player)"
    help_category = HELP_CATEGORY

    def func(self):
        pass


class BBRemoveCmd(default_cmds.MuxCommand):
    """
    Removes a post written by you.  Admins are allowed to remove any post.

    Usage:
        |w+bbremove <#>/<#>|n - removes a post
    """

    key = "+bbremove"
    locks = "cmd:perm(Player)"
    help_category = HELP_CATEGORY

    def func(self):
        pass


class BBJoinCmd(default_cmds.MuxCommand):
    """
    Join the specified board, is allowed.

    Usage:
        |w+bbjoin <#>|n - joins board <#>

    See: |whelp +bbread|n to see a list of available boards.
    """

    key = "+bbjoin"
    locks = "cmd:perm(Player)"
    help_category = HELP_CATEGORY

    def func(self):
        pass


class BBLeaveCmd(default_cmds.MuxCommand):
    """
    This command allows the user to leave a board that they are currently subscribed to.

    Usage:
        |w+bbleave <#>|n - leaves board <#>
    """

    key = "+bbleave"
    locks = "cmd:perm(Player)"
    help_category = HELP_CATEGORY

    def func(self):
        pass


class BBCreateCmd(default_cmds.MuxCommand):
    """
    Admin only command that creates a new bulletin board

    Usage:
        |w+bbcreate <name>|n - create a new board named <name>
    """

    key = "+bbcreate"
    locks = "cmd:perm(Admin)"
    help_category = HELP_CATEGORY

    def func(self):
        name = self.args
        ex_board = Board.objects.filter(db_key=name)
        if ex_board:
            self.caller.msg("|gSYSTEM:|n A board with that name already exists.  Please try another.")
            return
        new_board = create_object("typeclasses.board.Board", key=name)

        storage = self.caller.search(STORAGE_OBJECT)
        new_board.move_to(storage)
        self.caller.msg("|gSYSTEM:|n Bulletin Board {} created.".format(name))


class BBDeleteCmd(default_cmds.MuxCommand):
    """
    Deletes a board and all of its posts.

    Usage:
        |w+bbdelete <#>|n - deletes board <#>
    """

    key = "+bbdelete"
    locks = "cmd:perm(Admin)"
    help_category = HELP_CATEGORY

    def func(self):
        pass


class BBLockCmd(default_cmds.MuxCommand):
    """
    Defines the locks for a specific board.

    |rBE ADVISED|n this will remove existing locks as replace them with what is defined in the command.
    Adjust accordingly.

    Usage:
        |w+bblock <#>=<lockstring>|n - redefines the locks for board <#>
    """

    key = "+bblock"
    locks = "cmd:perm(Admin)"
    help_category = HELP_CATEGORY

    def func(self):
        pass


class BBTimeoutCmd(default_cmds.MuxCommand):
    """
    Sets the timeout for a board.  Each post is deleted after the timeout has expired for that specific post.
    Default timeout is 0 which means no posts are deleted.

    Usage:
        |w+bbtimeout <#>=<timeout in days>|n - sets the timeout for the specified board.
    """

    key = "+bbtimeout"
    cmd = "cmd:perm(Admin)"
    help_category = HELP_CATEGORY

    def func(self):
        pass


class BBSCmdSet(default_cmds.CharacterCmdSet):
    key = "BBSCommands"
    priority = 2

    def at_cmdset_creation(self):
        self.add(BBReadCmd())
        self.add(BBPostCmd())
        self.add(BBCmd())
        self.add(BBProofCmd())
        self.add(BBRemoveCmd())
        self.add(BBTimeoutCmd())
        self.add(BBJoinCmd())
        self.add(BBLeaveCmd())
        self.add(BBCreateCmd())
        self.add(BBDeleteCmd())
        self.add(BBLockCmd())
