#! /usr/bin/bash 

screen -S server -X stuff list
sleep 3
screen -S server -X hardcopy /root/server_logs.txt

cat /root/server_logs.txt | grep players