# timetable-to-csv
## About
A web scraping application for students at the University of Essex which stores timetable information in a CSV file for use in Microsoft Excel, Google Calendar etc.

## Preparation
Install Python3.

    ## Ubuntu/Debian
    sudo apt-get update
    sudo apt-get install python3 python3-pip

    ## Fedora/Red Hat
    sudo dnf install python3 python3-pip

Install dependencies using pip.

    sudo pip install bs4 datetime tabulate requests robobrowser requests_ntlm

Ensure the program has execution permissions.

    chmod +x timetable.py

## Run

    ./timetable.py
