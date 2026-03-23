#!/bin/bash
set -e

export APOLLO_ELV2_LICENSE=accept

echo "Composing supergraph schema from subgraphs..."

for i in $(seq 1 30); do
    if rover supergraph compose --config /app/supergraph.yaml 2>/dev/null > /tmp/supergraph.graphql && [ -s /tmp/supergraph.graphql ]; then
        cp /tmp/supergraph.graphql /app/supergraph.graphql
        echo "Supergraph composed successfully"
        break
    fi
    echo "Waiting for subgraphs... (attempt $i/30)"
    sleep 3
done

if [ ! -s /app/supergraph.graphql ]; then
    echo "ERROR: Failed to compose supergraph schema"
    exit 1
fi

echo "Starting Apollo Router..."
exec router --dev --config /app/router.yaml --supergraph /app/supergraph.graphql --log info
