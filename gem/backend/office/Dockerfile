FROM gem-server:latest

# make shared folder for generated reports
RUN mkdir -p /usr/shared/downloads

# install all the requirements
WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# copy sources
COPY . .

CMD [ "gunicorn", "main:APPLICATION" ]
