#!/bin/sh

set -e

host="$1"
shift
cmd="$@"

echo "⏳ Waiting for PostgreSQL at $host..."
until nc -z "$host" 5432; do
  sleep 1
done

echo "✅ PostgreSQL is ready! Starting FastAPI..."
exec $cmd
