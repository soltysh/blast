#!/bin/bash

# create service account for the cron job
oc create serviceaccount scraper
oc policy add-role-to-user view -z scraper

# create all the templates for each component
for dir in $(find * -maxdepth 0 -type d)
do
    oc new-app ${dir}/template.yaml
done
