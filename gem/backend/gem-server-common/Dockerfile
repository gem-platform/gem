FROM python:slim

# install basic requirements
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# install gem's requirements

# Do not copy into /usr/src/app folder, because it can
# be overwriten by mounted volume
# volumes: - ./gem/gem-meeting-server:/usr/src/app
WORKDIR /usr/src/gem-server-common
COPY . .
RUN pip install --no-cache-dir .

# well done
CMD [ "true" ]
