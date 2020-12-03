#!/bin/bash
#Script to setup the classifier
# See README.md for details
source config.sh

./make-instance-group.sh
./upload-cert.sh
./make-load-balancer.sh
