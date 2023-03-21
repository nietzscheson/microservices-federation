Microservices Federation Project
==============

This is a Docker (with docker-compose) environment for Microservices Federation Project.
Is a example that how we can to federate multiples microservices using [Apollo Federation](https://www.apollographql.com/docs/federation/).
Each schema in each microservice works independently. With Apollo Federation they are combine into a single graph.

![Microservices Federation](./docs/microservices-federation.png?raw=true "Graph of Microservices Federation")

# Installation

1. First, clone this repository:

```bash
git clone https://github.com/nietzscheson/microservices-federation
```
2. Init project
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
--------------------------------------------------------------------------------
gateway   docker-entrypoint.sh /bin/ ...   Up             0.0.0.0:4000->80/tcp
order     sh ./entrypoint.sh flask r ...   Up (healthy)   0.0.0.0:5003->5000/tcp
product   sh ./entrypoint.sh flask r ...   Up (healthy)   0.0.0.0:5002->5000/tcp
user      sh ./entrypoint.sh flask r ...   Up (healthy)   0.0.0.0:5001->5000/tcp
```
The microservices are running in:

- APIGateway: [localhost:4000/graphql](http://localhost:4000/graphql)
- User API: [localhost:5000/graphql](http://localhost:5001/graphql)
- Product API: [localhost:5001/graphql](http://localhost:5002/graphql)
- Order API: [localhost:5002/graphql](http://localhost:5003/graphql)

5. Run test:
```bash
make test
```
