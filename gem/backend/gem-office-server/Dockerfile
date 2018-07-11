FROM gemplatform/gem-server:latest

RUN mkdir -p /usr/shared/downloads
WORKDIR /usr/src/app
COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 5001

# CMD gunicorn --bind 0.0.0.0:5001 main:app
CMD [ "python", "-u", "/usr/src/gem-server-common/_runner.py" ]
