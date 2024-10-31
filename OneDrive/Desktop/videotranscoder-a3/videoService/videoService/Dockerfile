FROM node:18-alpine
WORKDIR /app
COPY . .
RUN yarn install --production
RUN npm i ffprobe --save
RUN apk add --no-cache ffmpeg
EXPOSE 3002
CMD ["node", "server.js"]
