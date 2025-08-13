FROM node:22-alpine
WORKDIR /app

COPY vite-project/package-lock.json ./
COPY vite-project/package.json ./

RUN npm install

# COPY vite-project/ ./  此行不需要因為會藉由yaml的volume來同步資料到容器中


EXPOSE 5173

CMD ["npm", "run", "dev"]
# RUN npm run build (正式上線用)