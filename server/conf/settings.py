"""
Evennia settings file.

The available options are found in the default settings file found
here:

/root/Test/evennia/evennia/settings_default.py

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

If you want to share your game dir, including its settings, you can
put secret game- or server-specific settings in secret_settings.py.

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *

######################################################################
# Evennia base server config
######################################################################

INLINEFUNC_ENABLED=True

# This is the name of your game. Make it catchy!
SERVERNAME = "Paranoia MUSH"

# Server ports. If enabled and marked as "visible", the port
# should be visible to the outside world on a production server.
# Note that there are many more options available beyond these.

# Telnet ports. Visible.
TELNET_ENABLED = True
TELNET_PORTS = [4000]
# (proxy, internal). Only proxy should be visible.
WEBSERVER_ENABLED = True
WEBSERVER_PORTS = [(4001, 4002)]
# Telnet+SSL ports, for supporting clients. Visible.
SSL_ENABLED = False
SSL_PORTS = [4003]
# SSH client ports. Requires crypto lib. Visible.
SSH_ENABLED = False
SSH_PORTS = [4004]
# Websocket-client port. Visible.
WEBSOCKET_CLIENT_ENABLED = True
WEBSOCKET_CLIENT_PORT = 4005
# Internal Server-Portal port. Not visible.
AMP_PORT = 4006

######################################################################
# Default Typeclasses
######################################################################

BASE_CHARACTER_TYPECLASS = "typeclasses.clones.Clone"
BASE_GUEST_TYPECLASS = "typeclasses.accounts.Guest"

######################################################################
# Guest Configuration
######################################################################
GUEST_ENABLED = True
GUEST_LIST = ["Clone1", "Clone2", "Clone3", "Clone4", "Clone5"]
PERMISSION_GUEST_DEFAULT = "Guest"

######################################################################
# Game Index Config
######################################################################

# GAME_INDEX_LISTING = {
#     'game_status': 'beta',
#     # Optional, comment out or remove if N/A
#     'game_website': 'http://paranoia.pennmush.org:4001',
#     'short_description': 'Based on the Table Top Roleplaying Game Paranoia.',
#     # Optional but highly recommended. Markdown is supported.
#     'long_description': ("Greetings Citizens, I am the Computer. I am your friend. Alpha Complex needs Troubleshooters. "
#                          "So it's time for me to incubate some new clones to help test some of my new systems. "
#                          "Please proceed to the Clone Assignment Request Department for your clone acquisition and "
#                          "assignment needs.Paranoia is a Comedy Horror Table Top game set in the far future where "
#                          "humans have been sequestered to an underground (maybe) base called Alpha Complex. It is "
#                          "run by the Computer. Humans are now all clones and are created to help troubleshoot "
#                          "issues that the Computer reports. Please come and help me beta test my new game!"
#     ),
#     'listing_contact': 'grungies1138@gmail.com',
#     # At minimum, specify this or the web_client_url options. Both is fine, too.
#     'telnet_hostname': 'paranoia.pennmush.org',
#     'telnet_port': 4000,
#     # At minimum, specify this or the telnet_* options. Both is fine, too.
#     'web_client_url': 'http://paranoia.pennmush.com:4001/webclient',
# }

######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
