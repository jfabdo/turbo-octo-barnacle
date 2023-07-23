FROM nikolaik/python-nodejs:latest
WORKDIR /app
COPY . .
RUN yarn install --production
RUN /app/setup.sh
RUN pip3 install -r requirements.txt
CMD ["http-server"]
EXPOSE 80
EXPOSE 1999