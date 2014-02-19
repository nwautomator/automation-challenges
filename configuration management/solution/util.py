import paramiko
from paramiko.ssh_exception import SSHException


def get_user():
    """Returns the user
    """
    return 'vagrant'


def get_password():
    """Returns the password. This is certainly an insecure way of doing things: paramiko is capable of using key auth.
    """
    return 'vagrant'


def get_nodes():
    """Returns the nodes to be updated
    """
    return ['192.168.99.100', '192.168.99.101', '192.168.99.102', '192.168.99.103', '192.168.99.104']


def run_report():
    """Runs the report of successes and failures, using paramiko (SSH client)
    """
    success, fail = 0, 0
    nodes = get_nodes()
    print "Running tests..."
    for node in nodes:
        # log into each of the nodes
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(node, username=get_user(), password=get_password())
        try:
            stdin, stdout, stderr = client.exec_command('egrep -irl "widget output" /etc/widgetfile')
            lines = stdout.readlines()
            if len(lines) == 1:     # success
                line = lines[0]      # there will only be one line
                if "/etc/widgetfile" == line.strip():
                    success += 1
                    continue
                fail += 1
            else:
                fail += 1
        except SSHException, e:
            fail += 1
            print e.message

    print "Successes: %d" % success
    print "Failures: %d" % fail
