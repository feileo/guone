#!/bin/sh
debug="debug"
arg=$1

if [ -z $arg ]
then
    arg='no_debug'
fi

if [ $arg = $debug ]
then 
    ./bin/guone
else
    ./bin/gunicorn -k gevent  -c gun.conf app:app
fi
