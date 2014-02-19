#!/bin/bash

# get all ssh requests
ssh_instances=`grep "/production/file_metadata/modules/ssh/sshd_config" ../puppet_access_ssl.log`

# count them
ssh_instance_count=`echo "$ssh_instances" | wc -l`
echo Number of entries containing /production/file_metadata/modules/ssh/sshd_config:
echo $ssh_instance_count
echo

# use AWK to match not 200
ssh_instance_not_200=`echo "$ssh_instances" | awk 'BEGIN {sum = 0;}{if($9 != "200") sum = sum + 1;} END{print sum;}'`
echo Number of entries containing /production/file_metadata/modules/ssh/sshd_config not returning code 200:
echo $ssh_instance_not_200
echo

# use AWK to match not 200 from all log
all_not_200=`cat ../puppet_access_ssl.log | awk 'BEGIN {sum = 0;}{if($9 != "200") sum = sum + 1;} END{print sum;}'`
echo Number of entries not returning code 200:
echo $all_not_200
echo

# Get the total report list
put_dev_report=`grep "PUT /dev/report/" ../puppet_access_ssl.log`

# count them
put_dev_report_count=`echo "$put_dev_report" | wc -l`
echo Number of entries running a PUT request against /dev/report:
echo $put_dev_report_count
echo

# find the IPs, sort and display nicely
put_dev_report_stats=`echo "$put_dev_report" | grep -ohE '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' | sort | tr -d ' ' | uniq --count | sort -gk1`
echo PUT request against /dev/report by IP report: 
echo "$put_dev_report_stats"
