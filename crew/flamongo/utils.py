import os
import sys


def dup2(f1, f2):
    try:
        os.dup2(f1, f2)
    except:
        pass


def daemonize():
    """Daemonizes the calling process."""
    first_child_pid = os.fork()
    if first_child_pid == 0:
        # inside the first child
        second_child_pid = os.fork()
        # become session leader
        os.setsid()
        if second_child_pid > 0:
            # inside the first child
            os._exit(os.EX_OK)
        elif second_child_pid < 0:
            # inside the first child with error
            os._exit(os.EX_OSERR)
        # inside the second child
        # set umask to have no permissions
        os.umask(0)
        # change to the root directory so the directory doesn't lock
        os.chdir('/')
        # open devnull
        fd = os.open(os.devnull, os.O_RDWR)
        # redirect stdout and stderr to devnull
        dup2(fd, sys.stdin.fileno())
        dup2(fd, sys.stdout.fileno())
        dup2(fd, sys.stderr.fileno())
    elif first_child_pid > 0:
        # inside the parent
        os._exit(os.EX_OK)
    else:
        # inside the parent with error
        os._exit(os.EX_OSERR)
