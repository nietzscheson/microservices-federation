const { ApolloServer } = require("apollo-server");
const { ApolloGateway, IntrospectAndCompose } = require("@apollo/gateway");

const gateway = new ApolloGateway({
    supergraphSdl: new IntrospectAndCompose({
        subgraphs: [
            { name: "users", url: "http://user:5000/graphql" },
        ],
    }),
});

const cors = {
    "origin": "*",
    "methods": "GET,HEAD,PUT,PATCH,POST,DELETE",
    "preflightContinue": false,
    "optionsSuccessStatus": 204
}
const server = new ApolloServer({ cors, gateway });

server.listen(80).then(({ url }) => {
  console.log(`🚀 Server ready at ${url}`);
});
