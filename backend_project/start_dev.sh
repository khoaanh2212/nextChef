#!/usr/bin/env bash
set -e
set -u
export TAG=latest
export REGISTRY=docker.apiumtech.io
echo 'EMPTY_DEVELOPMENT_ENV=TRUE' > development.env
readonly DOCKER_COMPOSE="docker-compose -p nextchefdev -f compose/base.yml -f compose/development.yml"
$DOCKER_COMPOSE stop && yes | $DOCKER_COMPOSE rm && $DOCKER_COMPOSE build && $DOCKER_COMPOSE up -d
docker inspect --format '{{range .Config.Env}}{{println . }}{{end}}' nextchefdev_web_1 > development.env
$DOCKER_COMPOSE logs
