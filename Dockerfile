FROM python:3.11.5-alpine

#RUN adduser -D sppuser
USER root
WORKDIR /sppapp

ENV PATH="/root/.local/bin:${PATH}"
#ENV PYTHONUNBUFFERED 1

#COPY --chown=root:root pyproject.toml .
#COPY --chown=root:root poetry.lock .
COPY --chown=root:root src ./src
COPY --chown=root:root .env .
COPY --chown=root:root requirements.txt .

# RUN apk update
# RUN apk add make automake gcc g++ subversion python3-dev
RUN apk update && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev \
    python3-dev gfortran musl-dev make automake g++ subversion python3-dev\
    && apk add libffi-dev

# RUN pip3 install wheel --user && \
    #pip3 install --platform manylinux2010_x86_64 :none: faster_fifo
    #pip3 install poetry --user
    #pip3 install Cython --user && \
    #pip3 install --upgrade pip setuptools --user

RUN pip3 install -r requirements.txt --user

