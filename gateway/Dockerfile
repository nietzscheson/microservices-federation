FROM node:22-slim

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install Rover CLI
RUN npm install -g @apollo/rover@latest

# Install Apollo Router v2
WORKDIR /tmp
RUN curl -sSL https://router.apollo.dev/download/nix/v2.12.0 | sh && \
    mv /tmp/router /usr/local/bin/router

WORKDIR /app

COPY supergraph.yaml router.yaml entrypoint.sh ./
RUN chmod +x entrypoint.sh

EXPOSE 4000

ENTRYPOINT ["./entrypoint.sh"]
