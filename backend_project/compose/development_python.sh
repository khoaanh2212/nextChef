#!/bin/bash

set -euo pipefail

echo "reading /development.env"

while IFS='' read -r line || [[ -n "$line" ]]; do
    if [[ $line =~ ^([^[:space:]]+)=([^[:space:]]+)$ ]] ; then
        envkey="${BASH_REMATCH[1]}"
        envval="${BASH_REMATCH[2]}"
        if [ -z ${!envkey:-} ] ; then
            echo "FROM COMPOSE: $envkey=$envval"
            eval "export $envkey=$envval"
        else
            echo "FROM ENVIRONMENT: $envkey=${!envkey}"
        fi
    fi
done < "/development.env"

/usr/local/bin/python "$@"
