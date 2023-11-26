# Step 1: Build the application
FROM node:20 AS builder
WORKDIR /app

# Install python and java for api generation
RUN apt-get update && apt-get install -y default-jre

COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

COPY . .
RUN yarn run generateAPI
RUN yarn run build

# Step 2: Set up the production environment
FROM nginx:stable-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]