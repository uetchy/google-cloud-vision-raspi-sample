#!/bin/sh

pip-compile requirements.in
docker-compose build
