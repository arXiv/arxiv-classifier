#!/bin/sh
# script to run under systemd
su busybody
source /cache/lucene/classifier-venv/bin/activate
cd /users/e-prints/arxiv-classifier
./classifier-gunicorn.sh
