FROM node:latest

WORKDIR /app

COPY package*.json /app

# Install dependencies
RUN npm i

# Copy app source
COPY . /app

EXPOSE 3000

#CMD ["npm", "run", "start"]
