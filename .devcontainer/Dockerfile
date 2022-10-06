# syntax=docker/dockerfile:1

FROM python:3.9.14

RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt update \
    && apt install gh git git-lfs python3-paho-mqtt nano -y

##WORKDIR /app
##VOLUME [ "/repo" ]
##COPY content/. /app/
##RUN pip install -r requirements.txt

ENV GIT_SSL_NO_VERIFY=true
