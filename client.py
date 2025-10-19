import asyncio
import json
import time
import csv
import argparse

NW_HOST = "localhost"
NW_PORT = 9999

class LocalClock:
    def __init__(self, rho):
        self.L_base = time.time()   
        self.R_base = time.time()   
        self.rho = rho

    def now(self):
        R_now = time.time()
        return self.L_base + (R_now - self.R_base) * (1 + self.rho)

    def adjust(self, offset):
        self.L_base = self.now() + offset
        self.R_base = time.time()

async def sync_with_server(local_clock):
    reader, writer = await asyncio.open_connection(NW_HOST, NW_PORT)

    T1 = local_clock.now()
    request = json.dumps({"type": "time req"})
    writer.write(request.encode())
    await writer.drain()

    data = await reader.read(1024)
    T3 = local_clock.now()  
    response = json.loads(data.decode())
    Ts = response["server_time"]

    RTT = T3 - T1
    d = RTT / 2
    offset = Ts - (T1 + d)

    local_clock.adjust(offset)

    writer.close()
    await writer.wait_closed()

async def main(duration, epsilon_max, rho):
    local_clock = LocalClock(rho)
    start_time = time.time()
    end_time = start_time + duration

    with open("clock_log.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["actual_time", "local_time"])
        print("actual_time,local_time")

        while time.time() < end_time:
            actual_time = time.time()
            local_time = local_clock.now()

            writer.writerow([f"{actual_time:.3f}", f"{local_time:.3f}"])
            print(f"{actual_time:.3f},{local_time:.3f}")

            if abs(local_time - actual_time + rho) >= epsilon_max:
                await sync_with_server(local_clock)
                delayed_time = time.time() - actual_time
                await asyncio.sleep(max(0, 1 - delayed_time))

            else: 
                await asyncio.sleep(1)  

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--d", type=int, default=30, help="Duration in seconds")
    parser.add_argument("--epsilon_max", type=float, default=0.05, help="Max tolerable error")
    parser.add_argument("--rho", type=float, default=1e-6, help="Clock drift")
    args = parser.parse_args()

    asyncio.run(main(args.d, args.epsilon_max, args.rho))
