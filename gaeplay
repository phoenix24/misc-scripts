#!/bin/bash

function deploy(){
    echo "deploying paged.me."
    cd ../tmp && play gae:deploy --gae ../gae/appengine-java-sdk-1.3.7
}

function prep() {
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

function clean() {
    echo "removing the tmp && paged.me.zip"
    rm -rf ../page.me.zip && rm -rf ../tmp/ 
}

case "$1" in
    "deploy")
        deploy
        exit 0
        ;;

    "prep"  )
        prep
        exit 0
        ;;

    "clean" )
        clean
        exit 0
        ;;

    *       )
        echo "  prep   - to initiate the deployment, extract from git archive; and sanitize"
        echo "  deploy - to start the actual deployment"
        exit 0
        ;;
esac

exit 0
