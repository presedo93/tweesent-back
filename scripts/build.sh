#!/bin/bash

dir=${pwd}
cd ..
docker build -f docker/Dockerfile -t tweesent-back .
cd $dir