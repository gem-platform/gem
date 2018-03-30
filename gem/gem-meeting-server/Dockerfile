FROM gemplatform/gem-server:latest


WORKDIR /usr/src/app
COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8090

CMD [ "python", "-u", "/usr/src/tools/_runner.py" ]