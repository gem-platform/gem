FROM gem-server:latest

RUN apt-get install -y cron

# Install python3 to run scripts
COPY requirements.txt /usr/app/requirements.txt
RUN pip3 install --no-cache-dir -r /usr/app/requirements.txt

# Copy scripts
COPY templates templates
COPY /15min/deadline.py /etc/periodic/15min/deadline
RUN chmod a+x /etc/periodic/15min/deadline

#
CMD [ "cron", "-f" ]
