FROM python:3.8.13-alpine3.16

ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

RUN apk update
RUN apk add --no-cache git postgresql-dev gcc libc-dev
RUN apk add --no-cache gcc g++ make libffi-dev python3-dev build-base
RUN apk add py3-pip py3-pillow py3-cffi py3-brotli gcc musl-dev python3-dev pango
RUN apk add chromium
RUN apk add chromium-chromedriver
RUN apk add gettext

RUN pip install gunicorn
RUN pip install ipdb
RUN pip install ipython

WORKDIR /app

RUN git clone https://github.com/javiercavlop/decide.git .
RUN git pull
RUN echo "$(<requirements.txt)"s
RUN pip install -U pip
RUN pip install -r requirements.txt

WORKDIR /app/decide

# local settings.py
ADD docker-settings.py /app/decide/local_settings.py

RUN ./manage.py collectstatic

#CMD ["gunicorn", "-w 5", "decide.wsgi", "--timeout=500", "-b 0.0.0.0:5000"]
