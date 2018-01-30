#start the engine

from socket import *
from threading import Thread
from Crypto.PublicKey import RSA

online = True
mbuffer = []

server = socket(AF_INET, SOCK_DGRAM)
server.bind(('',0))
port = server.getsockname()[1]

client = socket(AF_INET, SOCK_DGRAM)

public, private = open("key.txt").read().split(":")
public = RSA.importKey(public)
private = RSA.importKey(private)

def listening():
	global mbuffer
	global server
	global online
	global private
	
	while online:
		mbuffer.append(private.decrypt(server.recvfrom(1024).decode()))

Thread(target=listening).start()

class Peer:
	
	def __init_(self,key,addr):
		self.key = RSA.importKey(key)
		self.address = addr
		
	def message(m):
		global client
		client.sendto(self.key.encrypt(m).encode(),addr)
		
class PeerList(list):
	
	def __init__(self,peers=None):
		super(PeerList, self).__init__()
		for p in peers:
			assert(isinstance(p,Peer))
			self.append(p)
			
	def message(self,m):
		for each s in self:
			s.message(m)
	
	def append(self,p):
		assert(isinstance(p,Peer))
		super().append(p)
		
	def insert(self,p):
		assert(isinstance(p,Peer))
		super().insert(p)

peers = PeerList()
