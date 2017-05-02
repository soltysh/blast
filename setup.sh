#!/bin/bash

# create config first
oc new-app config.yaml

# and then remaining resources
for dir in $(find * -maxdepth 0 -type d)
do
    oc new-app ${dir}/template.yaml
done
