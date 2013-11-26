#!/bin/bash

# Grab count of GET requests for sshd_config
sshd_count=$(grep "/production/file_metadata/modules/ssh/sshd_config" puppet_access_ssl.log | wc -l)
# Grab count of PUT requests for files under /dev/report
report_count=$(grep "PUT /dev/report" puppet_access_ssl.log | wc -l)
# Counter for sshd_config HTTP codes != 200
rc_count=0
# Counter for any return code != 200
all_rc_count=0
# PUT request counter
put_count=0

# for i in $(grep "/production/file_metadata/modules/ssh/sshd_config" puppet_access_ssl.log)
while read -r line
do
  
  # Count number response codes != 200
  return_code=$(echo $line | awk '{print $9}')
  if [ "$return_code" -ne "200" ]
  then
    all_rc_count=$(expr $all_rc_count + 1)
  fi

  if [ $(echo $line | grep "/production/file_metadata/modules/ssh/sshd_config" | wc -l) -gt 0 ]
  then
    # Grab the 9th field in the file (return code)
    ssh_return_code=$(echo $line | awk '{print $9}')
    if [ "$ssh_return_code" -ne "200" ]
    then
      # sshd_config return code != 200
      rc_count=$(expr $rc_count + 1)
    fi
  fi
  
  # Operate on PUT /dev/report lines
  if [ $(echo $line | grep "PUT /dev/report" | wc -l) -gt 0 ]
  then
    if [ $put_count -eq 0 ]
    then
      # First iteration - initialize 2 arrays ip and ip_count
      ip[$put_count]=$(echo $line | awk '{print $1}')
      ip_count[$put_count]="1"
      put_count=$(expr $put_count + 1)
      
    else
      # check ip for IP address from current line
      match="no"
      for i in "${ip[@]}"
      do
        if [ "$i" == "$(echo $line | awk '{print $1}')" ]
        then
          # Existing IP - increment count
          ip_count[$put_count]=$(expr ${ip_count[$put_count]} + 1)
          match="yes"
        fi
      done
      
      if [ "$match" == "no" ]
      then
        # No matches found in array ip - add to array
        ip[$put_count]=$(echo $line | awk '{print $1}')
        ip_count[$put_count]="1"
        put_count=$(expr $put_count + 1)
      fi
    fi
  fi
done < puppet_access_ssl.log

# Print results

echo "/production/file_metadata/modules/ssh/sshd_config was fetched $sshd_count times."
echo "Of the nuber of times sshd_config was fetched, Apache returned $rc_count non 200 response codes."
echo "Of all requests in the file, $all_rc_count non 200 response codes were seen."
echo "$report_count PUT requests were sent to a path under /dev/report, of those the following IPs were seen:"

for (( j=0; j<${#ip[@]}; j++ ))
do
  echo "IP ${ip[$j]} was seen ${ip_count[$j]} time(s)."
done
