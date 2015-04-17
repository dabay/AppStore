# -*- coding: utf8 -*-
__author__ = 'Xiaohuan_Wang'

import subprocess
import signal
import sys


WORKER_USER = "nardev"
WORKER_IP = "172.16.88.15"


def pre_exec():
    """
    Ignore the SIGINT signal by setting the handler to the standard signal handler SIG_IGN.
    """
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def exec_cmd(cmd, *args):
    cmd_str = cmd + " " + " ".join(args)
    res = subprocess.Popen(
        cmd_str, shell=True, bufsize=2048,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=pre_exec
    )
    return res.communicate()[0]


def ssh_exec_cmd(cmd):
    """
    Put double -t is crucial to prevent various status messages popping up
    """
    ssh_command_prefix = str(
        "ssh {0}@{1} -t -t -i ~/.ssh/id_rsa "
    ).format(WORKER_USER, WORKER_IP)
    return exec_cmd(ssh_command_prefix, cmd)


if __name__ == '__main__':
    # ssh nardev@172.16.88.15 -t -t -i ~/.ssh/id_rsa ./AutoIt3.exe install_app.au3 598217338 0
    app_id = 598217338
    if len(sys.argv) > 1:
        app_id = sys.argv[1]
    autoit_cmd = "./AutoIt3.exe install_app.au3 %s 0" % app_id
    ssh_exec_cmd(autoit_cmd)
    print "done"
