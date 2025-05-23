# Stage 1: Build the Vue.js application
FROM node:18-alpine AS build-stage

RUN yarn config set registry https://registry.npmmirror.com

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock)
COPY package*.json ./
# If using yarn, it would be:
# COPY yarn.lock ./ 
# COPY package.json ./

# Install dependencies
RUN npm install
# If using yarn:
# RUN yarn install

# Copy the rest of the application code
COPY . .

# Build the application for production
RUN npm run build
# If using yarn:
# RUN yarn build

# Stage 2: Serve the built application using Nginx
FROM nginx:stable-alpine

# Copy the built assets from the build stage
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Copy a custom Nginx configuration file (optional, but good for SPA routing)
# If not provided now, Nginx will use its default config.
# For a Vue SPA, a custom config is needed to handle client-side routing.
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 for Nginx
EXPOSE 80

# Command to start Nginx
CMD ["nginx", "-g", "daemon off;"]
