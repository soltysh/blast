#!/bin/bash

# create ui build and deployment configs and associated image streams
oc new-app \
    soltysh/lighttpd-centos7~https://github.com/soltysh/blast.git \
    --context-dir=ui \
    --name=ui \
    --labels=app=ui
# set readiness probe in deployment config
oc set probe dc/ui --readiness --get-url=http://:8080/
# create route for the frontend
oc expose svc/ui

# create remaining resources from pre-configured templates
for dir in image text video
do
    oc new-app ${dir}/template.yaml
done
