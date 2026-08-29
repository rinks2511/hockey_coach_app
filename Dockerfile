FROM node:18-alpine
WORKDIR /app
COPY index.html server.js ./
EXPOSE 8080
CMD ["node", "server.js"]
