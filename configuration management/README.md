Instructions
============

In this directory is a file, "template.file". This file needs to be distributed to N systems, with the following portion replaced with dynamic content based on the contents of the output of the command 'facter -p widget' on the given target system:

    # Replace this
    widget_type X
    # ... with this:
    # widget_type (output from facter -p widget)

In whatever language you like, as simply or as complicated as you like, write a solution that will:

* Across N number of linux systems (where N is a number from 0-positive infinity):
 * Place the template file on the system in /etc/widgetfile with the appropriate portions of the file replaced with the actual widget value
* Reports the number of systems from N that were successfully templated
* Reports the number of systems from N that failed to template

You can assume total control over the access model on the systems - e.g., if you want to place the file with direct SSH, that's fine. If you want the file to be retrieved from a HTTP or other service by a daemon running on each system, that's fine. Document/code that in your solution.

Provide full documentation and example usage for how you would deploy this solution.

If you do not have access to multiple systems or virtualization to test this solution (we recommend Vagrant and Virtualbox if you don't have access to anything else), we will accept an untested solution with good documentation that explains the methodology behind the tool. Your method and approach are more at issue here than your implementation.
