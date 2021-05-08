#!/bin/bash
# Add a user to the broker.

PASSWD_FILE="/mosquitto/config/pwfile"

usage()
{
  echo "Usage: add_user.sh -c [username] | add_user.sh -b [username] [password]"
}

while getopts "c:b:" option
do
  case "${option}" in
    c)
      docker exec -it mission-broker /bin/ash -c "mosquitto_passwd -c ${PASSWD_FILE} ${OPTARG}"
      ;;
    b)
      if [[ $# -eq 3]]
      then
        docker exec -it mission-broker /bin/ash -c "mosquitto_passwd -b ${PASSWD_FILE} ${OPTARG} $3"
      else
        echo "ERROR: bad arguments number."
        usage
      ;;
    :)
      echo "ERROR: -${option} requires the username as argument."
      usage
      ;;
    \?)
      echo "ERROR: -${option} is not supported."
      usage
      ;;
    esac
done
