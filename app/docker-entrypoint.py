#!/usr/bin/python
import subprocess
import logging
import sys
import argparse
import signal
import libtmux
from libtmux.session import Session

log = None
tmuxSrv = libtmux.Server()

# STDOUT logging setup
def setupLogging():
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    sout = logging.StreamHandler(sys.stdout)
    sout.setLevel(logging.DEBUG)
    logformat = logging.Formatter('<*DOCKER*>[%(asctime)s][%(name)s][%(levelname)s]: %(message)s', "%m/%d/%Y %I:%M:%S %p")
    sout.setFormatter(logformat)
    log.addHandler(sout)
    return log

# Argparse setup
def setupArgParsing():
    parser = argparse.ArgumentParser(prog='docker-entrypoint.py')
    parser.add_argument('--start', dest='start', help='start minecraft server', action='store_true')
    parser.add_argument('--stop', dest='stop', help='stop minecraft server', action='store_true')
    parser.add_argument('--kill', dest='kill', help='kill minecraft server', action='store_true')
    parser.add_argument('-c', '--cmd', '--command', nargs='+', dest='command', help='run command in server')
    return parser

def onStop(sig, stack):
    log.info("!!!*** TESTING ON STOP RECV. EXITING() ***!!!")
    log.info("RECEIVED SIGNAL %i " % sig)
    log.info("RECIEVED STACK %s " % stack)
    subprocess.call("tmux kill-session -t book", shell=True)

def setupTraps():
    for sig in [ signal.SIGINT, signal.SIGTERM ]:
        try:
            signal.signal(sig, onStop)
            log.info("-- REGISTERED SIGNAL %s (%i)" % (sig.name, sig.value))
        except OSError as ex:
            log.error(ex)

log = setupLogging()
parser = setupArgParsing()
args = parser.parse_args()

log.info(args)

# Parse command line args
if (args.start):
    log.info("-- LAUNCHING MINECRAFT SERVER --")
    setupTraps()
    subprocess.call("sphinx-build -b html ./docs ./docs/_book", shell=True)
    subprocess.call("tmux new-session -d -s book", shell=True)
    #tmuxSrv.find_where({ "session_name": "book" }).attached_window().select_pane().send_keys("python3 docs.py"); # get_by_id("book") not returning valid session, try find_where
    subprocess.call("tmux send-keys -t book \"python3 docs.py\" C-m", shell=True)
    subprocess.call("./ServerStart.sh", shell=True)
elif (args.stop):
    log.info("-- STOPPING MINECRAFT SERVER --")
    exit()
elif (args.kill):
    log.info("-- KILLING MINECRAFT SERVER --")
    exit()
elif (args.cmd):
    log.info(args.cmd)