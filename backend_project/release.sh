#!/usr/bin/env bash
set -eux
cd ..
REGISTRY=$1
commit_hash=int_$(git rev-parse HEAD)
docker pull $REGISTRY/nextchef:$commit_hash
git checkout master
git stage version.txt
./increment_version.sh -p
git add version.txt
version=$(cat version.txt)
docker pull $REGISTRY/nextchef:$commit_hash
docker tag $REGISTRY/nextchef:$commit_hash $REGISTRY/nextchef:$version
docker push $REGISTRY/nextchef:$version
git commit -m "incremented version in version.txt"
git push origin master
git tag -a $version -m "incremented version"
git push origin --tags
cd backend_project
make deploy-production TAG=$version REGISTRY=docker.apiumtech.io