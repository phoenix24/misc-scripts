#!/bin/bash

function pagedeploy(){
    echo "deploying paged.me."
    cd ../tmp && play gae:deploy --gae ../gae/appengine-java-sdk-1.3.7
}

function pageprep() {
    echo "checking for app git-status"
    
    status=`git diff --raw`
    if [[ -z $status ]]; then
        echo "app is ready to deploy"
    else
        echo "uncommited changes remain, app cannot be deployed."
        exit 0
    fi

    echo "preping paged.me for deploy."
    git archive master --format zip > ../page.me.zip && rm -rf ../tmp/ && mkdir ../tmp && cd ../tmp && unzip ../page.me.zip 
}

function pageclean() {
    echo "removing the tmp && paged.me.zip"
    echo `pwd`
}

if [[ -z $1 ]]; then
    echo "usage:"
    echo "  prep   - to initiate the deployment, extract from git archive; and sanitize"
    echo "  deploy - to start the actual deployment"
    exit 0
fi

if [[ $1 == 'deploy' ]]; then
    pagedeploy
    exit 0
fi

if [[ $1 == 'prep' ]]; then
    pageprep
    exit 0
fi

if [[ $1 == 'clean' ]]; then
    pageclean
    exit 0
fi


