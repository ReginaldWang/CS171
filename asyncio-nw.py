import asyncio
import random
import json

NW_HOST = "localhost"
NW_PORT = 9999

SERVER_HOST = "localhost"
SERVER_PORT = 8000

# -----------------------------
# Forward a single message with random delay
# -----------------------------
async def forward_message(msg, writer):
    delay = random.uniform(0.0001, 0.0005)  # 0.1 ms - 0.5 ms
    await asyncio.sleep(delay)
    writer.write(msg)
    await writer.drain()


# -----------------------------
# Handle each client connection
# -----------------------------
async def handle_conn(reader, writer):
    addr = writer.get_extra_info("peername")
    print(f"[NW] Client connected: {addr}")

    while True:
        # Receive message from client
        data = await reader.read(1024)
        if not data:
            print(f"[NW] Client {addr} disconnected")
            break

        # Forward to time server
        srv_reader, srv_writer = await asyncio.open_connection(SERVER_HOST, SERVER_PORT)
        await forward_message(data, srv_writer)

        # Receive server response
        server_response = await srv_reader.read(1024)

        # Forward server response back to client
        await forward_message(server_response, writer)

        srv_writer.close()
        await srv_writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_conn, NW_HOST, NW_PORT)
    addr = server.sockets[0].getsockname()
    print(f"[NW] Listening on {NW_HOST}:{NW_PORT}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
