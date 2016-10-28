#!/bin/bash

set -eux

exec 1> >(logger -s -t NextChef-out/$(basename $0) 2>&1)
exec 2> >(logger -s -t NextChef-err/$(basename $0))

cd $(dirname ${BASH_SOURCE[0]})

export REGISTRY=$REGISTRY
export TAG=$TAG

readonly DOCKER_COMPOSE="docker-compose -p nextchefprod -f compose/base.yml -f compose/staging.yml"
$DOCKER_COMPOSE down || true 
$DOCKER_COMPOSE pull
$DOCKER_COMPOSE up -d
