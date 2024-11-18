#!/usr/bin/env bash

docker-compose exec deploy sh -c "rm /data/build2neo/*-part*.csv"
docker-compose up -d

