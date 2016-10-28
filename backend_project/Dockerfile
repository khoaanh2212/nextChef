FROM python:2.7.11

RUN mkdir /code
WORKDIR /code
ADD requirements /code/requirements
RUN pip install -r /code/requirements/local.txt
RUN pip install -r /code/requirements/test.txt

ARG SSH_DEVELOPER_INSTALLED=0
RUN if [ $SSH_DEVELOPER_INSTALLED -eq 1 ]; then \
    apt-get update && apt-get install openssh-server -y --no-install-recommends && apt-get clean all && \
    ssh-keygen -A && \
    sed -ri 's/^#?PermitRootLogin[[:space:]].*$/PermitRootLogin yes/g' /etc/ssh/sshd_config && \
    echo 'root:developer' | chpasswd && \
    mkdir -p /var/run/sshd \
;fi

RUN mkdir /var/tmp/django_cache

EXPOSE 8000
ENV PYTHONUNBUFFERED 1
VOLUME ["/code/backend"]
ADD . /code