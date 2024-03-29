FROM python:3.9.0

LABEL version="1.0"
LABEL autor="luizfelipevbll"

ENV DOCKER_ON=True
ENV DEBUG=True
ENV TZ="America/Sao_Paulo"

RUN date
RUN apt-get update && apt-get install -y apt-utils
RUN apt-get install -y gcc \
    zlibc \
    zlib1g-dev \
    libssl-dev \
    libbz2-dev \
    libsqlite3-dev \
    libncurses5-dev \
    libgdbm-dev \
    libgdbm-compat-dev \
    liblzma-dev \
    libreadline-dev \
    libffi-dev \
    uuid-dev \
    apt-transport-https \
    ca-certificates \
    man \
    curl \
    wget \
    vim \
    nano \
    wget \
    gnupg2 \
    default-libmysqlclient-dev \
    build-essential \
    python3-pip \
    bash-completion \
    tree \
    neofetch \
    sqlite3 \
    libmariadb-dev \
    && apt-get autoremove -y \
    && apt-get autoclean -y


RUN mkdir -p /home/src
WORKDIR /home/src/

RUN mkdir -p /home/mail
RUN mkdir -p /home/job
RUN mkdir -p /home/upload
RUN mkdir -p /home/logs


COPY ./ /home/src

# ! Install institutional certificates
COPY ./certificates/docker_CA.crt /usr/local/share/ca-certificates/
RUN chmod 777 /usr/local/share/ca-certificates/docker_CA.crt
RUN update-ca-certificates

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt 

EXPOSE 8000
EXPOSE 80

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
