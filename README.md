# Spindel

Spindel is a network library containing designed with a particular focus.
 - It is not using asyncio, so it should be easy to use in your application
 - It is all written in python without any dependencies besides the standard lib
 - It handles tcp connections, and on top of this it implements Websocket server and client.
 - It implements normal HTTP.
 - It can optionally use secure sockets.
 - It works by running in a single thread regardless of the number of connections established.
 - It is threadsafe!