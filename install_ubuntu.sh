#!/bin/bash
sudo apt-get update

sudo apt-get install libblas-dev liblapack-dev gfortran python-pip python-dev build-essential

sudo pip install -r requirements.txt
