#!/usr/bin/bash

while true; do
    while read j; do
        killall python3 > /dev/null 2>&1
        python3 main.py &
        sleep 1
    done < <(inotifywait -q -e modify -e delete -e create --exclude db.json *)
done
