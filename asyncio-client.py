import asyncio

NW_HOST = "localhost"
NW_PORT = 9999

async def tcp_client(msg, host, port):
    reader, writer = await asyncio.open_connection(host, port)

    writer.write(msg.encode())
    await writer.drain()

    data = await reader.read(1024)
    print(f"[CLIENT] Server Response: {data.decode()}")

    writer.close()
    await writer.wait_closed()

async def main():
    await tcp_client("Hello, Asyncio!", host=NW_HOST, port=NW_PORT)

if __name__ == "__main__":
    asyncio.run(main())
