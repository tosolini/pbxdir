FROM node:25-alpine AS build

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .
RUN npm run build

FROM python:3.11-alpine

WORKDIR /app

COPY --from=build /app/dist ./dist

EXPOSE 3000

CMD ["python", "-m", "http.server", "3000", "--directory", "dist", "--bind", "0.0.0.0"]
