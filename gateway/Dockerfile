FROM node:18

WORKDIR /app

COPY package.json .
RUN yarn install --ignore-engines

CMD yarn start
