Microservices Federation Project
==============

This is a Docker (with docker-compose) environment for Microservices Federation Project.
Is a example that how we can to federate multiples microservices using [Apollo Federation](https://www.apollographql.com/docs/federation/).
Each schema in each microservice works independently. With Apollo Federation they work like a team.

![Microservices Federation](./docs/microservices-federation.png?raw=true "Graph of Microservices Federation")

# Installation

1. First, clone this repository:

```bash
git clone https://github.com/nietzscheson/microservices-federation
```
2. Copy the environment vars:

```bash
cp .env.dist .env
```
3. Init project
```bash
make
```
4. Show containers:
```bash
make ps
```
This results in the following running containers:
```bash
docker-compose ps
  Name                Command                  State               Ports
---------------------------------------------------------------------------------
gateway    dumb-init -- npm start           Up             0.0.0.0:4000->80/tcp
postgres   docker-entrypoint.sh postgres    Up (healthy)   0.0.0.0:5432->5432/tcp
product    sh ./entrypoint.sh flask r ...   Up (healthy)   0.0.0.0:5001->5000/tcp
user       sh ./entrypoint.sh flask r ...   Up (healthy)   0.0.0.0:5000->5000/tcp
```
The microservices are running in:

- APIGateway: [localhost:4000/graphql](localhost:4000/graphql)
- User API: [localhost:5000/graphql](localhost:5000/graphql)
- Product API: [localhost:5001/graphql](localhost:5001/graphql)
- Order API: [localhost:5002/graphql](localhost:5002/graphql)

5. Run test:
```bash
make test
```
