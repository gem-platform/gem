FROM gemplatform/gem-server:latest


WORKDIR /usr/src/app
COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 5000

CMD [ "python", "-u", "main.py" ]