import asyncio
import websockets


async def sender(ws: websockets.ClientConnection):
    while True:
        msg = await asyncio.to_thread(input, "Send: ")
        await ws.send(msg)


async def receiver(ws: websockets.ClientConnection):
    while True:
        msg = await ws.recv()
        print("\nServer:", msg)


async def main():
    uri = "ws://localhost:8000/ws"

    async with websockets.connect(uri) as ws:
        await asyncio.gather(
            sender(ws),
            receiver(ws),
        )


asyncio.run(main())
