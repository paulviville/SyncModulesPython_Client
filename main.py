import asyncio
import websockets
import uuid
import json

# from SyncModulesPython.Core.ModuleCore import ModuleCore

from SyncModulesPython.Core.ModulesRegistry import ModulesRegistry
# import SyncModulesPython as Modules
print
module = ModulesRegistry( 1234 )

class ClientNetwork:
	def __init__( self ):
		print( "ClientNetwork - __init__" )
		self.websocket = None

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

# await clientNetwork.connect()

async def main( ):
	clientNetwork = ClientNetwork( )
	await clientNetwork.connect( )
	asyncio.create_task( clientNetwork.listen( ) )

	message = {
		"UUID": str( uuid.uuid4( ) )
	}
	clientNetwork.sendFn( json.dumps( message ) )
	# await clientNetwork.send( json.dumps( message ) )

	await asyncio.sleep(30)

asyncio.run( main( ) )