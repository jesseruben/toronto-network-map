#!/usr/bin/env bash
sudo apt-get update
sudo apt-get upgrade

# for crypto setup -->before running pip install -r requrments
sudo aptitude install libffi-dev

# for postgres
sudo apt-get install postgresql postgresql-contrib
sudo apt-get install libpq-dev python-dev

#for gis
sudo apt-get install binutils libproj-dev gdal-bin
sudo apt-get install postgis*
