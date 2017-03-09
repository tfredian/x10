#!/bin/bash
cat << EOF
Status: 200 OK
Content type: text/plain

EOF
export X10CONFIG=/var/www/x10config
export $(echo "$QUERY_STRING" | awk -F\& '{print tolower($1) " " tolower($2) " " tolower($3)}')
if [ -z "$cmd" ]
then
  case $op in
    get)
      heyu onstate $name;;
    set)
      heyu $state $name;;
  esac
else
  cmd=$(echo $cmd | awk '{gsub("%20"," ");print $0}')
  heyu $cmd
fi

