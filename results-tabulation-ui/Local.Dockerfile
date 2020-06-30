FROM node:13.10.1-alpine
ENV NODE_ENV production
WORKDIR /app
COPY package*.json /app/
COPY ./src /app/src
COPY ./public /app/public

ENV CI="true"
ENV REACT_APP_AUTH_APP_URL=http://localhost:3001
ENV REACT_APP_TABULATION_API_URL=https://localhost:8243/tabulation/0.1.0
ENV REACT_APP_DEBUG="true"
RUN npm ci
RUN npm install --silent
# RUN npm run build

EXPOSE 3000
CMD ["npm", "start"]
