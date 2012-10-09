'''
Copyright (c) 2012 Nathan Osman

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from imp import find_module, load_module
from os import mkdir, path
from sys import exit
from twisted.internet import reactor

from client import StackIRCClient, StackIRCFactory

# This is the template created in the user's home directory when it does not
# already exist. The user can then customize it.
_template = '''#=========================================================
# Please adjust the values below to customize your server.
#=========================================================

# The IRC server and port to connect to.
server = 'irc.freenode.net'
port   = 6667

# The API key used for making requests against the Stack Exchange API. Note that
# although this is not _technically_ required, it is recommended. You will
# quickly run out of requests if you leave this blank.
key = ''

# The Stack Exchange site you want to pull questions from. This needs to be the
# TLD for the site, such as 'stackapps.com' or 'apple.stackexchange.com'.
site = 'askubuntu.com'

# The nick for this bot. Feel free to leave it at the default so that other
# users know where the bot came from and that it means no harm :P
nick = 'StackIRC'

# A dictionary with tag names as keys and lists of channels as the values
# for those keys. So for example, if you had the following:
#
#   tags = { 'php': ['#room1', '#room2'] }
#
# then all questions asked with the 'php' tag will be posted to '#room1' and
# '#room2'. A room can be used for multiple tags. Fear not - StackIRC is smart
# enough to group API requests even if you have a lot of tags.
tags = {
    'compiz': ['#compiz',],
}

# The interval between successive requests to the API (in seconds). This value
# needs to be set at 60 or higher to avoid problems (and 120 is recommended).
interval = 120.0
'''

class StackIRCBot:
    
    def __init__(self):
        # Determine if the user's settings file exists.
        p = path.join(path.expanduser('~'), '.stackirc')
        s = path.join(p, 'config.py')
        try:
            self.config = load_module('config', *find_module('config', [p,]))
        except ImportError, e:
            global _template
            print 'The file "%s" does not exist. StackIRC will now create the file and exit. Please open the file in a text editor, adjust the configuration values, and start StackIRC again.' % s
            # Create the directory and configuration file.
            if not path.exists(p):
                mkdir(p)
            f = open(s, 'w')
            f.write(_template)
            exit()
        # Provide the clients with access to the config values and create the factory.
        StackIRCClient.config   = self.config
        StackIRCClient.nickname = self.config.nick
        self.factory = StackIRCFactory()
    
    def run(self):
        print 'Connecting to %s:%s...' % (self.config.server, self.config.port,)
        reactor.connectTCP(self.config.server, self.config.port, self.factory)
        reactor.run()

