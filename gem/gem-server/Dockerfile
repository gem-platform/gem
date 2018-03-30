FROM python:3

# install basic requirements
WORKDIR /usr/src/app
COPY ./gem-server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# install gem's requirements
WORKDIR /usr/src/libs/gem-lib-core
COPY ./gem-lib-core .
RUN pip install --no-cache-dir .

WORKDIR /usr/src/libs/gem-lib-database
COPY ./gem-lib-database .
RUN pip install --no-cache-dir .

# Do not copy into /usr/src/app folder, because it can
# be overwriten by mounted volume
# volumes: - ./gem/gem-meeting-server:/usr/src/app
WORKDIR /usr/src/tools
COPY ./gem-server .

# well done
CMD [ "true" ]