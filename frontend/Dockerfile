FROM node:latest

WORKDIR /app

COPY . /app

RUN npm i
RUN npm run build
RUN npm i -g serve

EXPOSE 3000

#CMD ["npm", "run", "start"]
