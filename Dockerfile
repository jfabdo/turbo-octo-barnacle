FROM nikolaik/python-nodejs:latest
WORKDIR /app
COPY src/build/web/* ./

RUN mkdir archives
RUN git clone --depth 1 https://github.com/pygame-web/archives archives
RUN chmod -R a+r archives

RUN yarn install --production
RUN npm install -g http-server
CMD ["http-server","--cors","--port","8000"] 
EXPOSE 8000
