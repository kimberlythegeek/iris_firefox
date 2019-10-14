FROM kimberlythegeek/iris:latest
MAINTAINER Kimberly Sereduck <ksereduck@mozilla.com>

WORKDIR /iris_firefox
COPY . /iris_firefox


ENV IRIS_CODE_ROOT /iris_firefox
ENV PYTHONPATH /iris_firefox
RUN rm -rf /tmp/.X99-lock && \
    Xvfb :99 -screen 0 1920x1080x24+32 +extension GLX +extension RANDR &> xvfb.log && \
    iris firefox -n -i DEBUG
