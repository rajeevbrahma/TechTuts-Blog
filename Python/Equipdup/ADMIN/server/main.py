import ast
import paho.mqtt.client as mqtt
import logging
import ConfigParser
from Savoir import Savoir
import simplejson as json
import logging
import uuid
from twilio.rest import Client


LOG_FILENAME = 'LogFiles/main.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,format='%(asctime)s, %(levelname)s, %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


class Multichainpython:

	def __init__(self,rpcuser,rpcpasswd,rpchost,rpcport,chainname):
		self.rpcuser = rpcuser
		self.rpcpasswd = rpcpasswd
		self.rpchost = rpchost
		self.rpcport = rpcport
		self.chainname = chainname

	def multichainConnect(self):
		try:
			# The api connection 
			self.api = Savoir(self.rpcuser, self.rpcpasswd, self.rpchost, self.rpcport, self.chainname)
			return self.api
		except Exception as e:
			logging.error("The multichainConnect error %s,%s"%(e,type(e)))
			return False
	def gettotalbalances(self):
		try:
		    totalbalances = self.api.gettotalbalances()
		    return totalbalances
		except Exception as e:
		    print e
		    return False

	def sendAsset(self,assetaddress,assetname,assetquantity):
		try:
			sendasset = self.api.sendassettoaddress(assetaddress,assetname,assetquantity)
			return sendasset
		except Exception as e:
			print e,"\t send assetaddress issue"
			logging.error("The sendAsset error %s,%s"%(e,type(e)))			
			return False
	
	# - ------- - - - - - -- Following functions are for querying the asset ---- - - - - 
	
	def subscribeToasset(self,assetname):
		try:
			subscrbtoasst = self.api.subscribe(assetname)
			return subscrbtoasst
		except Exception as e:
			logging.error("The subscribeToasset error %s,%s"%(e,type(e)))
			return False	
	def queryAssetTransactions(self,assetname):
		try:
			queryassttrans = self.api.listassettransactions(assetname)
			return queryassttrans 
		except Exception as e:
			logging.error("The queryAssetTransactions error %s,%s"%(e,type(e)))		 
			return False
	
	def queryassetsdetails(self,assetname):
		try:
			assetdetails = self.api.listassets(assetname,True) # Here True is for fetching full details its called verbose
			return assetdetails
		except Exception as e:
			logging.error("The queryassetdetails error %s,%s"%(e,type(e)))		

	def queryassets(self):
		try:
			assets = self.api.listassets() # Here True is for fetching full details its called verbose
			return assets
		except Exception as e:
			logging.error("The queryassets error %s,%s"%(e,type(e)))			


class MQtt:
	def __init__(self,host,port,subTopic,pubTopic,mc_conn,mc,tw,timealive=60):
		self.host = host
		self.port = port
		self.timealive = timealive
		self.payload = None
		self.subTopic = subTopic
		self.pubTopic = pubTopic
		self.mc_conn = mc_conn
		self.tw = tw
		self.mc = mc


	def assetTrx(self):
		asset = mc.queryassets()
		assets = []

		for val in asset:
			assets.append(val["name"])

		# print assets

		assetTaken = {}

		i=1	

		for ass in assets:		
			retrnVal = mc.queryAssetTransactions(ass)
			if(len(retrnVal)>1):		
				for key in retrnVal[-1]["addresses"]:
					if retrnVal[-1]["addresses"][key] == 1:
						for user in USER_DATA:
							if key  == USER_DATA[user]["walletAddress"]:
								assetTaken.update({i:{"user":user,"asset":ass}})
								i+=1
		print assetTaken
		return assetTaken	
	

	def __on_connect(self,client, userdata, flags, rc):
		try:
			print "Connected with result code "+str(rc)
			if self.subTopic!=None:
				(result,mid)= client.subscribe(self.subTopic)
				print result
		except Exception as e:
			logging.error("The on_connect error %s,%s"%(e,type(e)))

	def __on_message(self,client, userdata, msg):
		try:			
			data = msg.payload
			print data,"RAW DATA"
			message = ast.literal_eval(data)
			self.payload = message
			print self.payload,"EVERY PAYLOAD"
			if (self.payload["type"] == "REQ"):

				if (self.payload["op"] == "LOGIN"):
					assetbalances = self.mc_conn.gettotalbalances()
					username = self.payload["details"]["username"]
					password = self.payload["details"]["password"]

					if (username == USER_DATA[username]["username"] and password == USER_DATA[username]["password"]):
						message = {"sender":"SERVER","type":"RESP","op":"LOGIN","details":{"returnVal":0},"payload":assetbalances}
					else:
						message = {"sender":"SERVER","type":"RESP","op":"LOGIN","details":{"returnVal":1}}

				elif(self.payload["op"] == "OTP"):
					print "ELIF"
					otp = str(uuid.uuid4())[:4]
					print otp,"\nOTP"
					messagetoUser = "OTP to receive the Asset"+self.payload["details"]["asset"]+", from "+self.payload["details"]["sender"]+"is "+otp	
					message = {"sender":"SERVER","type":"RESP","op":"OTP","details":{"otp":otp}}
					print message,messagetoUser,"\nMESSAGE,MESSAGETOUSER"
					# tw.send(USER_DATA[self.payload["details"]["receiver"]]["mobile"],messagetoUser)

				elif(self.payload["op"] == "SND-AST"):
					self.mc.sendAsset(USER_DATA[self.payload["details"]["receiver"]]["walletAddress"],self.payload["details"]["asset"],1)
					assetTakenmessage = self.assetTrx()
					assetbalances = self.mc_conn.gettotalbalances()
					message = {"sender":"SERVER","type":"RESP","op":"AST-TKN","details":{"ast-tkn":assetTakenmessage,"ast-bal":assetbalances}}
					
				elif(self.payload["op"] == "AST-TKN"):
					assetTakenmessage = self.assetTrx()
					assetbalances = self.mc_conn.gettotalbalances()
					message = {"sender":"SERVER","type":"RESP","op":"AST-TKN","details":{"ast-tkn":assetTakenmessage,"ast-bal":assetbalances}}
							

				else:
					pass	

			print message		
			self.send(json.dumps(message))

			


		except Exception as e:
			logging.error("The on_message error %s,%s"%(e,type(e)))	 	


	def connect(self):
		try:
			self.mqttc = mqtt.Client()
			self.mqttc.on_connect = self.__on_connect
			self.mqttc.on_message = self.__on_message
			self.mqttc.connect(self.host,self.port,self.timealive)
			
			if self.subTopic != None:
				print "Hu"				
				self.mqttc.loop_start()
				self.mqttc.loop_forever()
			
		except Exception as e:
			logging.error("The connect error %s,%s"%(e,type(e)))	
		
	
	def send(self,message):
		try:
			(result,mid) = self.mqttc.publish(self.pubTopic,message,2)
			return result
		except Exception as e:
			print e
			logging.error("The send error %s,%s"%(e,type(e)))
		
class TWilio:
	def __init__(self,sid,from_num,authToken):
		self.account_sid = sid
		self.auth_token  = authToken
		self.from_num = from_num
	def connect(self):
		try:		
			self.client = Client(self.account_sid, self.auth_token)
			return self.client
		except Exception as e:
			logging.error("The connect error %s,%s"%(e,type(e)))
				
	def send(self,to,message):
		try:
			msg = self.client.messages.create(to=to, from_=self.from_num,body=message)
			return msg
		except Exception as e:
			logging.error("The send error %s,%s"%(e,type(e)))	
		

if __name__ == '__main__':
	
	USER_DATA = {
				"thub":{"walletAddress":"","username":"thub","password":"123","mobile":"+919550119531"},
				"3892":{"walletAddress":"","username":"3892","password":"123","mobile":"+919550119531"},
				"783":{"walletAddress":"","username":"783","password":"123","mobile":"+918985833200"},
				}
	


	filename = "config.ini"
	cf = ConfigParser.ConfigParser()
	cf.read(filename)

	# TWILIO DETAILS
	account_sid = cf.get("Twilio","sid")
	auth_token  = cf.get("Twilio","authToken")	
	twilionumber = cf.get("Twilio","from")

	tw = TWilio(account_sid,twilionumber,auth_token)
	tw_conn = tw.connect()

	# MULTICHAIN DETAILS
	rpcuser = cf.get("Multichain","rpcuser")
	rpcpasswd = cf.get("Multichain","rpcpasswd")
	rpchost = cf.get("Multichain","rpchost")
	rpcport = cf.get("Multichain","rpcport")
	chainname = cf.get("Multichain","chainname")
	mc = Multichainpython(rpcuser,rpcpasswd,rpchost,rpcport,chainname)
	mc_conn = mc.multichainConnect()

	# MQTT DETIALS
	host = cf.get("Mqtt","host")
	port = cf.get("Mqtt","port")
	subTopic = cf.get("Mqtt","subTopic")
	pubTopic = cf.get("Mqtt","pubTopic")

	mq = MQtt(host,port,subTopic,pubTopic,mc_conn,mc,tw)			
	mq.connect()


	

