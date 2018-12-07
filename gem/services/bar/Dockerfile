FROM gem-server:latest

# make shared folder for images
RUN mkdir -p /usr/shared/downloads

# copy requirements.txt
WORKDIR /usr/src/app
COPY ./requirements.txt ./

# install requirements
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .

# run
CMD [ "python", "main.py" ]