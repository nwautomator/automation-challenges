Log scraping
============

Goals: Use various tools to scrape the logs to find certain occurrences and statistics. 

# Procedure steps:
* How many times the URL "/production/file_metadata/modules/ssh/sshd_config" was fetched
    * Of those requests, how many times the return code from Apache was not 200
* The total number of times Apache returned any code other than 200
* The total number of times that any IP address sent a PUT request to a path under "/dev/report/"
    * A breakdown of how many times such requests were made by IP address


# Procedure detail:

#### Determine the number of times "/production/file_metadata/modules/ssh/sshd_config" was fetched

First, a little setup work was done to get the total output when grepping for this string

    ssh_instances=`grep "/production/file_metadata/modules/ssh/sshd_config" ../puppet_access_ssl.log`

This returned each string matching. Getting the count was as simple as piping the output to wc

    ssh_instance_count=`echo "$ssh_instances" | wc -l`
    echo Number of entries containing /production/file_metadata/modules/ssh/sshd_config:
    echo $ssh_instance_count

#### Determine the number of times "/production/file_metadata/modules/ssh/sshd_config" was fetched without code 200 being returned

This was a little trickier and uses awk for field matching and counting. The code returned is the ninth ($9) field.

    ssh_instance_not_200=`echo "$ssh_instances" | awk 'BEGIN {sum = 0;}{if($9 != "200") sum = sum + 1;} END{print sum;}'`
    echo Number of entries containing /production/file_metadata/modules/ssh/sshd_config not returning code 200:
    echo $ssh_instance_not_200

#### Determine the total number of times Apache returned any code other than 200

This is just an extension of the previous task, except matching against the whole file

    all_not_200=`cat ../puppet_access_ssl.log | awk 'BEGIN {sum = 0;}{if($9 != "200") sum = sum + 1;} END{print sum;}'`
    echo Number of entries not returning code 200:
    echo $all_not_200

#### Determine the total number of times that any IP address sent a PUT request to a path under "/dev/report/"

Again, a little set up work was done

    put_dev_report=`grep "PUT /dev/report/" ../puppet_access_ssl.log`

Then the count was made

    put_dev_report_count=`echo "$put_dev_report" | wc -l`
    echo Number of entries running a PUT request against /dev/report:
    echo $put_dev_report_count

#### Give a breakdown of how many times such requests were made by IP address

This pipes the output of the matches into an IP filter, sorts it, cuts it up, then counts the number of occurrences. The first column returned will be the count, the second column will be the matching IP.

    put_dev_report_stats=`echo "$put_dev_report" | grep -ohE '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' | sort | tr -d ' ' | uniq --count | sort -gk1`
    echo PUT request against /dev/report by IP report:
    echo "$put_dev_report_stats"
