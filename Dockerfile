FROM nikolaik/python-nodejs:latest
WORKDIR /app
#COPY . .
COPY src/build/web/* ./

RUN yarn install --production
RUN npm install -g http-server
CMD ["http-server","--cors","--port","8001"] 
EXPOSE 8001
