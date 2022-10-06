FROM --platform=linux/arm/v7 arm32v7/python:3.9.14

WORKDIR /app
COPY *.py *.txt /app/

RUN pip install -r requirements.txt

RUN chmod +x /app/mqtt_forwarder.py

ENV MQTT_HOST="172.16.2.10" \
    MQTT_USER="mqtt" \
    MQTT_PWD="A30b979f2B#8" \
    MQTT_DEST_BASE="hubitat/34-e1-d1-80-0c-f2-000d/mqtt-garage-door-819/cmd" \
    MQTT_SOURCE_TOPIC="homebridge/myq/CG083017EDB7/#" \
    MQTT_FORWARDER_HASHMAP='{ "garagedoor": "contactSensor" }'

ENTRYPOINT ["python3", "-u", "/app/mqtt_forwarder.py"]
