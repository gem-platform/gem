FROM gem-server:latest

# make shared folder for files
RUN mkdir -p /usr/shared/media

WORKDIR /usr/src/app
COPY ./requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .

CMD [ "python", "main.py" ]
