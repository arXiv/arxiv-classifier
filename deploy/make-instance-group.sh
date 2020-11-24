# makes the managed instance group for the classifier #

# TODO There is no updating of instance-templates.
# Need some way to have instance-templates that we create
# with a name and then we can update them. They either need to have the same
# name or we need to create new names constantly.
# Use part of the docker image hash?
# Use a date time stamp?
# FYI I was unable to delete an in use template.


gcloud compute instance-groups managed describe $CLASSIFIER_MIG 2&>1 > /dev/null
if [ ! $? ]
then
    # make template
    #https://cloud.google.com/compute/docs/instance-templates/create-instance-templates#with-container
    gcloud compute instance-templates create-with-container $TEMPLATE \
           --machine-type e2-medium \
           --tag=allow-classifier-health-check \
           --container-image $IMAGE_URL

    # make instance group
    gcloud compute instance-groups managed create $CLASSIFIER_MIG \
           --base-instance-name classifier \
           --size 2\
           --template $TEMPLATE \
           --zone $ZONE
    
    # Set named port for the load balancer to pick up. By default, the load
    # balancer is looking for http.
    gcloud compute instance-groups managed set-named-ports $CLASSIFIER_MIG \
           --named-ports http:$PORT \
           --zone=$ZONE
    
    # In the docs it shows an example with the named port as unmanaged:
    # https://cloud.google.com/load-balancing/docs/https/ext-http-lb-simple#named-port
    gcloud compute instance-groups unmanaged set-named-ports $CLASSIFIER_MIG \
           --named-ports http:$PORT \
           --zone=$ZONE
else
    echo "Skipping creating a new instance group since one already exists."
fi

exit 0

#UPDATe PROCESS
  gcloud compute instance-templates create-with-container classifier-templatev2 \
           --machine-type e2-medium \
           --tag=allow-classifier-health-check \
           --container-image $IMAGE_URL

  gcloud compute instance-groups managed set-instance-template $CLASSIFIER_MIG --template=classifier-templatev2 --zone=$ZONE

  gcloud compute instance-groups managed rolling-action start-update $CLASSIFIER_MIG \
    --version template=classifier-templatev2 \
    --max-surge 4 \
    --zone=$ZONE
