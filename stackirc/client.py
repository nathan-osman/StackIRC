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
from twisted.internet.task import LoopingCall

from config import StackIRCConfig

class StackIRCClient(irc.IRCClient):
    
    def __init__(self):
        self.nickname = StackIRCConfig.nick
        self.password = None if StackIRCConfig.password == '' else StackIRCConfig.password
        self.last_request = int(time())
        self.site         = Site(StackIRCConfig.site)
    
    def signedOn(self):
        print 'Connection and sign-on succeeded.'
        for c in set([j for i in StackIRCConfig.tags.values() for j in i]):
            print 'Joining %s...' % c
            self.join(c)
        # Create the loop that calls 'refresh'.
        self.loop = LoopingCall(self.refresh)
        self.loop.start(StackIRCConfig.interval, False)
    
    def refresh(self):
        try:
            questions = self.site.search.tagged(StackIRCConfig.tags.keys()) \
                .sort('creation').order('asc').fromdate(self.last_request) \
                .pagesize(2).filter('A9T75')
            sorted_questions = {}
            for q in questions:
                for t in q.tags:
                    if t in StackIRCConfig.tags:
                        if t in sorted_questions: sorted_questions[t].append(q)
                        else:                     sorted_questions[t] = [q,]
            for t in sorted_questions.keys():
                for q in sorted_questions[t]:
                    for c in StackIRCConfig.tags[t]:
                        self.msg(c, ('%s | http://%s/q/%s' % (
                            q.title,
                            StackIRCConfig.site,
                            q.question_id,
                        )).encode("utf-8"))
            # If any questions were returned, grab the timestamp of the latest item.
            if len(questions):
                self.last_request = questions[-1].creation_date_timestamp + 1
        except APIError, e:
            print 'API Error: %s' % e

