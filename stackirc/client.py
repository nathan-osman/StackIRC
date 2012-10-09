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

from calendar import timegm
from stackpy import API, APIError, Site
from time import time
from twisted.words.protocols import irc
from twisted.internet import protocol
from twisted.internet.task import LoopingCall

class StackIRCClient(irc.IRCClient):
    
    def __init__(self):
        self.last_request = int(time())
        self.site         = Site(self.config.site)
    
    def signedOn(self):
        print 'Connection and sign-on succeeded.'
        # Connect to the channels in the config file.
        for t in self.config.tags.values():
            for c in t:
                print 'Joining %s...' % c
                self.join(c)
        # Create the loop that calls 'refresh'.
        self.loop = LoopingCall(self.refresh)
        self.loop.start(self.config.interval, False)
    
    def refresh(self):
        try:
            to_time = int(time())
            questions = self.site.questions.tagged(self.config.tags.keys()).sort('creation') \
                .fromdate(self.last_request).todate(to_time)
            latest_time = 0
            sorted_questions = {}
            for q in questions:
                latest_time = max(latest_time, timegm(q.creation_date.utctimetuple()))
                for t in q.tags:
                    if t in self.config.tags:
                        if t in sorted_questions: sorted_questions[t].append(q)
                        else:                     sorted_questions[t] = [q,]
            for t in sorted_questions.keys():
                for q in sorted_questions[t]:
                    for c in self.config.tags[t]:
                        self.msg(c, '%s | http://%s/q/%s' % (
                            q.title,
                            self.config.site,
                            q.question_id,
                        ))
            # If any questions were returned, grab the latest timestamp on them.
            if len(questions):
                self.last_request = latest_time + 1
        except APIError, e:
            print 'API Error: %s' % e

class StackIRCFactory(protocol.ClientFactory):
    
    def buildProtocol(self, addr):
        return StackIRCClient()
