# Phicomm M1 Python Plugin
#
# Author: Zack
#
"""
<plugin key="Phicomm-M1" name="Phicomm M1 Receiver" author="Zack" version="1.1.0" externallink="http://domoticz.cn/forum/">
</plugin>
"""
import Domoticz
import socket
import json
import re
import binascii

class plugin:
	serverConn = None
	clentMaps = {}
	clientConns = {}
	pattern = r"(\{.*?\})"
	brightness_hex = "aa 2f 01 e0 24 11 39 8f 0b 00 00 00 00 00 00 00 00 b0 f8 93 11 42 0e 00 3d 00 00 02 7b 22 62 72 69 67 68 74 6e 65 73 73 22 3a 22 %s 22 2c 22 74 79 70 65 22 3a 32 7d ff 23 45 4e 44 23"
	dict_value = {'0': '0', '10': '100', '20': '25'}

	# Update Device into DB
	def updateDevice(self, device, nValue, sValue):
		if device.sValue != sValue:
			device.Update(nValue=nValue, sValue=str(sValue))
			Domoticz.Log("Update "+":'" + str(nValue)+" "+str(sValue)+"' ("+device.Name+")")

	def createAndUpdateDevice(self, identity, data):
		Domoticz.Debug("Device count: " + str(len(Devices)))
		deviceTag = self.generateIdentityTag(identity)
		jsonData = self.parseJsonData(data)
		if jsonData:
			#create dimmer
			if not self.getExistDevice(deviceTag):
				Options =   {	"LevelActions"  :"||||" , 
					"LevelNames"    :"Off|On|Dark" ,
					"LevelOffHidden":"false",
					"SelectorStyle" :"0"
				}
				Domoticz.Device(Name=identity + "_Selector", Unit=len(Devices) + 1, TypeName="Selector Switch", Switchtype=18, Options=Options, DeviceID=deviceTag, Used=1).Create()

			for i in range(4):
				deviceId = deviceTag + str(i)
				sValue = jsonData[self.index_to_key(i)]
				device = self.getExistDevice(deviceId)
				if i == 3: #fix hcho value.
					sValue = float(sValue) / 1000
				if device:
					self.updateDevice(device,1, sValue)
				else:
					deviceNum = len(Devices) + 1
					Domoticz.Device(Name=identity + "_" + self.index_to_key(i),  Unit=deviceNum, TypeName="Custom", Options={"Custom":self.measure_to_str(i)}, DeviceID=deviceId, Used=1).Create()


	def generateIdentityTag(self, addr):
		identity = addr.replace('.','')
		return identity[len(identity)-8:]

	def getExistDevice(self, identity):
		for x in Devices:
			if str(Devices[x].DeviceID) == identity:
				return Devices[x]
		return None


	def parseJsonData(self,data):
		jsonStr = re.findall(self.pattern,str(data) ,re.M)
		if len(jsonStr) > 0:
			return json.loads(jsonStr[0])
		else:
			return None

	def measure_to_str(self, arg):
		keys = {
			0: "1;℃",
			1: "1;%",
			2: "1;μg/m³",
			3: "1;mg/m³",
		}
		return keys.get(arg, "null")

	def index_to_key(self, arg):
		keys = {
			0: "temperature",
			1: "humidity",
			2: "value",
			3: "hcho",
		}
		return keys.get(arg, "temperature")

	def stringToHex(self, str):
		r = ''
		hex = binascii.hexlify(str.encode()).decode('utf-8')
		for i, c in enumerate(hex):
			r = r + c
			if i % 2 == 1:
				r = r + ' '
		return r

	def genCommand(self, unit, parameter, level):
		key = Devices[unit].DeviceID
		if key in self.clientConns:
			value = self.dict_value[str(level)]
			hexCommand = self.brightness_hex%(self.stringToHex(value))
			self.clientConns[key].Send(bytes.fromhex(hexCommand))
			self.updateDevice(Devices[unit],2,level)

	def onStart(self):
		# Domoticz.Debugging(1)
		Domoticz.Heartbeat(60)
		self.serverConn = Domoticz.Connection(Name="Data Connection", Transport="TCP/IP", Protocol="line", Port="9000")
		self.serverConn.Listen()
	def onStop(self):
		Domoticz.Log("onStop called")
		if self.serverConn.Connected():
			self.serverConn.Disconnect()

	def onConnect(self, Connection, Status, Description):
		if (Status == 0):
			Domoticz.Log("Connected successfully to: "+Connection.Address+":"+Connection.Port)
		else:
			Domoticz.Log("Failed to connect ("+str(Status)+") to: "+Connection.Address+":"+Connection.Port+" with error: "+Description)

		Domoticz.Log(str(Connection))
		identityTag = self.generateIdentityTag(Connection.Address)
		self.clientConns[identityTag] = Connection

	def onMessage(self, Connection, Data, Status, Extra):
		Domoticz.Log("onMessage called for connection: "+Connection.Address+":"+Connection.Port)	
		self.createAndUpdateDevice(Connection.Address,Data)

	def onCommand(self, Unit, Command, Level, Hue):
		Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))
		
		self.genCommand(Unit, Command, Level)
		
		#

	def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
		Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

	def onDisconnect(self, Connection):
		Domoticz.Log("onDisconnect called")

	def onHeartbeat(self):
		Domoticz.Log("onHeartbeat...")

global _plugin
_plugin = plugin()

def onStart():
	global _plugin
	_plugin.onStart()

def onStop():
	global _plugin
	_plugin.onStop()

def onConnect(Connection, Status, Description):
	global _plugin
	_plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data, Status, Extra):
	global _plugin
	_plugin.onMessage(Connection, Data, Status, Extra)

def onCommand(Unit, Command, Level, Hue):
	global _plugin
	_plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
	global _plugin
	_plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
	global _plugin
	_plugin.onDisconnect(Connection)

def onHeartbeat():
	global _plugin
	_plugin.onHeartbeat()