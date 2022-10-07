FROM --platform=linux/arm/v7 arm32v7/python:3.9.14

WORKDIR /app

COPY *.txt /app/
RUN pip install -r requirements.txt \
    && rm /app/requirements.txt

COPY *.py /app/

RUN chmod +x /app/mqtt_forwarder.py

ENV MQTT_HOST="172.16.2.10" \
    MQTT_USER="mqtt" \
    MQTT_PWD="this-wont-work" \
    MQTT_DEST_BASE="hubitat/34-e1-d1-80-0c-f2-000d" \
    MQTT_SOURCE_TOPIC="homebridge/myq/CG083017EDB7/#" \
    MQTT_FORWARDER_HASHMAP='{ "garagedoor": "mqtt-garage-door-821/cmd/switch" }' \
    MQTT_MESSAGE_REPLACE_MAP='{ "garagedoor": { "closed": "on", "open": "off" } }'

ENTRYPOINT ["python3", "-u", "/app/mqtt_forwarder.py"]
