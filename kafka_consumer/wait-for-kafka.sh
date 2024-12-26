#!/bin/bash
set -e

KAFKA_HOST="${KAFKA_HOST:-localhost}"
KAFKA_PORT="${KAFKA_PORT:-9092}"

echo "Waiting for Kafka to be ready at $KAFKA_HOST:$KAFKA_PORT..."

while ! nc -z "$KAFKA_HOST" "$KAFKA_PORT"; do
  sleep 1
done

echo "Kafka is ready! Starting the producer..."
exec "$@"
