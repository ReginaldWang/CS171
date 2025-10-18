import asyncio

SERVER_HOST = "localhost"
SERVER_PORT = 8000

async def handle_conn(reader, writer):
    addr = writer.get_extra_info("peername")
    print(f"[SERVER] Received Connection from {addr}")

    while True:
        data = await reader.read(1024)
        if not data:
            print("[SERVER] Connection Closed")
            break

        msg = data.decode()
        print(f"[SERVER] Message: {data.decode()}")

        writer.write(b"Message Received!")

async def main():
    srv = await asyncio.start_server(handle_conn, SERVER_HOST, SERVER_PORT)
    addr = srv.sockets[0].getsockname()

    print(f"[SERVER] ### SERVER LISTENING ON {SERVER_HOST}:{SERVER_PORT} ###")

    async with srv:
        await srv.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
