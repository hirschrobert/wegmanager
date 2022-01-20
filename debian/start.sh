#!/bin/sh

group=accounting

if [ $(id -gn) != $group ]; then
  exec sg $group "$0"
fi

/opt/wegmanager/bin/python /opt/wegmanager/bin/wegmanager