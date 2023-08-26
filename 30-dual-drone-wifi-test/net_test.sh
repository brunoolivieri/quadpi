#!/bin/bash

IP_TARGET='192.168.1.1'
TIMEOUT=5
PING_RETRIES=10
IPERF_PERIOD=15

echo "----------------------------------------------------------"
echo "RUNNING TEST WITH CODE $1"
echo "----------------------------------------------------------"

DATE=$(date +"%Y-%m-%d-%Hh-%Mm-%Ss")
echo -e "\n\n [log] são $DATE \n\n"

echo -e "\nTesting bitrate UDP with flow control: \n"
iperf3 -c $IP_TARGET -t $IPERF_PERIOD -u -l 1460
echo -e "\n\n"

echo -e "Testing bitrate TCP: \n"
iperf3 -c $IP_TARGET -t $IPERF_PERIOD
echo -e "\n\n"

echo -e "Testing bitrate TCP: \n"
iperf3 -c $IP_TARGET -t $IPERF_PERIOD
echo -e "\n\n"

echo -e "\nTesting PING 50 bytes: "
ping $IP_TARGET -w $TIMEOUT -4 -c $PING_RETRIES -s 50

echo -e "\nTesting PING 100 bytes: "
ping $IP_TARGET -w $TIMEOUT -4 -c $PING_RETRIES -s 100

echo -e "\nTesting PING 500 bytes: "
ping $IP_TARGET -w $TIMEOUT -4 -c $PING_RETRIES -s 200

echo -e "\nTesting PING 1000 bytes: "
ping $IP_TARGET -w $TIMEOUT -4 -c $PING_RETRIES -s 1000

DATE=$(date +"%Y-%m-%d-%Hh-%Mm-%Ss")
echo -e "\n\n [log] são $DATE \n\n"

echo -e "**********************************************************"
echo -e "FINISHING TEST WITH CODE $1"
echo -e "**********************************************************\n\n\n"
