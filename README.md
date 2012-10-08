## StackIRC

StackIRC is a small Python application that posts questions from Stack Exchange sites to IRC channels.

### Requirements

StackIRC currently depends on the following:

- [python-irclib](https://bitbucket.org/jaraco/irc) - you will need to retrieve the source, extract the files, and build the package with the following commands:

        wget http://pypi.python.org/packages/source/i/irc/irc-3.1.1.zip
        unzip irc-3.1.1.zip
        cd irc-3.1.1
        sudo python setup.py install

- [Stack.PY](https://launchpad.net/stackpy) - you will need to run the following commands to add my PPA and install the package:

        sudo apt-add-repository ppa:george-edison55/george-edison
        sudo apt-get update
        sudo apt-get install python-stackpy

### Setup

[TODO]
