import asyncio
import time
import json

SERVER_HOST = "localhost"
SERVER_PORT = 8000

async def handle_conn(reader, writer):
    addr = writer.get_extra_info("peername")
    print(f"[SERVER] Client connected: {addr}")

    while True:
        data = await reader.read(1024)
        if not data:
            print(f"[SERVER] Client {addr} disconnected")
            break

        try:
            request = json.loads(data.decode())
        except json.JSONDecodeError:
            request = {}

        if request.get("type") == "time req":
            server_time = time.time()  
            response = json.dumps({"type": "time resp", "server_time": server_time})
            writer.write(response.encode())
            await writer.drain()

async def main():
    server = await asyncio.start_server(handle_conn, SERVER_HOST, SERVER_PORT)
    addr = server.sockets[0].getsockname()
    print(f"[SERVER] Listening on {SERVER_HOST}:{SERVER_PORT}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
