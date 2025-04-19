FROM python:3.12.10-bookworm

RUN pip install virtualenv

RUN apt-get -y update && apt-get install -y  \
gcc \
libc-dev \
libffi-dev \
python3-psycopg2 \
&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN python3 -m venv .venv
RUN . .venv/bin/activate 
#. (dot) command is POSIX-standard, source is Bash. there's no difference between the two in bash 😂

COPY ./Protocols requirements.txt ./

RUN pip install -r requirements.txt
