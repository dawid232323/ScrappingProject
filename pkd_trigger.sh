#!/bin/bash
wc -l list_of_counties.txt > temp.txt
read lines words characters filename < temp.txt
while [ $lines -gt 0 ] 
do
    python3 better_api.py
    echo "Time for next iteration"
    wc -l list_of_counties.txt > temp.txt
    read lines words characters filename < temp.txt
done
