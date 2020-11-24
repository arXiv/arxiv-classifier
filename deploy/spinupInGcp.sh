#!/bin/bash
set -v

# Deploys to a MIG in GCP
# Steps
#  instance template
#  managed instance group
#  create backend service with that MIG
#  create 
#

# This is for the initial create of the classifier resources in GCP

if [[ ! $(gcloud config get-value project) =~ "classifier" ]]
then
    echo "It seems you are not configured to a classifier GCP project."
    echo "Run something like 'gcloud config set project arxvi-classifier'"
    exit 1
fi

if [[ ! -d "./models" ]]
then
    if [[ ! $(xz --help) ]]
    then
        echo "The utility xz needs to be installed to get and decompress the model"
        exit 1
    fi
    echo "Downloading and decompressing model"
    gsutil cp gs://arxiv-classifier-dev-models/models.tar.xz models.tar.xz
    xz --decompress models.tar.xz
    tar xf models.tar
fi

SHORT_SHA=$(git rev-parse --short HEAD)
# Tricky quirk of GCP: the part after gcr.io must be a GCP project.
CLASIFIER_IMAGE_TAG="gcr.io/arxiv-classifier-dev/classifier"

echo "Starting docker build"
docker build \
       --build-arg git_commit="$SHORT_SHA" \
       -t "$CLASIFIER_IMAGE_TAG" \
       --label git-commit=$SHORT_SHA \
       --label github-repo=arxiv-classifier \
       .

gcloud auth configure-docker
docker push "$CLASIFIER_IMAGE_TAG"

CLASSIFIER_VM_NAME="classifier-vm"

gcloud compute instances describe --zone=us-east1-d classifier-vm
if [[ ! $? ]]
then
    # VM has not yet been started so start one up.
    
    # Setup firewall to allow access to just cornell VMs which have
    # the arxiv web nodes. An additional rule will be needed to
    # allow access to GCP VMs.
    gcloud compute firewall-rules create fw-allow-cornell-to-9808 \
           --network=default \
           --action=allow \
           --direction=ingress \
           --source-ranges=128.84.0.0/16 \
           --target-tags=allow-cornell-web-nodes \
           --rules=tcp:9808
    
    ### Setup the VM with docker image ###
    # create the VM running the docker image for arxiv labs
    gcloud compute instances create-with-container "$CLASSIFIER_VM_NAME" \
           --zone=us-east1-d  \
           --container-image "$CLASIFIER_IMAGE_TAG:latest"
    
    # add tags to pickup the firewall
    gcloud compute instances add-tags "$CLASSIFIER_VM_NAME" \
           --zone=us-east1-d \
           --tags=allow-cornell-web-nodes
else
    gcloud compute instances update-container "$CLASSIFIER_VM_NAME" \
           --zone=us-east1-d \
           --container-image "$CLASIFIER_IMAGE_TAG:latest"



