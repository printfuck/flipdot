import paho.mqtt.client as mqtt
import sys

mqtc = mqtt.Client()


def pixel( x,y,color):
	mqtc.publish("foobar/flipdot/pixel", "{\"color\":\"" + color + "\",\"x\":" + str(x) + ",\"y\":" + str(y) + "}" )

def clear(color):
	mqtc.publish("foobar/flipdot/clear", color)
	time.sleep(5)

if(__name__ == "__main__"):
   mqtc.connect("10.42.0.244", 1883, 60)
   width = sys.argv[2]
   height = sys.argv[3]
   x_offset = sys.argv[0]
   y_offset = sys.argv[1]
   color = sys.argv[4]
   
   for i in range(0, width):
      for j in range(0, height):
          pixel(i+ xoffset, j + y_offset, color)

