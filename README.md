## StackIRC

StackIRC is a small Python application that posts questions from Stack Exchange sites to IRC channels.

### Installation

There are two sets of instructions for installing StackIRC - one for Ubuntu 12.04+ users and one for every other platform.

- **Ubuntu Users:**

  Open a terminal and run the following commands:
  
      sudo apt-add-repository ppa:george-edison55/george-edison
      sudo apt-get update
      sudo apt-get install python-stackirc

- **Other Platforms:**

  StackIRC depends on the following Python packages:

  - [python-twisted](http://twistedmatrix.com/trac/)
  - [Stack.PY](https://launchpad.net/stackpy) - you can download this from PyPI [here](http://pypi.python.org/pypi/stackpy)

  After installing the dependencies, you will need to download and extract the latest archive from [this page](https://github.com/nathan-osman/StackIRC/downloads). `cd` into the directory you extracted and run the following command:
  
        python setup.py install

  **Note:** on Unix platforms you will need to prefix the command with `sudo`.

I have tested StackIRC *only* on Python 2.7.

### Usage

The application can be started with the 'stackirc' command:

    stackirc

The first time this command is run, a configuration file will be generated and placed in your home directory (`~/.stackirc/config.py`). You will need to open the file and follow the instructions inside to continue setting up the application.

Once complete, you can run the `stackirc` command once again to start the server.
