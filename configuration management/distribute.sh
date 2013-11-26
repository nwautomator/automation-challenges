#!/bin/bash

# Distribution count
dist_count=0
# Extraction count
ext_count=0
# Puppet count
pup_count=0

for h in `cat hosts | egrep -v ^#` 
do    
  # Distribute our module
  scp widget.tar.gz root@$h:/etc/puppet/modules > /dev/null
  if [ $? -ne 0 ]
  then
    $dist_count=$(expr $dist_count + 1)
  fi
  # Extract the module
  ssh -t root@$h 'tar -zxvf /etc/puppet/modules/widget.tar.gz -C /etc/puppet/modules' > /dev/null
  if [ $? -ne 0 ]
  then
    $ext_count=$(expr $ext_count + 1)
  fi
  # Apply the module
  ssh -t root@$h 'puppet apply --debug -e "include widget"' > /dev/null
  if [ $? -ne 0 ]
  then
    $pup_count=$(expr $pup_count + 1)
  fi
        

done

if [ $dist_count -gt 0 ] || [ $ext_count -gt 0 ] || [ $pup_count -gt 0 ]
then
  echo "There were $dist_count failures in distributing the module."
  echo "There were $ext_count failures in extracting the module."
  echo "There were $pup_count failures in applying the module."
else
  echo "Module distribution, extraction, and application successful."
fi
