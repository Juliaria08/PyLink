import yaml
import sys
from collections import defaultdict

import world

global testconf
testconf = {'bot':
                {
                    'nick': 'PyLink',
                    'user': 'pylink',
                    'realname': 'PyLink Service Client',
                    # Suppress logging in the test output for the most part.
                    'loglevel': 'CRITICAL',
                    'serverdesc': 'PyLink unit tests'
                },
            'servers':
                # Wildcard defaultdict! This means that
                # any network name you try will work and return
                # this basic template:
                defaultdict(lambda: {
                        'ip': '0.0.0.0',
                        'port': 7000,
                        'recvpass': "abcd",
                        'sendpass': "chucknorris",
                        'protocol': "null",
                        'hostname': "pylink.unittest",
                        'sid': "9PY",
                        'channels': ["#pylink"],
                        'maxnicklen': 20,
                        'sidrange': '8##'
                    })
           }

def validateConf(conf):
    """Validates a parsed configuration dict."""
    assert type(conf) == dict, "Invalid configuration given: should be type dict, not %s." % type(conf).__name__
    for section in ('bot', 'servers', 'login'):
        assert conf.get(section), "Missing %r section in config." % section
    for netname, serverblock in conf['servers'].items():
        for section in ('ip', 'port', 'recvpass', 'sendpass', 'hostname',
                        'sid', 'sidrange', 'channels', 'protocol', 'maxnicklen'):
            assert serverblock.get(section), "Missing %r in server block for %r." % (section, netname)
        assert type(serverblock['channels']) == list, "'channels' option in " \
            "server block for %s must be a list, not %s." % (netname, type(serverblock['channels']).__name__)
    assert type(conf['login'].get('password')) == type(conf['login'].get('user')) == str and \
        conf['login']['password'] != "changeme", "You have not set the login details correctly!"
    return conf

def loadConf(fname):
    """Loads a PyLink configuration file from the filename given."""
    with open(fname, 'r') as f:
        try:
            conf = yaml.load(f)
        except Exception as e:
            print('ERROR: Failed to load config from %r: %s: %s' % (fname, type(e).__name__, e))
            sys.exit(4)
        return conf

if world.testing:
    conf = testconf
    confname = 'testconf'
else:
    try:
        # Get the config name from the command line, falling back to config.yml
        # if not given.
        fname = sys.argv[1]
        confname = fname.split('.', 1)[0]
    except IndexError:
        # confname is used for logging and PID writing, so that each
        # instance uses its own files. fname is the actual name of the file
        # we load.
        confname = 'pylink'
        fname = 'config.yml'
    conf = validateConf(loadConf(fname))
