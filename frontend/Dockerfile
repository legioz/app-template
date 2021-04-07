# estágio de compilação
FROM node:lts-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
ARG FRONTEND_ENV=production
ENV VUE_APP_ENV=${FRONTEND_ENV}
RUN npm run build

# estágio de produção
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]