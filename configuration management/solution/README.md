Configuration management
========================

Goals: deploy the file 'template.file' to each node, then replace the value of the line 'widget_type X' with the output from the command 'facter -p widget'. 

# Procedure steps:
* Create the nodes for testing
* Create a test widget for facter to output arbitrary data
* Deploy the files to the nodes
* Replace the value
* Test each machine and display report



# Procedure detail:

## Create the nodes for testing

Using vagrant, run the commands:

    $ vagrant init
    $ vagrant up

This was done for five virtual machines.

**Create a test widget for facter to output arbitrary data**

The following snippet was used as the widget:

    Facter.add("widget") do
        setcode do
            "\"widget output\""
        end
    end

## Deploy the file to the nodes

Fabric will be used to deploy both the template.file to /etc, and the widget.rb file to /use/share/facterlib. One thing to note is that the FACTERLIB environment variable must be updated in
order to reference the new location.

    $ fab push_widget_file
    $ fab push_template_file

## Replace the value

Fabric will also be used to run remote commands to replace the value.

    $ fab run_template_update

For convenience, each of the fabric tasks (pushing files, running updates) has been consolidated into one fabric task:

    $ fab run_full

## Test each machine and display the report

A custom tool will be used to SSH into each machine and verify that the value has been replaced. This tool, too, is a Python script. This tool is separate from the primary deployment
mechanism because fabric does not provide summation out of the box. It can be done, but the Task class must be extended.

    $ python report.py



# Steps to test and verify:

* Create five VMs with IPs in the range 192.168,99.100-104 and start them. I used Ubuntu 12.04 images.
* Create a python virtual environment (I used virtualenvwrapper), and install the packages according to the requirements file

    $ mkvirtualenv test && cd test
    $ pip install -r requirements.txt

* Run the fabric command

    $ fab run_full

* Run the report

    $ python report.py

* The output will look like:

    Success: 5
    Failures: 0
