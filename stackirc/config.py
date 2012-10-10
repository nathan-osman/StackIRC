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
from stackpy import API

class MetaStackIRCConfig(type):
    
    # These are the defaults for the application.
    defaults = {
        # Server settings.
        'server':   'irc.freenode.net',
        'port':     6667,
        'nick':     'StackIRC',
        'password': '',
        # SE settings.
        'key':      '2ep05kX1Gb8HeHXKvo2Fyg((',
        'site':     'askubuntu.com',
        'tags':     { 'compiz': ['#compiz',] },
        # General settings.
        'interval': 120.0,
    }
    
    # This is the template created in the user's home directory when it does not
    # already exist. The user can then customize it.
    template = '''#=================================================================
# Please adjust the values below to customize your server.
#
# Some of the settings below are commented out (begin with a '#')
# and can be left at their defaults. Only uncomment them if you
# need to change the value.
#=================================================================

# The IRC server and port to connect to.

#server = '%(server)s'
#port   = %(port)s

# The nick for this bot. Feel free to leave it at the default so that other
# users know where the bot came from and that it means no harm :P Keep in mind
# that if another instance of the bot is already running on the server, another
# name will likely be substituted, such as 'StackIRC__' or something.

nick     = '%(nick)s'
password = '%(password)s'

# The API key used for making requests against the Stack Exchange API. This can
# safely be left at the default below unless you need custom statistics.

#key = '%(key)s'

# The Stack Exchange site you want to pull questions from. This needs to be the
# TLD for the site, such as 'stackapps.com' or 'apple.stackexchange.com'.

site = '%(site)s'

# A dictionary with tag names as keys and lists of channels as the values
# for those keys. So for example, if you had the following:
#
#   tags = { 'php': ['#room1', '#room2'] }
#
# then all questions asked with the 'php' tag will be posted to '#room1' and
# '#room2'. A room can be used for multiple tags. Fear not - StackIRC is smart
# enough to group API requests even if you have a lot of tags.

tags = %(tags)s

# The interval between successive requests to the API (in seconds). This value
# needs to be set at 60 or higher to avoid problems (and 120 is recommended).

#interval = %(interval).1f
''' % defaults

    def __init__(self, *args):
        super(MetaStackIRCConfig, self).__init__(*args)
        # The path to the user's stackirc directory and the filename of the config file.
        self.cpath = path.join(path.expanduser('~'), '.stackirc')
        self.cfile = path.join(self.cpath, 'config.py')
    
    def load(self):
        try:
            self.config = load_module('config', *find_module('config', [self.cpath,]))
            # Also set the API key.
            API.key = self.key
            return True
        except ImportError:
            return False
    
    def create(self):
        # Create the directory and configuration file.
        if not path.exists(self.cpath):
            mkdir(self.cpath)
        f = open(self.cfile, 'w')
        f.write(self.template)
    
    def __getattr__(self, key):
        try:
            return getattr(self.config, key)
        except AttributeError:
            return self.defaults[key]

class StackIRCConfig:
    
    # Enables dynamic attributes.
    __metaclass__ = MetaStackIRCConfig

