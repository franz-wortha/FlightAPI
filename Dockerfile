FROM node:24-alpine

WORKDIR /app

# Install dependencies first
COPY package*.json ./
RUN npm install

# Copy rest of project
COPY . .

EXPOSE 1337

CMD ["npm", "run", "develop"]
