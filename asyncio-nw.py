import asyncio

NW_HOST = "localhost"
NW_PORT = 9999

SERVER_HOST = "localhost"
SERVER_PORT = 8000

async def handle_conn(reader, writer):
    addr = writer.get_extra_info("peername")
    print(f"[NW] Received Connection from {addr}")

    while True:
        data = await reader.read(1024)
        if not data:
            print("[NW] Connection Closed")
            break

        msg = data.decode()
        print(f"[NW] Message: {msg}")

        writer.write(b"Message Received!")

        reversed_msg = msg[::-1]
        await asyncio.sleep(5)

        await tcp_client(reversed_msg, SERVER_HOST, SERVER_PORT)

async def tcp_client(msg, host, port):
    reader, writer = await asyncio.open_connection(host, port)

    writer.write(msg.encode())
    await writer.drain()

    data = await reader.read(1024)
    print(f"[NW] Server Response: {data.decode()}")

    writer.close()
    await writer.wait_closed()

async def main():
    srv = await asyncio.start_server(handle_conn, NW_HOST, NW_PORT)
    addr = srv.sockets[0].getsockname()

    print(f"[NW] ### LISTENING ON {NW_HOST}:{NW_PORT} ###")

    async with srv:
        await srv.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
