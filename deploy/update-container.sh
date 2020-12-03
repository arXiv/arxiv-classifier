#!/bin/bash
# create a new tempalte

# TODO Fix this witht he rolling command

# update MIG to new tempalte
gcloud compute instance-groups managed set-instance-template instance-group-name \
    --template instance-template \
    --zone zone
