import sys
import os

from fabric.api import sudo, hosts, env, task, run, cd, roles
from fabric.decorators import runs_once
from fabric.operations import put
from fabric.contrib.files import exists, contains

from util import get_nodes, get_user, get_password

env.user = get_user()
env.password = get_password()
env.warn_only = True

nodes = get_nodes()

env.roledefs.update({
    'nodes': nodes
})

widget_file = "/home/andrew/work/applications/head/widget.rb"
template_file = "/home/andrew/work/applications/head/template.file"


@task
@roles('nodes')
def apt_install(pkg):
    apt_update()
    sudo("apt-get -q -y install %s" % pkg)


@task
@roles('nodes')
def apt_update():
    sudo("apt-get -q update")


@task
@roles('nodes')
def push_widget_file():
    # if the facter widget doesn't exist, create it
    if not exists("/usr/share/facterlib"):
        sudo("mkdir -p /usr/share/facterlib")
    with cd("/usr/share/facterlib"):
        put(widget_file, "widget.rb", use_sudo=True)


@task
@roles('nodes')
def test_widget_output():
    # testing the output
    widget_output = run("export FACTERLIB=/usr/share/facterlib:$FACTERLIB && facter -p widget")
    print "widget output: %s" % widget_output


@task
@roles('nodes')
def push_template_file():
    # push the template file to the node
    with cd("/etc"):
        put(template_file, "widgetfile", use_sudo=True)


@task
@roles('nodes')
def run_template_update():
    # get the output once again
    widget_output = run("export FACTERLIB=/usr/share/facterlib:$FACTERLIB && facter -p widget")
    # Run sed. sed always wins
    out = sudo("sed -ir 's/widget_type X/widget_type %s/' /etc/widgetfile" % widget_output)


@task
@roles('nodes')
def run_full():
    push_widget_file()
    push_template_file()
    run_template_update()
