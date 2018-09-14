FROM gem-server:latest

# make shared folder for generated reports
RUN mkdir -p /usr/shared/downloads

# install all the requirements
WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy sources
COPY . .

EXPOSE 5001

# CMD gunicorn --bind 0.0.0.0:5001 main:app
CMD [ "python", "-u", "/usr/src/gem-server-common/_runner.py" ]
