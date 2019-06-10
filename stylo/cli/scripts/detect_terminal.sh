#!/bin/bash

# Due to the wide array of terminal emulators used by linux users we need
# a way to determine which one the user is currently using so that when it
# comes to launching our own commands we know which one to use.
#
# The majority of this script is based on the following answer on askubuntu
# but tweaked to our needs: https://askubuntu.com/a/508047

# Now that we have the PID we can get a lot of imformation about it from the
# /proc directory. There is far far to much going on here to go through now but
# if you're interested I recommend the following article that goes through this
# directory in great detail:
#
# http://www.tldp.org/LDP/Linux-Filesystem-Hierarchy/html/proc.html
#
# What we are after is the PID of parent process of our shell since that will
# belong to the terminal emulator the user is currently using. We can get that
# information from the /proc/PID/stat file. This file is machine friendly so
# if we were to cat it yourself you would see a large collection on meaningless
# numbers. However through the power of man pages the number we are interested
# in is in the 4th column.
#
# For more details see: http://man7.org/linux/man-pages/man5/proc.5.html
# To find the relevant section Ctrl+F for: /proc/[pid]/stat
#
get_ppid () {
    echo $(cat /proc/$1/stat | cut -f 4 -d \  )
}

# Once we have the PID of the parent process we can determine the name of the
# command associated with it using the `ps` command. Again there is so much
# detail we could go into here but if you are interested I suggest checking
# out the man page.
#
# http://man7.org/linux/man-pages/man1/ps.1.html
get_proc_name () {
    echo $(ps -p $1 -o comm= )
}

contains () {
    x=$1

    shift
    values=("$@")

    for i in "${values[@]}"
    do
        if [ "$i" == "$x" ]; then
            echo 0
            return
        fi
    done

    echo 1
}

old_pid=$$
ignore=("bash" "python" "stylo")

while :
do
    ppid=$(get_ppid $old_pid)
    name=$(get_proc_name $ppid)

    should_ignore=$(contains $name "${ignore[@]}")

    if ! [ "$should_ignore" == "0" ]; then
        break
    fi

    old_pid=$ppid
done

echo -e "$name\t$(which $name)"
