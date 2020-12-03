# Description of deployed resources

The classifier is deployed to GCP in the arxiv-classifier-dev
project. It is run as VMs running docker images in a managed instance
group. This is then served via a GCP load balancer to a reserved IP
address. In AWS route53 classifier.labs.arxiv.org is pointed to that
IP address.

There is a build trigger in arxiv-classifier-dev that builds on
commits to the develop branch.
[classifier triggers in GCP](https://console.cloud.google.com/cloud-build/triggers?authuser=1&project=arxiv-classifier-dev)

The status can be checked here:
https://classifier.labs.arxiv.org/status

# How to deploy from scratch 

These are instructions to deploy a new load balancer, managed instnce
group and certificate to a GCP project. Once these are run they do not
need to be run again for the project. These do not need to be repeted
if you goal is to update the classifer image running on the VM
containers.

The `arxiv-classifier/deploy` directory has the scripts `config.sh`,
`make-instance-group.sh`, `upload-cert.sh` and
`make-load-balancer.sh`.

## Step one preliminaries
To deploy you'll need the GCP SDK installed and a GCP account with
access to the project. You'll need to get the labs.arxiv.org
certficate from last pass and save it as
`arxiv-classifier/deploy/labs.arxiv.org.crt and
`arxiv-classifier/deploy/labs.arxiv.org.key`

## Step two config
Check that `config.sh` has the URL for the classifier image you want
to deploy. You can get the URLs from the [GCP container
registry](https://console.cloud.google.com/gcr/images/arxiv-classifier-dev?project=arxiv-classifier-dev&authuser=1).

If the image URL is not what you want you can edit it in that file, or source the file then do:
```
source deploy/config.sh
export IMAGE_URL="gcr.io/arxiv-classifer-dev/classifier@git-commit:1234ABCD"
```
If the image URL is fine do:
```
source deploy/config.sh
```
## Step three do it
```
cd arxiv-classifier/deploy
./make-instance-group.sh
./upload-cert.sh
./make-load-balancer.sh
```

At this point the project will have an instance group running the
classifier, a load balancer and a reserved IP address. If you need a
domain name to point to the IP address, go to your provider and define
a new name.

# How to update the classifier in an existing deploy
In GCP there are two things needed to update the containers' images in
a managed instance group. One is to update the instance-template and
the second is to start a rolling update.

```
cd arxiv-classifier/deploy
./update-image.sh "SOME_GCP_IMAGE_URL"
```

