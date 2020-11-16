# arxiv/classifier

# This is slightly different than arxiv-base:
# It is python:3.6-slim based, not centos
# IUS is only needed in centos7 so IUS is not needed
# It is a multi stage build to make a smaller image.
# Mysql is not installed since it is not needed.
# A python venv is activated by setting PATH.
# Installing from requirements.txt because pipenv takes a very long time to resolve deps.

FROM python:3.6-slim as compile-image

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

# Setup venv and put into use. https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV

# Every python thing after this is in the venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt ./
RUN pip install --no-deps -r requirements.txt
 
########## STAGE 2 ##############
FROM python:3.6-slim as build-image
ARG git_commit

ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /opt/arxiv/
ADD models /opt/arxiv/models
COPY --from=compile-image /opt/venv /opt/venv

RUN echo $git_commit > /git-commit.txt
ADD classifier /opt/arxiv/classifier

entrypoint ["/opt/venv/bin/gunicorn", "-w", "4",\
           "-b", "0.0.0.0:9808",\
           "--log-file=-",\
           "--worker-tmp-dir", "/dev/shm",\
           "classifier.test_app:create_app()"]

