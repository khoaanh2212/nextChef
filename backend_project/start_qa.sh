#!/bin/bash

set -e
set -u

cd $(dirname ${BASH_SOURCE[0]})

export TAG=latest
export REGISTRY=docker.apiumtech.io
readonly DOCKER_COMPOSE="docker-compose -p nextchefqa -f compose/base.yml -f compose/qa.yml"

git pull origin master
make docker-image

$DOCKER_COMPOSE kill
$DOCKER_COMPOSE rm -f

echo
echo "!! RUNNING : http://localhost:8001"
echo

$DOCKER_COMPOSE up
