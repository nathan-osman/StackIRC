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
    site = 'stackoverflow.com'
    
    # The nick for this bot.
    nick = 'StackIRC'
    
    # A dictionary with tag names as keys and lists of channels as the values
    # for those keys.
    tags = {
        'php': ['#stackirc',],
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
            self.target()
            sleep(Config.interval)

class StackIRC(client.SimpleIRCClient):
    
    def __init__(self):
        client.SimpleIRCClient.__init__(self)
        self.last_request = int(time())
        self.site         = Site(Config.site)
        self.timer        = Timer(Config.interval, self.refresh)
    
    def on_welcome(self, c, e):
        for t in Config.tags.values():
            for c in t:
                print 'Joining channel %s...' % c
                self.connection.join(c)
        print 'Connections established!'
        self.timer.start()
    
    def refresh(self):
        try:
            cur_time = int(time())
            questions = self.site.search.tagged(Config.tags.keys()).sort('creation') \
                .fromdate(self.last_request).todate(cur_time)
            sorted_questions = {}
            for q in questions:
                for t in q.tags:
                    if t in Config.tags:
                        if t in sorted_questions: sorted_questions[t].append(q)
                        else:                     sorted_questions[t] = [q,]
            for t in sorted_questions.keys():
                for q in sorted_questions[t]:
                    for c in Config.tags[t]:
                        self.connection.privmsg(c, '%s | http://%s/q/%s' % (
                            q.title,
                            Config.site,
                            q.question_id,
                        ))
            self.last_request = cur_time + 1
        except APIError, e:
            print 'Error: %s' % e

if __name__ == '__main__':
    API.key = Config.key
    c = StackIRC()
    try:
        print 'Initiating connection to %s:%s...' % (
            Config.server,
            Config.port,
        )
        c.connect(Config.server,
                  Config.port,
                  Config.nick)
        c.start()
    except client.ServerConnectionError, e:
        print 'Error: %s' % e
    
