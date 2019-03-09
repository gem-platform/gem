#!/bin/sh
# export environment file for cron
printenv | sed 's/^\(.*\)$/export \1/g' > .env

# run app
service rsyslog start
service cron start

tail -f /var/log/messages