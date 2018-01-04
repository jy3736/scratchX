#----------------------------------------------------
import time
import serial.tools.list_ports as port_list
import serial
    
#----------------------------------------------------
from flask import Flask
app = Flask(__name__)

#----------------------------------------------------
Arduino_VID = "2341"

#----------------------------------------------------
def get1stArduino():
  for p in port_list.comports():
    p=list(p)
    if Arduino_VID in p[-1]:
      return p[0]
  return None

#----------------------------------------------------
@app.route("/")
def hello():
  return "Hello World!"

#----------------------------------------------------
@app.route("/arduino")
def _get1stArduino():
  port=get1stArduino()
  if port: 
    return port
  return "No Arduino device found!"

#----------------------------------------------------
@app.route("/cmd/M/<int:act>")
def _cmdM(act):
  p=get1stArduino()
  if p:
    ser = serial.Serial(p,9600)
    if ser:
      cmd="#M"+str(act)
      ser.write(cmd.encode())     
      print(ser.name," : ",cmd)         
      ser.close()
      return "Success : "+cmd   
  return "Failure"

#----------------------------------------------------
@app.route("/send/<msg>")
def _send(msg):
  p=get1stArduino()
  if p:
    ser = serial.Serial(p,9600)
    if ser:
      ser.write(msg.encode())     
      print(ser.name," : ",msg)         
      ser.close()
      return "Success : " + msg   
  return "Failure"

#----------------------------------------------------
@app.route("/ports")
def getports():
  ret=""
  for p in port_list.comports():
    p=list(p)
    ret+=p[0]+ " : " + p[-1] + "<br>\n"
  return ret

#----------------------------------------------------
if __name__=='__main__':
  app.run(host="0.0.0.0",port=5000)