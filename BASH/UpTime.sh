#!/bin/bash

showUpTime(){
	local up=$(uptime -p | cut -c4-)
	local since=$(uptime -s)
	cat << EOF
----
This Machine has been up for ${up}
It has been running since ${since}
____
EOF
}

showUpTime
