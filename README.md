## StackIRC

StackIRC is a small Python application that posts questions from Stack Exchange sites to IRC channels.

### Requirements

StackIRC currently depends on the following:

- [python-twisted](http://twistedmatrix.com/trac/) - you will need to run the following command in order to install the package:

        sudo apt-get install python-twisted

- [Stack.PY](https://launchpad.net/stackpy) - you will need to run the following commands to add my PPA and install the package:

        sudo apt-add-repository ppa:george-edison55/george-edison
        sudo apt-get update
        sudo apt-get install python-stackpy

I have tested StackIRC *only* on Python 2.7.

### Installation

In order to install Stack.PY you will need to unpack the archive you downloaded and open a terminal in the directory that was created. You can then run the following command to install the Python modules:

    sudo ./setup.py install

The application can be started with the 'stackirc' command:

    stackirc

The first time this command is run, a configuration file will be generated and placed in your home directory (`~/.stackirc/config.py`). You will need to open the file and follow the instructions inside to continue setting up the application.

Once complete, you can run the `stackirc` command once again to start the server.
