export PROJ=arxiv-classifier-dev
export PORT=9808
export CLASSIFIER_MIG=classifier-dev-mig
export ZONE=us-east1-d
export TEMPLATE=classifier-template

# This should not be set to latest so the instance tempalte is deterministic
# but there is probably a better way to do this.
export IMAGE_URL="gcr.io/arxiv-classifier-dev/classifier@sha256:320fa932b844a790aab29b3dbae3f7e7d6b08544e71da2ef757159d4efebf0c2"
