FROM tiangolo/node-frontend:10 as builder

ADD ./src /app/src
COPY package*.json /app/
COPY ./public /app/public
WORKDIR /app
RUN npm install

ARG AUTH_APP_URL="https://tabulations.ecdev.opensource.lk"
ARG TABULATION_API_URL="https://apim-gateway.ecdev.opensource.lk/tabulation/0.1.0"

ENV REACT_APP_AUTH_APP_URL=$AUTH_APP_URL
ENV REACT_APP_TABULATION_API_URL=$TABULATION_API_URL
ENV REACT_APP_DEBUG=true
ENV REACT_APP_TABULATION_API_PAGINATION_LIMIT=250
ENV REACT_APP_USE_PDF_SERVICE=true

RUN npm run build

FROM nginx:1.15

COPY --from=builder /app/build/ /usr/share/nginx/html
COPY --from=builder /nginx.conf /etc/nginx/conf.d/default.conf
WORKDIR /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"];
# CMD echo 'window._env_ = {}; window._env_.API_BASE ="'${API_BASE}'"' > env-config.js && nginx -g 'daemon off;'
# CMD ["bash", "-c", "echo 'window._env_.API_BASE = \"$API_BASE\"' > env-config.js && nginx -g 'daemon off;'"]
# CMD echo ${API_BASE}
