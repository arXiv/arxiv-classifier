### Setting up the load balancer ###
set -ev

# from https://cloud.google.com/load-balancing/docs/https/ext-https-lb-simple#load-balancer
# Modified slightly for wsgi port at $PORT

# reserve an IP address
# gcloud compute addresses create lb-ipv4-classifier \
#        --project=$PROJ \
#        --ip-version=IPV4 \
#        --global
       

# # Need a health check for the load balancer to know if the backend is up
# gcloud compute health-checks create http classifier-health-check \
#        --port $PORT \
#        --request-path="/status" \
#        --check-interval 20s \
#        --healthy-threshold 1 \
#        --unhealthy-threshold 3 \
#        --project=$PROJ \

# # Need to open the firewall to perform health check on instances
# gcloud compute firewall-rules create allow-classifier-health-check \
#         --allow tcp:$PORT \
#         --source-ranges 130.211.0.0/22,35.191.0.0/16 \
#         --network default

# Create a backend service
gcloud compute backend-services create classifier-backend-service \
       --project=$PROJ \
       --port-name=http \
       --health-checks=classifier-health-check \
       --global

# Add backend as a link to classifier instance group
gcloud compute backend-services add-backend classifier-backend-service \
       --project=$PROJ \
       --instance-group=$CLASSIFIER_MIG \
       --instance-group-zone=$ZONE \
       --balancing-mode=RATE \
       --max-rate=200 \
       --global

# Create a URL map to route incoming requests to the backend service:
# This becomes the name of the load balancer in the GCP UI
gcloud compute url-maps create classifier-dev-lb \
       --project=$PROJ \
       --default-service classifier-backend-service

# Create a target HTTP(S) proxy to route requests to your URL map.
# The proxy is the portion of the load balancer that holds the SSL
# certificate.
gcloud compute target-https-proxies create classifier-target-https-proxy \
       --project=$PROJ \
       --ssl-certificates=labs-ssl-cert \
       --url-map=classifier-dev-lb

# Create a global forwarding rule to route incoming requests to the proxy.
gcloud compute forwarding-rules create classifier-dev-forwarding-rule \
       --project=$PROJ \
       --address=lb-ipv4-classifier \
       --target-https-proxy=classifier-target-https-proxy \
       --global \
      --ports=443

#  Create a target HTTPS proxy to route requests to your URL map. 
# The proxy is the portion of the load balancer that holds the SSL certificate 
# for HTTPS Load Balancing, so you also load your certificate before this step.
gcloud compute target-https-proxies create https-lb-proxy \
       --project=$PROJ \
       --url-map classifier-dev-lb \
       --ssl-certificates labs-ssl-cert

# If the load balancer doesn't work after about 60 sec.
# to to the GCP UI, go to load balancer, go to the load balancer that
# this script creates, click edit, click finalize and then save (or update)
