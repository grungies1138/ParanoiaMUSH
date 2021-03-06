import datetime
import evennia
from evennia import DefaultScript, create_message, create_script, default_cmds, GLOBAL_SCRIPTS, search_tag
from evennia.utils.utils import lazy_property, crop
from evennia.utils import evtable
from evennia.comms.models import Msg


HELP_CATEGORY = "BBS"
PREFIX = "|[002|wBBS:|n"
_HEAD_CHAR = "|015-|n"
_SUB_HEAD_CHAR = "-"
_WIDTH = 80

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
        self.interval = 60 * 60 * 24
        self.persistent = True
        self.start_delay = True

    def at_repeat(self):
        today = datetime.datetime.now()
        if self.db.timeout > 0:
            for post in self.get_all_posts():
                delta = today - post.date_created
                if delta.days > self.db.timeout:
                    post.delete()

    def get_all_posts(self):
        return list(evennia.Msg.objects.get_by_tag(category=self.key))

    def get_post(self, post_id):
        post = evennia.Msg.objects.get_by_tag(post_id, category=self.key)
        if post:
            return post[0]
        else:
            return None


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

            table = evtable.EvTable("#", "Name", "Last Post", "Posts", "U", border="header", table=None,
                                    header_line_char=_SUB_HEAD_CHAR, width=_WIDTH)
            for board in boards:
                last = None
                unread = board.get_all_posts()
                if len(board.get_all_posts()) > 0:
                    last = board.get_all_posts()[-1].date_created
                    last = last.strftime("%m/%d/%Y")
                    unread = [unread.remove(p) for p in unread if p.id in self.caller.db.read.get(board.key)]
                table.add_row(board.db.board_id, board.key, last, len(board.get_all_posts()), len(unread))

            table.reformat_column(0, width=5)
            table.reformat_column(1, width=30)
            table.reformat_column(2, width=25)
            table.reformat_column(3, width=8, align="r")
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
            board_read = self.caller.db.read.get(board.key)
            if post.id not in board_read:
                self.caller.db.read.get(board.key).append(post.id)
        else:
            boards = self.get_subscribed_boards(self.caller)
            temp_board = [b for b in boards if b.db.board_id == int(self.args)]
            if not temp_board:
                self.caller.msg("{} That board does not exist.  See |w+bbread|n to see the list of "
                                "available boards.".format(PREFIX))
                return
            board = temp_board[0]
            self.caller.msg("{}".format(board.key))
            self.caller.msg("=" * _WIDTH)
            message = []
            table = evtable.EvTable("#", "", "Title", "Date Posted", "Posted By", border="header", table=None,
                                    header_line_char=_SUB_HEAD_CHAR, width=_WIDTH)
            for post in board.get_all_posts():
                read = "U" if post.id not in self.caller.db.read.get(board.key) else ""
                table.add_row(post.tags.all()[0], read, post.header, post.date_created.strftime("%m/%d/%Y"),
                              post.senders[0].key)

            table.reformat_column(0, width=5)
            table.reformat_column(1, width=6)
            table.reformat_column(2, width=31)
            table.reformat_column(3, width=25)
            table.reformat_column(4, width=13)

            message.append(table)
            message.append("-" * _WIDTH)
            self.caller.msg("\n".join(str(m) for m in message))

    def get_subscribed_boards(self, target):
        subs = self.caller.db.read.keys()
        boards = []
        for s in subs:
            # b = Board.objects.filter(db_key=s)
            b = [b for b in GLOBAL_SCRIPTS.boardHandler.boards() if b.key == s]
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
            self.caller.db.read.get(board.key).append(post.id)
            del self.caller.db.post
            self.caller.msg("{} {} posted to the {} board.".format(PREFIX, header, board.key))

        else:
            if "/" not in self.args:
                self.caller.msg("{} Invalid syntax.  Please try again.  See: |whelp +bbpost|n for help".format(PREFIX))
                return

            args = self.args.split("/")

            temp_board = [b for b in GLOBAL_SCRIPTS.boardHandler.boards() if b.db.board_id == int(args[0])]
            if not temp_board:
                self.caller.msg("{} That board does not exist.  See |w+bbread|n to see the list of "
                                "available boards.".format(PREFIX))
                return
            board = temp_board[0]

            if not board.access(self.caller, 'post'):
                self.caller.msg("{} You do not have permission to post to that board.  See |w+bbread|n to "
                                "see a list of available boards.".format(PREFIX))
                return
            my_board = [b for b in self.caller.db.read.keys() if board.key == b]
            if not my_board:
                self.caller.msg("{} You cannot post to a board you do not subscribe to.  Please see |whelp +bbjoin|n"
                                .format(PREFIX))
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
        b_id, p_id = self.args.split("/")
        board = [b for b in GLOBAL_SCRIPTS.boardHandler.boards() if b.db.board_id == b_id]
        if not board:
            self.caller.msg("{} That is not a valid board.  Please see |whelp +bblist|n to find a valid board."
                            .format(PREFIX))
            return
        post = Msg.objects.get_by_tag(p_id, category=b_id)
        if not post:
            self.caller.msg("{} Not a valid post number.  Please see |w+bbread <board#>|n to find the post you are "
                            "looking for.".format(PREFIX))
            return
        # board[0].db.posts.db.posts.remove(post)
        post.delete()
        self.caller.msg("{} Post removed.".format(PREFIX))


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
        boards = GLOBAL_SCRIPTS.boardHandler.boards()
        for b in boards:
            if not b.access(self.caller, 'read'):
                boards.remove(b)

        board = [b for b in boards if b.db.board_id == int(self.args)]
        if not board:
            self.caller.msg("{} Either that board does not exist or you are not authorized to see it.  See |whelp "
                            "+bblist|n for more info.".format(PREFIX))
            return
        board = board[0]
        if not self.caller.db.read:
            self.caller.db.read = {}
        self.caller.db.read[board.key] = []
        board.db.subscribers.append(self.caller)
        self.caller.msg("{} {} joined.".format(PREFIX, board.key))


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
        board = [b for b in GLOBAL_SCRIPTS.boardHandler.boards() if b.db.board_id == int(self.args)]
        if not board:
            self.caller.msg("{} Not a valid board.".format(PREFIX))
            return
        my_board = [b for b in self.caller.db.read.keys() if b == board[0].key]
        if not my_board:
            self.caller.msg("{} You are not a subscriber of that board.  Please see |w+bbread|n to see your "
                            "subscribed boards.".format(PREFIX))
            return
        del self.caller.db.read[board[0].key]
        board[0].db.subscribers.remove(self.caller)
        self.caller.msg("{} Unsubscribed from {}".format(PREFIX, board[0].key))


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
        boards = GLOBAL_SCRIPTS.boardHandler.boards()
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
        for board in GLOBAL_SCRIPTS.boardHandler.boards():
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
        board = [b for b in GLOBAL_SCRIPTS.boardHandler.boards() if b.db.board_id == int(self.lhs)]
        if not board:
            self.caller.msg("{} Board not found.  Please see |w+bblist|n to find the correct board number."
                            .format(PREFIX))
            return
        board = board[0]
        board.locks.clear()
        board.locks.add(self.rhs)
        self.caller.msg("{} Locks set on {}".format(PREFIX, board.key))


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
        board = [b for b in GLOBAL_SCRIPTS.boardHandler.boards() if b.db.board_id == int(self.lhs)]
        if not board:
            self.caller.msg("{} Not a valid board.  Please see |w+bblist|n for the complete board list.".format(PREFIX))
            return
        board = board[0]
        if not isinstance(int(self.rhs), int):
            self.caller.msg("{} Invalid timeout value.  Please use numbers only.".format(PREFIX))
            return
        board.db.timeout = int(self.rhs)
        self.caller.msg("{} Timeout for board {} set to {}.".format(PREFIX, board.key, self.rhs))


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
