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
        for sub in self.obj.db.subscribers:
            sub.msg("|gSYSTEM:|n {} added to the {} board.".format(post.header, self.obj.key))

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
            table = evtable.EvTable("#", "Name", "Last Post", "Posts", "U", border="header", table=None,
                                    header_line_char=_SUB_HEAD_CHAR, width=_WIDTH)
            for board in boards:
                last = None
                if len(board.posts.db.posts) > 0:
                    last = board.posts.db.posts[-1].date_sent
                table.add_row(board.id, board.key, last, len(board.posts.db.posts), 1)

            table.reformat_column(0, width=5)
            table.reformat_column(1, width=30)
            table.reformat_column(2, width=25)
            table.reformat_column(3, width=8)
            table.reformat_column(4, width=10, align="r")

            message2 = []
            message2.append(table)
            message2.append("\n")

            self.caller.msg("\n".join(str(m) for m in message2))
        elif "/" in self.args:
            pass
        # else:
        #     board = list(Board.objects.all())[self.args]
        #     self.caller.msg("{} Posts".format(board.key))
        #     message = []
        #     table = evtable.EvTable("")


class BBPostCmd(default_cmds.MuxCommand):
    """
    This command begins writing a post to the specified board.

    The title will be limited to 60 characters.

    Usage:
        |w+bbpost <#>/<title>|n - Start a post on board <#> with the title of <title>.

        |w+bbpost|n - to complete a post and add it to the board.

    """
    key = "+bbpost"
    locks = "cmd:perm(Player)"
    help_category = HELP_CATEGORY

    def func(self):
        if not self.args:
            if not self.caller.db.post:
                self.caller.msg("|gSYSTEM:|n You have not started a post yet.  See |whelp +bbpost|n for more info.")
                return
            temp_post = self.caller.db.post
            message = temp_post.get("message")
            board = temp_post.get("board")
            header = temp_post.get("title")
            post = create_message(self.caller, message, receivers=board, header=header)
            board.posts.add(post)

        else:
            if "/" not in self.args:
                self.caller.msg("|gSYSTEM:|n Invalid syntax.  Please try again.  See: |whelp +bbpost|n for help")
                return

            args = self.args.split("/")

            board_ids = [b.id for b in list(Board.objects.all())]

            if not int(args[0]) in board_ids:
                self.caller.msg("|gSYSTEM:|n That is not a valid board ID.  Please try again.  See |whelp +bbread|n "
                                "for a list of the boards.")
                return

            board = Board.objects.filter(id=int(args[0]))[0]
            if not board.access(self.caller, 'post'):
                self.caller.msg("|gSYSTEM:|n You do not have permission to post to that board.  See |w+bbread|n to "
                                "see a list of available boards.")
                return

            self.caller.db.post = {"title": self.args[1], "board": board}
            self.caller.msg("|gSYSTEM:|n Post started.  type |w+bb <text>|n to add the post content.")


class BBCmd(default_cmds.MuxCommand):
    """
    Once a post is started, this command allows the user to add content to the post.  To append an new
    paragraph, just use this command a second time.  Each use will add a new line between each addition.

    Usage:
        |w+bb <text>|n - Add content to a currently started post.


    See |wcolor ansi|n for carriage returns, tabs and other special characters.
    """

    key = "+bb"
    locks = "cmd:perm(Player)"
    help_category = HELP_CATEGORY

    def func(self):
        post = self.caller.db.post
        message = post.get("message")
        if not post:
            self.caller.msg("|gSYSTEM:|n No BBS Post started.  See |whelp +bbpost|n for more info.")
            return
        post["message"] = "{}\n{}".format(message, self.args)
        self.caller.msg("|gSYSTEM:|n Post updated.  |w+bbproof|n to proof read your post.")


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
