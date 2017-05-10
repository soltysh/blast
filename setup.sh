#!/bin/bash

# create all the templates for each
for dir in $(find * -maxdepth 0 -type d)
do
    oc new-app ${dir}/template.yaml
done
