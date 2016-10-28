#!/bin/bash

set -euo pipefail

cd $(dirname ${BASH_SOURCE[0]})

export TAG=latest
export REGISTRY=docker.apiumtech.io
readonly DC="docker-compose -p nextchefdevserv -f compose/development-services.yml"
$DC up
