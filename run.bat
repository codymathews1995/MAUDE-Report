@echo off
echo Building Docker images...
docker-compose build --no-cache

echo Starting Docker containers...
docker-compose up
