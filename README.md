# CissTM Satellite V2 (Python)
[![Build Status](https://travis-ci.com/CISSTM/SatelliteV2.svg?branch=master)](https://travis-ci.com/CISSTM/SatelliteV2)


This is the newer version of the CissTM satellite, it's written in Python (instead of NodeJS), because of compatebility issues.

## How to install
### Clone from Github
Download the project
```
git clone https://github.com/CISSTM/SatelliteV2.git
```
### Open downloaded folder
```
cd SatelliteV2
```
### Install requirements
Firstly, install pip3 (the Python package manager).
```
sudo apt upgrade
sudo apt install python3-pip
```
Then install the requirements.
```
pip3 install -r requirements.txt
```
If there's a permission error, then you could use:
```
sudo pip3 install -r requirements.txt
```
### Run
Run the satellite software by using:
```
python3 src/main.py
```

