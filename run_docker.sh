#!/bin/bash
DB=db
# PG=pgadmin
DJANGO=web
# NGINX=nginx
SPARK=spark
KAFKA=kafka
ZOOKEEPER=zookeeper

if [[ "$*" == *windows* ]]
then
    DOCKER="winpty docker"
    DOCKER_COMPOSE="winpty docker-compose"
else
    DOCKER="docker"
    DOCKER_COMPOSE="docker-compose"
fi

sudo service postgresql* stop
sudo service nginx stop

$DOCKER_COMPOSE up -d $ZOOKEEPER $SPARK $DB
sleep 2
$DOCKER_COMPOSE up -d $KAFKA 
$DOCKER_COMPOSE up $DJANGO  