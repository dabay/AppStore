# -*- coding: utf8 -*-
__author__ = 'Xiaohuan_Wang'

import subprocess
import signal
import sys


WORKER_USER = "nardev"
WORKER_IP = "172.16.88.15"
IPA_REMOTE_FOLDER = "/cygdrive/c/Users/nardev/Music/iTunes/iTunes\ Media/Mobile\ Applications/"
IPA_LOCAL_FOLDER = "~/ipa/"


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


def scp_cmd(cmd):
    ssh_command_prefix = str("scp -i ~/.ssh/id_rsa ")
    print ssh_command_prefix + cmd
    return exec_cmd(ssh_command_prefix, cmd)


if __name__ == '__main__':
    scp_sub_cmd = '{}@{}:"{}*" {}'.format(WORKER_USER, WORKER_IP,IPA_REMOTE_FOLDER, IPA_LOCAL_FOLDER)
    scp_cmd(scp_sub_cmd)
    print "Done"