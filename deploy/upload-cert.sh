  ### upload SSL cert to GCP ###
if [ ! -e "labs.arxiv.org.key" ] 
then
  echo "The labs.arxiv.org.key is required. Get it from lastpass."
  exit 1
fi
if [ ! -e "labs.arxiv.org.crt" ] 
then
  echo "The labs.arxiv.org.crt is required. Get it from lastpass."
  exit 1
fi

  gcloud compute ssl-certificates create labs-ssl-cert \
      --project=$PROJ \
      --certificate=labs.arxiv.org.crt \
      --private-key=labs.arxiv.org.key \
      --global
