FROM python:3.9
LABEL maintainer="s@mck.la"
ARG MY_APP_PATH=/opt/mimecast-ttp-url-monitor

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ntp \
    && mkdir -p ${MY_APP_PATH}/data

ADD main.py auth.py requirements.txt ${MY_APP_PATH}
#COPY data ${MY_APP_PATH}/data
RUN pip install requests 
# -r ${MY_APP_PATH}/requirements.txt
#RUN pip3 install fastapi uvicorn[standard] qrcode[pil] requests
WORKDIR ${MY_APP_PATH}


VOLUME [${MY_APP_PATH}]

ENTRYPOINT python -u main.py


EXPOSE 8000/tcp
