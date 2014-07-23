#!/bin/bash
# Functions for creating sessions with dbus in kde4

# Needs konsole to be launched with --nofork

. $HOME/bin/elves.sh


# format : tabname, hostname, command
konsole_env=(
     "bouzeron" "bouzeron" "echo coucou bouzeron"
     "burp"    ""          "ls"
)

setup_konsole_env 2
