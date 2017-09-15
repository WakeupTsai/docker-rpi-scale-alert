import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import os
  
TOPIC = os.environ['TOPIC']
BROKER = os.environ['BROKER']

def alert(msg):
  obj = json.loads(str(msg.payload))
  print("msg.value: "+ str(obj['d']['value']))
  try:
    print("msg.geotag: "+ str(obj['d']['geotag']))
    
    # alert message
    data = {}
    data['event'] = 'motion'
    data['geotag'] = str(obj['d']['geotag'])
    json_data = json.dumps(data)

    publish.single('alert', json_data, qos=1, hostname=BROKER)

  except:
    pass
  

def on_connect(client, userdata, flags, rc):
  client.subscribe(TOPIC)

def on_message(client, userdata, msg):
  obj = json.loads(str(msg.payload))
  if obj['d']['value']==1:
    alert(msg)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883, 60)

client.loop_forever()
