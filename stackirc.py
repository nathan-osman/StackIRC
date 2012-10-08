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

#=====================================
#  Configuration for the Application
#=====================================

class Config
    
    # The IRC server and port to connect to.
    server = 'irc.freenode.net'
    port   = 6667
    
    # A dictionary with tag names as keys and lists of channels as the values
    # for those keys.
    tags = {
        'compiz': ['compiz',],
    }
    
    # The time to wait between refreshing information with the API (in seconds).
    # (I suggest avoiding numbers <60.)
    interval = 60

#=====================================
#        End of Configuration
#=====================================

