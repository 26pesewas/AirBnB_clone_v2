#!/usr/bin/python3
"""
This script (based on the file 1-pack_web_static.py) that
distributes an archive to your web servers, using the function do_deploy
"""


from fabric.api import local, env
from fabric.operations import env, put, run, sudo
import os.path
import shlex
env.hosts = ['3.236.44.83', '44.200.29.105']


def do_deploy(archive_path):
    """
    All remote commands must be executed on your both web servers
    (using env.hosts = ['<IP web-01>', 'IP web-02'] variable in your script)
    """
    if (os.path.isfile(archive_path) is False):
        return False

    try:
        nconfig = archive_path.split("/")[-1]
        ndir = ("/data/web_static/releases/" + nconfig.split(".")[0])
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(ndir))
        run("sudo tar -xzf /tmp/{} -C {}".format(nconfig, ndir))
        run("sudo rm /tmp/{}".format(nconfig))
        run("sudo mv {}/web_static/* {}/".format(ndir, ndir))
        run("sudo rm -rf {}/web_static".format(ndir))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(ndir))
        return True
    except:
        return False
