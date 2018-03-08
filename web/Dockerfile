FROM python:3.6.1
MAINTAINER Jackson Kontny <jackson.kontny@gmail.com>

# Create the group and user to be used in this container
# Also create the users home dir and specify bash as the shell
RUN groupadd flaskgroup && \
    useradd -m -g flaskgroup -s /bin/bash flask && \
    mkdir -p /home/flask/app/web
WORKDIR /home/flask/app/web

# Install the package dependencies (this step is separated
# from copying all the source code to avoid having to
# re-install all python packages defined in requirements.txt
# whenever any source code change is made)
COPY requirements.txt /home/flask/app/web
RUN pip install --no-cache-dir -r requirements.txt

COPY . /home/flask/app/web

RUN chown -R flask:flaskgroup /home/flask
USER flask
