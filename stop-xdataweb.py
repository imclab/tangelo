#!/usr/bin/env python
import sys
import os
import signal

path = os.path.dirname(os.path.abspath(sys.argv[0]))
pidfile = path + "/xdataweb.pid"
if os.path.exists(pidfile):
    f = file(pidfile)
    pid = f.read()
    os.kill(int(pid), signal.SIGKILL)
    os.remove(pidfile)
