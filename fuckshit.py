import serial
import time
import json
import paho.mqtt.client as mqt
size_index = {"small" : b"S", "medium": b"M", "large" : b"L"}
working = False



def on_connect(mosq, obj, foo ,bar ):
	print( "Connected" )

def on_message(mosq, obj, msg):
 	global working
	if working is True:
		return
	working = True
	if msg.topic.find("text") > 0:
		getText(msg.payload)
	elif msg.topic.find("clear") > 0:
		clear(msg.payload)
	elif msg.topic.find("pixel") > 0:
   		setPixel(msg.payload)
	elif msg.topic.find("horizontal") > 0:
   		hline(msg.payload)
	elif msg.topic.find("vertical") > 0:
   		vline(msg.payload)
	elif msg.topic.find("rect") > 0:
   		rect(msg.payload)
	se.reset_input_buffer()
	working = False

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed OK")

#
# { "color": "B", "x": 0, "y": 0, "size": "small", "text": "My messeage" } Black 
# { "color": "Y", "x": 0, "y": 0, "size": "medium", "text": "My messeage" } Yellow
# { "color": "Y", "x": 0, "y": 0, "size": "large", "text": "My messeage" } Yellow
#

def getText(msg):
	buffer = msg
	try:
		obj = json.loads(buffer)
		se.write(b"P," + bytes(obj["color"], "utf-8") + b"," + bytes(str(obj["x"]), "utf-8") + b"," + bytes(str(obj["y"]), "utf-8") + b"," + size_index[obj["size"]] + b"," + bytes(obj["text"], "utf-8") + b"\\")
	except:
        	return

#
# { "color": "B", "x": 0, "y": 0 } Black 
# { "color": "Y", "x": 0, "y": 0 } Yellow
#

def setPixel(msg):
	try:
		print("Pixel Set")
		obj = json.loads(msg)
		se.write(b"S," + bytes(str(obj["color"]), "utf-8" ) + b"," + bytes(str(obj["x"]),"utf-8")  + b"," + bytes(str(obj["y"]), "utf-8") + b",\\")
	except:
		return

def rect(msg):
	try:
		print("Rect Set")
		obj = json.loads(msg)
		x = obj["x"]
		y = obj["y"]
		width = obj["width"]
		height = obj["height"]
		color = bytes(obj["color"], "utf-8")
		for i in range(0,width):
			for j in range(0,height):
				pixel(i+x, j+y, color)
	except:
		return

#
# Message contains integer value
#

def clear(msg):
	try:
		buffer = msg #.decode("utf-8")
		if len(buffer) == 1:
			se.write(b"C," + buffer + b"\\")
	except:
		return

#
#
#

def vline(msg):
	buffer = msg #decode("utf-8")
	try:
        	obj = json.loads(msg)
        	se.write(b"V," + bytes(obj["color"], "utf-8") + b"," + bytes(str(obj["value"]), "utf-8") + b"\\")
	except:
		return

# 
# { "color": "Y", "value": 0 } Yellow
#

def hline(msg):
	buffer = msg #decode("utf-8")
	try:
		obj = json.loads(msg)
		se.write(b"H," + bytes(obj["color"], "utf-8") + b"," + bytes(str(obj["value"]), "utf-8") + b"\\")
	except:
		return

def pixel( x,y,color):
        se.write(b"S," + color + b"," + bytes(x,"utf-8")  + b"," + bytes(y, "utf-8") + b",\\")

# Set callbacks
if __name__ == '__main__':
        global se
        mqtc = mqt.Client()
        mqtc.connect("mqtt.chaospott.de", 1883, 60)
        mqtc.subscribe("foobar/flipdot/text", 0)
        mqtc.subscribe("foobar/flipdot/clear", 0)
        mqtc.subscribe("foobar/flipdot/horizontal", 0)
        mqtc.subscribe("foobar/flipdot/vertical", 0)
        mqtc.subscribe("foobar/flipdot/pixel", 0)
        mqtc.subscribe("foobar/flipdot/rect", 0)

        mqtc.on_message = on_message
        mqtc.on_connect = on_connect
        mqtc.on_subscribe = on_subscribe
        s = serial.Serial()
        #print(serial.tools.list_ports())
        s.port = '/dev/ttyUSB0'
        s.baudrate = 115200
        s.open()
        while not s.is_open:
                time.sleep(1)
        se = s
        mqtc.loop_forever(timeout=1.0, max_packets=1, retry_first_connection=False)

        s.close()
