FROM gem-server:latest


WORKDIR /usr/src/app
COPY ./requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .

CMD [ "python", "-u", "/usr/src/gem-server-common/_runner.py" ]