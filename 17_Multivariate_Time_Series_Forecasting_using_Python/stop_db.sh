#!/bin/bash

# Stop and remove TimescaleDB container
echo "Stopping TimescaleDB..."
docker stop timescaledb
docker rm timescaledb
echo "TimescaleDB stopped and removed"
