#!/bin/bash

# Start TimescaleDB container
echo "Starting TimescaleDB..."
docker run -d \
  --name timescaledb \
  -p 5432:5432 \
  -e POSTGRES_PASSWORD=postgres \
  timescale/timescaledb:latest-pg14

echo "Waiting for database to be ready..."
sleep 5

echo "TimescaleDB is running on port 5432"
echo "Connection details:"
echo "  Host: localhost"
echo "  Port: 5432"
echo "  User: postgres"
echo "  Password: postgres"
