#!/bin/bash
# Note: I did not get a chance to test this on a linux/mac machine, 
# but all except the docker parts were tested in an online tool 
filepathapi=$1
if [ -z "$filepathapi" ]
then
    path=$(pwd)
    filepathapi="$path/testdir"
fi
export filepathapi
docker build -t filepathapi:latest .
docker compose up