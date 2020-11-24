
# create a new tempalte

# update MIG to new tempalte
gcloud compute instance-groups managed set-instance-template instance-group-name \
    --template instance-template \
    --zone zone
