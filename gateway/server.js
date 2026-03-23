const { ApolloServer } = require("@apollo/server");
const { startStandaloneServer } = require("@apollo/server/standalone");
const { ApolloGateway, IntrospectAndCompose } = require("@apollo/gateway");

const gateway = new ApolloGateway({
    supergraphSdl: new IntrospectAndCompose({
        subgraphs: [
            { name: "users", url: "http://user:5000/graphql" },
            { name: "products", url: "http://product:5000/graphql" },
            { name: "orders", url: "http://order:5000/graphql" },
        ],
    }),
});

const server = new ApolloServer({
    gateway,
    plugins: [],
});

startStandaloneServer(server, {
    listen: { port: 80 },
    context: async ({ req }) => ({ req }),
}).then(({ url }) => {
    console.log(`🚀 Server ready at ${url}`);
});
