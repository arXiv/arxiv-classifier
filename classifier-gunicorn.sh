#!/usr/bin/env bash

#PROCESSOR_COUNT=$(nproc)
#GUNICORN_WORKER_COUNT=$(( PROCESSOR_COUNT * 2 + 1 ))

GUNICORN_WORKER_COUNT=4

gunicorn -w ${GUNICORN_WORKER_COUNT} -b 128.84.4.60:9808 'classifier.test_app:create_app()'
