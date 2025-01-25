# Frontend Dockerfile
FROM node:18

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install 
RUN npm install react-scripts


COPY . .

CMD ["npm", "start"]
