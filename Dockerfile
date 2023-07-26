FROM nikolaik/python-nodejs:latest
WORKDIR /app
COPY . .

COPY requirements.txt .
RUN yarn install --production
RUN npm install -g http-server
RUN pip3 install -r requirements.txt
RUN pip3 install git+https://github.com/pygame-web/pygbag --user --upgrade
RUN python3 -m pygbag --build --port 1999 test_panda3d_cube.py
CMD ["http-server","--cors","--port","1999"] 
EXPOSE 1999