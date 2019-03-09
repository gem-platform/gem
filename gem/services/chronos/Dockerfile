FROM gem-server:latest


# Install dependencies
COPY requirements.txt /usr/app/requirements.txt
RUN apt-get install -y cron rsyslog && \
    pip3 install --no-cache-dir -r /usr/app/requirements.txt

# Copy scripts
ADD . /usr/app
RUN chmod a+x /usr/app/1min/deadline.py && \
    chmod a+x /usr/app/entrypoint.sh

# Copy crontab
COPY crontab /etc/crontab

# Run
ENTRYPOINT [ "/usr/app/entrypoint.sh" ]
