import datetime
from typeclasses.objects import Object
from evennia import DefaultScript, create_message, create_script
from evennia.utils.utils import lazy_property, crop
from evennia import default_cmds
from evennia.utils import evtable
from evennia.comms.models import Msg
from evennia import GLOBAL_SCRIPTS


HELP_CATEGORY = "BBS"
PREFIX = "|[002|wBBS:|n"
_HEAD_CHAR = "|015-|n"
_SUB_HEAD_CHAR = "-"
_WIDTH = 78

# To initialize the BBS system, enter the following command:
# @py from evennia import GLOBAL_SCRIPTS; GLOBAL_SCRIPTS.update("boardHandler": {"typeclass": "typeclasses.board.BoardHandler"})


class BoardHandler(DefaultScript):
    def at_script_creation(self):
        self.db.last_board = 0
        self.key = "BoardHandler"
        self.persistent = True
        self.db.boards = []

    def boards(self):
        return self.db.boards


class Board(DefaultScript):
    def at_script_creation(self):
        # Messages are deleted in this number of days.  Or 0 for no timeout.
        self.db.timeout = 0
        self.db.subscribers = []
        self.locks.add("read:perm(Player);post:perm(Player)")
        self.db.last_post = 0
        self.db.board_id = 0
        self.db.posts = create_script("typeclasses.board.PostHandler", key="{}_posts".format(self.key))

    def posts(self):
        return self.db.posts

    def add_post(self, title, message, sender):
        post = create_message(sender, message, receivers=self, header=title)
        post.tags.add("post")
        post.tags.add(self.key, category="board")
        self.posts.add(post)

    def delete_post(self, post):
        self.posts.delete(post)

    def get_posts(self):
        return self.posts.db.posts

    def get_unread(self, caller):
        pass


class PostHandler(DefaultScript):
    def at_script_creation(self):
        self.db.posts = []
        self.interval = 60 * 60 * 24
        self.start_delay = True
        self.persistent = True

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
            sub.msg("{} {} added to the {} board.".format(PREFIX, post.header, self.obj.key))

    def remove(self, post):
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
            boards = self.get_subscribed_boards(self.caller)

            for b in boards:
                if not b.access(self.caller, 'read'):
                    boards.remove(b)
            table = evtable.EvTable("#", "Name", "Last Post", "Posts", "U", border="header", table=None,
                                    header_line_char=_SUB_HEAD_CHAR, width=_WIDTH)
            for board in boards:
                last = None
                if len(board.db.posts.db.posts) > 0:
                    last = board.db.posts.db.posts[-1].date_created
                    last = last.strftime("%m/%d/%Y")
                table.add_row(board.db.board_id, board.key, last, len(board.get_posts()), 1)

            table.reformat_column(0, width=5)
            table.reformat_column(1, width=30)
            table.reformat_column(2, width=25)
            table.reformat_column(3, width=6, align="r")
            table.reformat_column(4, width=12, align="r")

            message2 = []
            message2.append(table)
            message2.append("-" * _WIDTH)
            message2.append("\n")

            self.caller.msg("\n".join(str(m) for m in message2))
        elif "/" in self.args:
            args = self.args.split("/")
            boards = self.get_subscribed_boards(self.caller)
            temp_board = [b for b in boards if b.db.board_id == int(args[0])]
            if not temp_board:
                self.caller.msg("{} That board does not exist.  See |w+bbread|n to see the list of "
                                "available boards.".format(PREFIX))
                return
            board = temp_board[0]
            temp_post = Msg.objects.get_by_tag(args[1], category=board.key)
            if not temp_post:
                self.caller.msg("{} that post does not exist.  See |w+bbread {}|n to find a valid post."
                                .format(PREFIX, board.db.board_id))
                return
            post = temp_post[0]
            self.caller.msg("=" * _WIDTH)
            self.caller.msg(post.header)
            self.caller.msg("Posted on: {}".format(post.date_created.strftime("%m/%d/%Y %r")))
            self.caller.msg("Posted By: {}".format(post.senders[0].key))
            self.caller.msg("-" * _WIDTH)
            self.caller.msg(post.message)
            self.caller.msg("-" * _WIDTH)
        else:
            boards = self.get_subscribed_boards(self.caller)
            temp_board = [b for b in boards if b.db.board_id == int(self.args)]
            if not temp_board:
                self.caller.msg("{} That board does not exist.  See |w+bbread|n to see the list of "
                                "available boards.".format(PREFIX))
                return
            board = temp_board[0]
            self.caller.msg("{} Posts".format(board.key))
            message = []
            table = evtable.EvTable("#", "Read", "Title", "Date Posted", "Posted By", border="header", table=None,
                                    header_line_char=_SUB_HEAD_CHAR, width=_WIDTH)
            for post in board.get_posts():
                read = "U" if post not in self.caller.db.read.get(board.key) else ""
                table.add_row(post.tags.all()[0], read, post.header, post.date_created.strftime("%m/%d/%Y"),
                              post.senders[0].key)

            table.reformat_column(0, width=5)
            table.reformat_column(1, width=6)
            table.reformat_column(2, width=31)
            table.reformat_column(3, width=25)
            table.reformat_column(4, width=11)

            message.append(table)
            message.append("-" * _WIDTH)
            self.caller.msg("\n".join(str(m) for m in message))

    def get_subscribed_boards(self, target):
        subs = self.caller.db.read.keys()
        boards = []
        for s in subs:
            b = Board.objects.filter(db_key=s)
            if b:
                boards.append(b[0])
        return boards


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
                self.caller.msg("{} You have not started a post yet.  See |whelp +bbpost|n for more info."
                                .format(PREFIX))
                return
            temp_post = self.caller.db.post
            message = temp_post.get("message")
            board = temp_post.get("board")
            header = temp_post.get("title")
            post = create_message(self.caller, message, receivers=board, header=header)
            post_id = board.db.last_post + 1
            post.tags.add(str(post_id), category=board.key)
            board.db.last_post = post_id
            board.posts.add(post)
            del self.caller.db.post
            self.caller.msg("{} {} posted to the {} board.".format(PREFIX, header, board.key))

        else:
            if "/" not in self.args:
                self.caller.msg("{} Invalid syntax.  Please try again.  See: |whelp +bbpost|n for help".format(PREFIX))
                return

            args = self.args.split("/")

            temp_board = [b for b in Board.objects.all() if b.db.board_id == int(args[0])]
            if not temp_board:
                self.caller.msg("{} That board does not exist.  See |w+bbread|n to see the list of "
                                "available boards.".format(PREFIX))
                return
            board = temp_board[0]

            # board = Board.objects.filter(id=int(args[0]))[0]
            if not board.access(self.caller, 'post'):
                self.caller.msg("{} You do not have permission to post to that board.  See |w+bbread|n to "
                                "see a list of available boards.".format(PREFIX))
                return
            title = args[1]
            if len(args[1]) > 60:
                title = crop(title, width=60)
            self.caller.db.post = {"title": title, "board": board}
            self.caller.msg("{} Post started.  type |w+bbwrite <text>|n to add the post content.".format(PREFIX))


class BBWriteCmd(default_cmds.MuxCommand):
    """
    Once a post is started, this command allows the user to add content to the post.  To append an new
    paragraph, just use this command a second time.  Each use will add a new line between each addition.

    Usage:
        |w+bbwrite <text>|n - Add content to a currently started post.


    See |wcolor ansi|n for carriage returns, tabs and other special characters.
    """

    key = "+bbwrite"
    locks = "cmd:perm(Player)"
    help_category = HELP_CATEGORY

    def func(self):
        post = self.caller.db.post
        message = post.get("message")
        if not post:
            self.caller.msg("{} No BBS Post started.  See |whelp +bbpost|n for more info.".format(PREFIX))
            return
        if message:
            post["message"] = "{}\n{}".format(message, self.args)
        else:
            post["message"] = "{}".format(self.args)
        self.caller.msg("{} Post updated.  |w+bbproof|n to proof read your post.".format(PREFIX))


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
        post = self.caller.db.post
        if not post:
            self.caller.msg("{} There is no post started.  See |whelp +bbpost|n for more info.".format(PREFIX))
            return

        self.caller.msg("Proofing: {}".format(post.get("title")))
        self.caller.msg("-" * _WIDTH)
        self.caller.msg("\n{}\n".format(post.get("message")))
        self.caller.msg("-" * _WIDTH)
        self.caller.msg("If you are done, type |w+bbpost|n to post this message to the board.\n")


class BBTossCmd(default_cmds.MuxCommand):
    """
    Clears out a post that is in the progress of being written but not yet posted.

    Usage:
        |w+bbtoss|n
    """

    key = "+bbtoss"
    locks = "cmd:perm(Player)"
    help_category = HELP_CATEGORY

    def func(self):
        post = self.caller.db.post
        if not post:
            self.caller.msg("{} There is no post to toss.  See |whelp +bbpost|n for more info.".format(PREFIX))
            return
        del self.caller.db.post
        self.caller.msg("{} Post terminated.".format(PREFIX))


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
        if not self.args:
            self.caller.msg("{} No board listed.  See |whelp +bbjoin| and |whelp +bblist|n for more info."
                            .format(PREFIX))
            return
        # boards = list(Board.objects.all())
        boards = GLOBAL_SCRIPTS.boardHandler.db.boards
        for b in boards:
            if not b.access(self.caller, 'read'):
                boards.remove(b)

        board = [b for b in boards if b.db.board_id == int(self.args)]
        if not board:
            self.caller.msg("{} Either that board does not exist or you are not authorized to see it.  See |whelp "
                            "+bblist|n for more info.".format(PREFIX))
            return
        self.caller.db.read[board[0].key] = []
        self.caller.msg("{} {} joined.".format(PREFIX, board[0].key))


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


class BBListCmd(default_cmds.MuxCommand):
    """
    Shows the list of available Board to join.

    Usage:
        |w+bblist|n
    """

    key = "+bblist"
    locks = "cmd:perm(Player)"
    help_category = HELP_CATEGORY

    def func(self):
        # boards = list(Board.objects.all())
        boards = GLOBAL_SCRIPTS.boardHandler.db.boards
        if not boards:
            self.caller.msg("{} There are no boards to display.  Please see |whelp +bbcreate|n.".format(PREFIX))
            return
        self.caller.msg("Available Boards:")
        for b in boards:
            if b.access(self.caller, 'read'):
                self.caller.msg(f"{b.db.board_id:<5}{b.key}")


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
        # ex_board = Board.objects.filter(db_key=name)
        ex_board = None
        for board in GLOBAL_SCRIPTS.boardHandler.db.boards:
            if board.key == name:
                ex_board = True

        if ex_board:
            self.caller.msg("{} A board with that name already exists.  Please try another.".format(PREFIX))
            return
        new_board = create_script("typeclasses.board.Board", key=name)

        # storage = self.caller.search(STORAGE_OBJECT)
        board_id = GLOBAL_SCRIPTS.boardHandler.db.last_board + 1
        new_board.db.board_id = board_id
        GLOBAL_SCRIPTS.boardHandler.db.last_board = board_id
        GLOBAL_SCRIPTS.boardHandler.db.boards.append(new_board)
        self.caller.msg("{} Bulletin Board {} created.".format(PREFIX, name))


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
        if not isinstance(int(self.args), int):
            self.caller.msg("{} Not a valid number.  Please enter a valid board ID.".format(PREFIX))
            return
        board = [b for b in GLOBAL_SCRIPTS.boardHandler.db.boards if b.db.board_id == int(self.args)]
        if not board:
            self.caller.msg("{} Invalid Board ID #.  Please enter a valid board ID.".format(PREFIX))
            return
        for post in board[0].db.posts.db.posts:
            post.delete()
        GLOBAL_SCRIPTS.boardHandler.db.boards.remove(board[0])
        self.caller.msg("{} Board removed.".format(PREFIX))


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
        self.add(BBWriteCmd())
        self.add(BBProofCmd())
        self.add(BBRemoveCmd())
        self.add(BBTimeoutCmd())
        self.add(BBJoinCmd())
        self.add(BBLeaveCmd())
        self.add(BBCreateCmd())
        self.add(BBDeleteCmd())
        self.add(BBLockCmd())
        self.add(BBTossCmd())
        self.add(BBListCmd())
