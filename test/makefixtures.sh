#!/bin/bash
rm -rf fixtures
rm fixtures.tar.gz
mkdir fixtures
mongod --smallfiles --fork --nssize=1 --oplogSize=1 --master --logpath mongo.log --dbpath fixtures --quota --quotaFiles 1
sleep 5
mongo test fixtures.js
sleep 60
mongo test fixtures.js
sleep 60
mongo test fixtures.js
sleep 60
mongo test fixtures.js
killall mongod
tar pczf fixtures.tar.gz fixtures
rm -rf fixtures
rm mongo.log
