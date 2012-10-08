#!/usr/bin/env python
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

class Config:
    
    # The IRC server and port to connect to.
    server = 'irc.freenode.net'
    port   = 6667
    
    # The API key for requests and Stack Exchange site.
    key  = ''
    site = 'askubuntu'
    
    # The nick for this bot.
    nick = 'StackIRC'
    
    # A dictionary with tag names as keys and lists of channels as the values
    # for those keys.
    tags = {
        'stackirc': ['#stackirc',],
    }
    
    # The time to wait between refreshing information with the API (in seconds).
    # (I suggest avoiding numbers <60.)
    interval = 60.0

#=====================================
#        End of Configuration
#=====================================

from irc import client
from stackpy import API, APIError, Site
from threading import Thread
from time import sleep, time

class Timer(Thread):
    
    def __init__(self, interval, target):
        Thread.__init__(self)
        self.interval, self.target = interval, target
    
    def run(self):
        while True:
            sleep(Config.interval)
            self.target()

class StackIRC:
    
    def __init__(self):
        self.client       = client.IRC()
        self.connection   = None
        self.last_request = int(time())
        self.site         = Site(Config.site)
        self.timer        = Timer(Config.interval, self.refresh)
    
    def connect(self):
        try:
            print 'Initiating connection to %s:%s...' % (
                Config.server,
                Config.port,
            )
            self.connection = self.client.server().connect(Config.server,
                                                           Config.port,
                                                           Config.nick)
            for t in Config.tags.values():
                for c in t:
                    print 'Joining channel %s...' % c
                    self.connection.join(c)
            self.timer.start()
        except client.ServerConnectionError, e:
            print 'Error: %s' % e
        
        print 'Connections established!'
        self.client.process_forever()
    
    def refresh(self):
        
        # Sample demonstration.
        self.connection.privmsg('#stackirc', 'Hello world!')
        return
        
        try:
            cur_time = int(time())
            questions = self.site.questions.tagged(Config.tags) \
                .fromdate(self.last_request).todate(cur_time)
            for q in questions:
                print q
            self.last_request = cur_time + 1
        except APIError, e:
            print 'Error: %s' % e

if __name__ == '__main__':
    API.key = Config.key
    irc = StackIRC()
    irc.connect()
