#!/usr/bin/env python3

import os, re, time, json, argparse, signal
import paho.mqtt.client as mqtt # pip install paho-mqtt
import urllib.parse

verbose = False

CONNECTION_RETURN_CODE = [
    "connection successful",
    "incorrect protocol version",
    "invalid client identifier",
    "server unavailable",
    "bad username or password",
    "not authorised",
]

def parseArgs():
  parser = argparse.ArgumentParser(description='Send MQTT payload received from a topic to firebase.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument('-m', '--mqtt-host',   dest='host',        action="store",       help='Specify the MQTT host to connect to.',                         **environ_or_required('MQTT_HOST'))
  parser.add_argument('-u', '--username',    dest='username',    action="store",       metavar="USERNAME",     help='MQTT boroker login username',          **environ_or_required('MQTT_USER'))
  parser.add_argument('-p', '--password',    dest='password',    action="store",       metavar="$ECRET",       help='MQTT boroker login password',          **environ_or_required('MQTT_PWD'))
  parser.add_argument('-P', '--port',        dest='port',        action="store",       type=int,               default=1883,                                metavar=1883, help='MQTT boroker port')
  parser.add_argument('-a', '--hash-map',    dest='hashMap',     action="store",       help='Specify the map of MQTT topics to forward.',                   **environ_or_required('MQTT_FORWARDER_HASHMAP'))
  parser.add_argument('-n', '--dry-run',     dest='dryRun',      action="store_true",  default=False,          help='No data will be sent to the MQTT broker.')
  parser.add_argument('-d', '--destination', dest='destination', action="store",       help='The destination MQTT topic base.',                             **environ_or_required('MQTT_DEST_BASE'))
  parser.add_argument('-t', '--topic',       dest='topic',       action="store",       help='The listening MQTT topic.',                                    **environ_or_required('MQTT_SOURCE_TOPIC'))
  parser.add_argument('-v', '--verbose',     dest='verbose',     action="store_false", default=True,           help='Enable debug messages.')

  return parser.parse_args()

def signal_handler(signal, frame):
  print('You pressed Ctrl+C!')
  client.disconnect()

def environ_or_required(key):
  if os.environ.get(key):
    return {'default': os.environ.get(key)}
  else:
    return {'required': True}

def debug(msg):
  if verbose:
    print (msg)

def on_connect(client, userdata, flags, rc):
  debug("Connected with result: " + CONNECTION_RETURN_CODE[rc] if rc < len(CONNECTION_RETURN_CODE) else rc)

  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
  client.subscribe(args.topic)

def on_message(client, userdata, msg):
  sensorName = msg.topic.split('/') [-1]
  if sensorName in hashMap.keys():
    tstamp = int(time.time())
    mqttPath = urllib.parse.urljoin(args.destination + '/', hashMap[sensorName])
    debug("Received message from {0} with payload {1} to be published to {2}".format(msg.topic, str(msg.payload), mqttPath))
    nodeData = msg.payload
    ##newObject = json.loads(nodeData.decode('utf-8'))
    ##newObject['time'] = tstamp
    ##nodeData = json.dumps(newObject)
    if not args.dryRun:
      debug("Sending message...")
      client.publish(mqttPath, nodeData)
    else:
      debug("Dry run")
  else:
    debug("Received message from {0} with payload {1}. Hash not found in hashMap".format(msg.topic, str(msg.payload)))

if __name__ == '__main__':
  args = parseArgs()

  signal.signal(signal.SIGINT, signal_handler)
  signal.signal(signal.SIGTERM, signal_handler)

  verbose = args.verbose
  hashMap = json.loads(args.hashMap)

  client = mqtt.Client()
  client.on_connect = on_connect
  client.on_message = on_message

  if args.username is not None:
      client.username_pw_set(args.username, password=args.password)
  elif args.password is not None:
      raise Exception('Login with password requires username.')
  client.connect(host=args.host, port=args.port, keepalive=60)

  client.loop_forever()
