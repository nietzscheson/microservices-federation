# Microservices Federation

A hands-on example of how to federate multiple microservices into a single GraphQL API using [Apollo Federation](https://www.apollographql.com/docs/federation/).

Each microservice owns its own GraphQL schema and runs independently. Apollo Gateway composes them into a single unified graph, allowing clients to query across services transparently.

![Microservices Federation](./docs/microservices-federation.png?raw=true "Graph of Microservices Federation")

## Why Federation?

In a microservices architecture, each service typically exposes its own API. This forces clients to know which service owns which data and to orchestrate multiple requests. Apollo Federation solves this by:

1. **Each service defines its own schema** — the User service knows about users, the Product service knows about products, the Order service knows about orders.
2. **Services extend types from other services** — the Product service can add a `createdBy` field that references the `UserType` defined in the User service, without depending on it directly.
3. **The Gateway composes everything** — Apollo Gateway introspects all subgraph schemas, merges them into a single supergraph, and routes incoming queries to the right services automatically.

The result: clients see **one unified GraphQL API** while each team maintains its own independent service.

### Services

| Service   | Port | Description                                      |
|-----------|------|--------------------------------------------------|
| Gateway   | 4000 | Apollo Gateway — composes all subgraphs           |
| User      | 5001 | Manages users (`UserType`)                        |
| Product   | 5002 | Manages products, references `UserType` via `createdBy` |
| Order     | 5003 | Manages orders, references `UserType` and `ProductType` |

### How Federation connects the services

The **User service** defines the `UserType` as a federation entity with a key:

```python
@strawberry.federation.type(keys=["id"])
class UserType:
    id: strawberry.ID
    name: str
```

The **Product service** doesn't import from the User service. Instead, it declares a stub `UserType` and references it:

```python
@strawberry.federation.type(keys=["id"])
class UserType:
    id: strawberry.ID = strawberry.federation.field

@strawberry.federation.type(keys=["id"])
class ProductType:
    id: strawberry.ID
    name: str

    @strawberry.field
    def created_by(self) -> typing.Optional[UserType]:
        return UserType(id=self._created_by)
```

When a client queries `product { createdBy { name } }` through the Gateway:
1. The Gateway sends the product query to the **Product service**, which returns `createdBy: { id: 1 }`
2. The Gateway recognizes `UserType` is owned by the **User service** and sends a `_entities` lookup with `{ __typename: "UserType", id: 1 }`
3. The **User service** resolves the full user via `resolve_reference` and returns `{ id: 1, name: "Admin" }`
4. The Gateway merges the results and returns the complete response to the client

This is the power of federation — **services stay decoupled while the graph stays unified**.

## Tech Stack

- **Gateway**: Node.js, Apollo Gateway, Apollo Server
- **Microservices**: Python 3.13, FastAPI, Strawberry GraphQL (Federation 2)
- **Database**: SQLAlchemy + Alembic (SQLite)
- **DI Container**: dependency-injector + pydantic-settings
- **Package Manager**: uv
- **Infrastructure**: Docker Compose

## Getting Started

### Prerequisites

- Docker and Docker Compose

### Installation

1. Clone the repository:

```bash
git clone https://github.com/nietzscheson/microservices-federation
cd microservices-federation
```

2. Build and start all services:

```bash
make
```

3. Verify containers are running:

```bash
make ps
```

```
Container user      Running (healthy)   0.0.0.0:5001->5000/tcp
Container product   Running (healthy)   0.0.0.0:5002->5000/tcp
Container order     Running (healthy)   0.0.0.0:5003->5000/tcp
Container gateway   Running             0.0.0.0:4000->80/tcp
```

4. Apply database migrations:

```bash
make upgrade
```

5. (Optional) Load sample data:

```bash
make fixtures
```

### Endpoints

| Endpoint | URL |
|----------|-----|
| Unified Graph (Gateway) | [localhost:4000/graphql](http://localhost:4000/graphql) |
| User Service | [localhost:5001/graphql](http://localhost:5001/graphql) |
| Product Service | [localhost:5002/graphql](http://localhost:5002/graphql) |
| Order Service | [localhost:5003/graphql](http://localhost:5003/graphql) |

### Try a federated query

Open [localhost:4000/graphql](http://localhost:4000/graphql) and run:

```graphql
query {
  products {
    id
    name
    createdBy {
      id
      name
    }
  }
}
```

This single query hits the **Product service** for products and the **User service** for the `createdBy` user — composed transparently by the Gateway.

## Development

### Run tests

```bash
make test
```

Run tests for a single service:

```bash
make test.user
make test.product
make test.order
```

### Database migrations

Apply migrations:

```bash
make upgrade
```

Generate a new migration after modifying models:

```bash
make migrate
```

### Project structure

```
.
├── gateway/                    # Apollo Gateway (Node.js)
│   ├── server.js
│   ├── package.json
│   └── Dockerfile
├── services/
│   ├── Dockerfile              # Multi-stage build for all Python services
│   ├── user/
│   │   ├── pyproject.toml      # Dependencies (managed by uv)
│   │   ├── alembic.ini
│   │   ├── src/
│   │   │   ├── app.py          # FastAPI app, models, GraphQL schema
│   │   │   ├── settings.py     # pydantic-settings configuration
│   │   │   ├── containers.py   # dependency-injector container
│   │   │   └── database.py     # SQLAlchemy Base
│   │   ├── migrations/
│   │   └── tests/
│   ├── product/                # Same structure as user
│   └── order/                  # Same structure as user
├── docker-compose.yaml
└── Makefile
```
