import asyncio
import websockets
import uuid
import json

from SyncModulesPython.Core.ModuleCore import ModuleCore

from SyncModulesPython.Core.ModulesRegistry import ModulesRegistry


# registry.onCommand("ADD_MODULE", {"type":"ModuleCore", "UUID":str(uuid.uuid4())})

# def onModuleMessage ( payload ):
# 	moduleUUID = uuid.UUID(payload[ "moduleUUID" ])
# 	module = registry.getModule( moduleUUID )
# 	print( moduleUUID, module )
# 	if module is not None:
# 		module.input( payload )

class ClientNetwork:
	def __init__( self ):
		print( "ClientNetwork - __init__" )
		self.websocket = None

	async def run( self ):
		while True:
			await self.listen

	async def connect ( self, url="ws://localhost", port="3000" ):
		print( f'{url}:{port}')
		self.websocket = await websockets.connect( f'{url}:{port}' )

	async def send ( self, message: str ):
		await self.websocket.send( message )

	def sendFn ( self, message ):
		asyncio.create_task( self.send(message) )

	async def receive ( self ):
		return await self.websocket.recv( )

	def onMessage ( self, message ):
		print(f'received: { message }')
		messageData = json.loads( message )
		scope = messageData[ "scope" ]
		payload = messageData[ "payload" ]
		match scope:
			case "SYSTEM":
				print("system message")
			case "MODULE":
				self.onModuleMessage( payload )

	async def listen ( self ):
		try:
			async for message in self.websocket:
				self.onMessage( message )
		except websockets.ConnectionClosed:
			print( "connection closed" )

	async def disconnect ( self ):
		if self.websocket:
			await self.websocket.close( )
			print( "disconnected" )

	def setCallbacks ( self, onModuleMessage ):
		self.onModuleMessage = onModuleMessage

# await clientNetwork.connect()
UUID = uuid.uuid4( )

async def main( ):
	clientNetwork = ClientNetwork( )
		
	def outputFn ( payload ):
		message = {
			"scope": "MODULE",
			"senderUUID": str(UUID),
			"payload": payload
		}
		print( message )
		clientNetwork.sendFn( json.dumps( message ) )

	registry = ModulesRegistry( outputFn )

	def onModuleMessage ( payload ):
		moduleUUID = uuid.UUID(payload[ "moduleUUID" ])
		module = registry.getModule( moduleUUID )
		if module is not None:
			module.input( payload )

	clientNetwork.setCallbacks( onModuleMessage )


	await clientNetwork.connect( )
	asyncio.create_task( clientNetwork.listen( ) )
	# asyncio.run(clientNetwork.run())
	print( uuid.UUID(int=0))

	message = {
		"UUID": str( UUID )
	}
	clientNetwork.sendFn( json.dumps( message ) )
	# await clientNetwork.send( json.dumps( message ) )
	await asyncio.sleep(0.5)
	
	message = {
		"scope": "SYSTEM",
		"senderUUID": str( UUID ),
		"payload": {
			"command": "INSTANCE_JOIN",
			"data": {
				"instanceUUID": str( uuid.UUID(int=0)),
				"userUUID": str( UUID )
			}
		}
	}
	clientNetwork.sendFn( json.dumps( message ) )
	await asyncio.sleep(0.5)

	# scalar = registry.addModule( "Vector3Module", uuid.UUID(int=1), True)
	# await asyncio.sleep(0.5)
	# scalar.updateVector( [1, 1, 2], True )
	# await asyncio.sleep(0.5)
	# registry.removeModule( uuid.UUID(int=1), True )
	
	while True:
		await asyncio.sleep(1)

asyncio.run( main( ) )